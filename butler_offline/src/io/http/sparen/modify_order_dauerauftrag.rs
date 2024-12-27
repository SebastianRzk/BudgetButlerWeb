use crate::budgetbutler::pages::sparen::action_add_edit_order_dauerauftrag::{
    submit_order_dauerauftrag, SubmitOrderDauerauftragContext,
};
use crate::budgetbutler::pages::sparen::action_delete_order_dauerauftrag::{
    delete_order_dauerauftrag, DeleteContext,
};
use crate::budgetbutler::pages::sparen::action_split_order_dauerauftrag::{
    submit_split_order_dauerauftrag, ActionSplitOrderDauerauftragContext,
};
use crate::budgetbutler::pages::sparen::add_order_dauerauftrag::{
    handle_view, AddOrderDauerauftragContext,
};
use crate::budgetbutler::pages::sparen::split_order_dauerauftrag::{
    handle_split_order_dauerauftrag, SplitOrderDauerauftragContext,
};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_ADD;
use crate::io::disk::primitive::order_typ::read_ordertyp;
use crate::io::disk::primitive::rhythmus::read_rhythmus;
use crate::io::disk::primitive::segment_reader::Element;
use crate::io::html::views::sparen::add_order_dauerauftrag::render_add_order_dauerauftrag_template;
use crate::io::html::views::sparen::split_order_dauerauftrag::render_split_order_dauerauftrag_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::OrderDauerauftragChanges;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("add_orderdauerauftrag/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    order_dauerauftrag_changes: Data<OrderDauerauftragChanges>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Neuen Depotwert hinzufügen",
        SPAREN_ORDERDAUERAUFTRAG_ADD,
        AddOrderDauerauftragContext {
            database: &database_guard,
            order_dauerauftrag_changes: &order_dauerauftrag_changes.changes.lock().unwrap(),
            edit_buchung: None,
            heute: today(),
        },
        handle_view,
        render_add_order_dauerauftrag_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("add_orderdauerauftrag/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    order_dauerauftrag_changes: Data<OrderDauerauftragChanges>,
    form: Form<EditFormData>,
    config: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Konto editieren",
        SPAREN_ORDERDAUERAUFTRAG_ADD,
        AddOrderDauerauftragContext {
            database: &database_guard,
            order_dauerauftrag_changes: &order_dauerauftrag_changes.changes.lock().unwrap(),
            edit_buchung: Some(form.edit_index),
            heute: today(),
        },
        handle_view,
        render_add_order_dauerauftrag_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    database_version: String,
}

#[post("add_orderdauerauftrag/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    order_dauerauftrag_changes: Data<OrderDauerauftragChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_version.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitOrderDauerauftragContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                konto: KontoReferenz::new(Name::new(form_data.konto.clone())),
                start_datum: Datum::from_iso_string(&form_data.start_datum),
                ende_datum: Datum::from_iso_string(&form_data.ende_datum),
                rhythmus: read_rhythmus(Element::new(form_data.rhythmus.clone())),
                wert: OrderBetrag::new(
                    BetragOhneVorzeichen::from_user_input(&form_data.wert),
                    read_ordertyp(Element::new(form_data.typ.clone())),
                ),
                depotwert: DepotwertReferenz::new(ISIN::new(form_data.depotwert.clone())),
            },
        },
        &order_dauerauftrag_changes.changes,
        submit_order_dauerauftrag,
        &configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[post("add_orderdauerauftrag/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    order_dauerauftrag_changes: Data<OrderDauerauftragChanges>,
    form_data: Form<DeleteFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_version.clone(),
            current_db_version: database.db_version.clone(),
            context: DeleteContext {
                database: &database,
                delete_index: form_data.delete_index,
            },
        },
        &order_dauerauftrag_changes.changes,
        delete_order_dauerauftrag,
        &configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[derive(Deserialize)]
struct DeleteFormData {
    delete_index: u32,
    database_version: String,
}

#[derive(Deserialize)]
struct SubmitFormData {
    database_version: String,
    edit_index: Option<u32>,
    start_datum: String,
    ende_datum: String,
    name: String,
    konto: String,
    depotwert: String,
    wert: String,
    typ: String,
    rhythmus: String,
}

#[post("/split_orderdauerauftrag/")]
pub async fn load_split(
    data: Data<ApplicationState>,
    form: Form<SplitFormData>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let config_guard = configuration_data.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Order-Dauerauftrag teilen",
        SPAREN_ORDERDAUERAUFTRAG_ADD,
        SplitOrderDauerauftragContext {
            database: &database_guard,
            order_dauerauftrag_id: form.orderdauerauftrag_id,
        },
        handle_split_order_dauerauftrag,
        render_split_order_dauerauftrag_template,
        config_guard.database_configuration.name.clone(),
    ))
}

#[post("split_orderdauerauftrag/submit")]
pub async fn post_split_submit(
    data: Data<ApplicationState>,
    order_dauerauftraege_changes: Data<OrderDauerauftragChanges>,
    form_data: Form<SubmitSplitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_version.clone(),
            current_db_version: database.db_version.clone(),
            context: ActionSplitOrderDauerauftragContext {
                database: &database,
                order_dauerauftrag_id: form_data.orderdauerauftrag_id,
                erste_neue_buchung: Datum::from_iso_string(&form_data.datum),
                betrag: BetragOhneVorzeichen::from_user_input(&form_data.wert),
            },
        },
        &order_dauerauftraege_changes.changes,
        submit_split_order_dauerauftrag,
        &configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[derive(Deserialize)]
struct SubmitSplitFormData {
    database_version: String,
    orderdauerauftrag_id: u32,
    wert: String,
    datum: String,
}

#[derive(Deserialize)]
struct SplitFormData {
    database_version: String,
    orderdauerauftrag_id: u32,
}
