use crate::budgetbutler::pages::sparen::action_add_edit_sparbuchung::{
    submit_sparbuchung, SubmitSparbuchungContext,
};
use crate::budgetbutler::pages::sparen::action_delete_sparbuchung::{
    delete_sparbuchung, DeleteContext,
};
use crate::budgetbutler::pages::sparen::add_sparbuchung::{handle_view, AddSparbuchungenContext};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::SPAREN_SPARBUCHUNG_ADD;
use crate::io::disk::primitive::segment_reader::Element;
use crate::io::disk::primitive::sparbuchungtyp::read_sparbuchungtyp;
use crate::io::html::views::sparen::add_sparbuchungen::render_add_sparbuchung_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::SparbuchungenChanges;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("add_sparbuchung/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    sparbuchungen_changes: Data<SparbuchungenChanges>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Neues Sparkonto hinzufügen",
        SPAREN_SPARBUCHUNG_ADD,
        AddSparbuchungenContext {
            database: &database_guard,
            sparbuchung_changes: &sparbuchungen_changes.changes.lock().unwrap(),
            edit_buchung: None,
            heute: today(),
        },
        handle_view,
        render_add_sparbuchung_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("add_sparbuchung/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    sparbuchungen_changes: Data<SparbuchungenChanges>,
    form: Form<EditFormData>,
    config: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_id, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Konto editieren",
        SPAREN_SPARBUCHUNG_ADD,
        AddSparbuchungenContext {
            database: &database_guard,
            sparbuchung_changes: &sparbuchungen_changes.changes.lock().unwrap(),
            edit_buchung: Some(form.edit_index),
            heute: today(),
        },
        handle_view,
        render_add_sparbuchung_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    database_id: String,
}

#[post("add_sparbuchung/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    sparbuchungen_changes: Data<SparbuchungenChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitSparbuchungContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                typ: read_sparbuchungtyp(Element::new(form_data.typ.clone())),
                wert: BetragOhneVorzeichen::from_user_input(&form_data.wert),
                konto: KontoReferenz::new(Name::new(form_data.konto.clone())),
                datum: Datum::from_iso_string(&form_data.datum),
            },
        },
        &sparbuchungen_changes.changes,
        submit_sparbuchung,
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

#[post("add_sparbuchung/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    sparbuchungen_changes: Data<SparbuchungenChanges>,
    form_data: Form<DeleteFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: DeleteContext {
                database: &database,
                delete_index: form_data.delete_index,
            },
        },
        &sparbuchungen_changes.changes,
        delete_sparbuchung,
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
    database_id: String,
}

#[derive(Deserialize)]
struct SubmitFormData {
    database_id: String,
    edit_index: Option<u32>,
    datum: String,
    name: String,
    wert: String,
    typ: String,
    konto: String,
}
