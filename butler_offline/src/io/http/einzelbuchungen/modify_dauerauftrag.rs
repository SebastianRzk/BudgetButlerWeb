use crate::budgetbutler::pages::einzelbuchungen::action_add_edit_dauerauftrag::{
    submit_dauerauftrag, SubmitDauerauftragContext,
};
use crate::budgetbutler::pages::einzelbuchungen::action_delete_dauerauftrag::{
    delete_dauerauftrag, DeleteContext,
};
use crate::budgetbutler::pages::einzelbuchungen::action_split_dauerauftrag::{
    submit_split_dauerauftrag, ActionSplitDauerauftragContext,
};
use crate::budgetbutler::pages::einzelbuchungen::add_dauerauftrag::{
    handle_view, AddDauerauftragContext,
};
use crate::budgetbutler::pages::einzelbuchungen::split_dauerauftrag::{
    handle_split, SplitDauerauftragContext,
};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_DAUERAUFTRAG_ADD;
use crate::io::html::views::einzelbuchungen::add_dauerauftrag::render_add_dauerauftrag_template;
use crate::io::html::views::einzelbuchungen::split_dauerauftrag::render_split_dauerauftrag_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    AdditionalKategorie, DauerauftraegeChanges,
};
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("adddauerauftrag/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    dauerauftraege_changes: Data<DauerauftraegeChanges>,
    extra_kategorie: Data<AdditionalKategorie>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let config = configuration_data.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Dauerauftrag hinzufügen",
        EINZELBUCHUNGEN_DAUERAUFTRAG_ADD,
        AddDauerauftragContext {
            database: &database,
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            dauerauftraege_changes: &dauerauftraege_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: None,
            ausgeschlossene_kategorien: &config.erfassungs_configuration.ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_dauerauftrag_template,
        config.database_configuration.name.clone(),
    ))
}

#[post("adddauerauftrag/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    dauerauftraege_changes: Data<DauerauftraegeChanges>,
    form: Form<EditFormData>,
    extra_kategorie: Data<AdditionalKategorie>,
    configuration_data: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.db_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }
    let config_guard = configuration_data.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Dauerauftrag editieren",
        EINZELBUCHUNGEN_DAUERAUFTRAG_ADD,
        AddDauerauftragContext {
            database: &database_guard,
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            dauerauftraege_changes: &dauerauftraege_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: Some(form.edit_index),
            ausgeschlossene_kategorien: &config_guard
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_dauerauftrag_template,
        config_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    db_version: String,
}

#[post("adddauerauftrag/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    dauerauftraege_changes: Data<DauerauftraegeChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let betrag: Betrag;
    if form_data.typ == "Ausgabe" {
        betrag = Betrag::from_user_input(&form_data.wert).negativ();
    } else {
        betrag = Betrag::from_user_input(&form_data.wert);
    }

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitDauerauftragContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                kategorie: Kategorie::new(form_data.kategorie.clone()),
                wert: betrag,
                start_datum: Datum::from_iso_string(&form_data.start_datum),
                ende_datum: Datum::from_iso_string(&form_data.ende_datum),
                rhythmus: Rhythmus::from_german_string(&form_data.rhythmus),
            },
        },
        &dauerauftraege_changes.changes,
        submit_dauerauftrag,
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

#[post("adddauerauftrag/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    dauerauftrag_changes: Data<DauerauftraegeChanges>,
    form_data: Form<DeleteFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.db_version.clone(),
            current_db_version: database.db_version.clone(),
            context: DeleteContext {
                database: &database,
                delete_index: form_data.delete_index,
            },
        },
        &dauerauftrag_changes.changes,
        delete_dauerauftrag,
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

#[post("/splitdauerauftrag/")]
pub async fn load_split(
    data: Data<ApplicationState>,
    form: Form<SplitFormData>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_id, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let config_guard = configuration_data.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Dauerauftrag teilen",
        EINZELBUCHUNGEN_DAUERAUFTRAG_ADD,
        SplitDauerauftragContext {
            database: &database_guard,
            dauerauftrag_id: form.dauerauftrag_id,
        },
        handle_split,
        render_split_dauerauftrag_template,
        config_guard.database_configuration.name.clone(),
    ))
}

#[post("splitdauerauftrag/submit")]
pub async fn post_split_submit(
    data: Data<ApplicationState>,
    dauerauftraege_changes: Data<DauerauftraegeChanges>,
    form_data: Form<SubmitSplitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: ActionSplitDauerauftragContext {
                database: &database,
                dauerauftrag_id: form_data.dauerauftrag_id,
                erste_neue_buchung: Datum::from_iso_string(&form_data.datum),
                betrag: Betrag::from_user_input(&form_data.wert),
            },
        },
        &dauerauftraege_changes.changes,
        submit_split_dauerauftrag,
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
    database_id: String,
    dauerauftrag_id: u32,
    wert: String,
    datum: String,
}

#[derive(Deserialize)]
struct SplitFormData {
    database_id: String,
    dauerauftrag_id: u32,
}

#[derive(Deserialize)]
struct DeleteFormData {
    delete_index: u32,
    db_version: String,
}

#[derive(Deserialize)]
struct SubmitFormData {
    database_id: String,
    edit_index: Option<u32>,
    name: String,
    kategorie: String,
    wert: String,
    start_datum: String,
    ende_datum: String,
    rhythmus: String,
    typ: String,
}
