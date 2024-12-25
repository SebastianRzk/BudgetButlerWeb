use crate::budgetbutler::pages::einzelbuchungen::action_add_edit_ausgabe::{
    submit_ausgabe, SubmitContext,
};
use crate::budgetbutler::pages::einzelbuchungen::action_delete_ausgabe::{
    delete_ausgabe, DeleteContext,
};
use crate::budgetbutler::pages::einzelbuchungen::add_ausgabe::{handle_view, AddBuchungContext};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_AUSGABE_ADD;
use crate::io::html::views::einzelbuchungen::add_ausgabe::render_add_ausgabe_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    AdditionalKategorie, EinzelbuchungenChanges,
};
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("addausgabe/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
    einzelbuchungen_changes: Data<EinzelbuchungenChanges>,
    extra_kategorie: Data<AdditionalKategorie>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let configuration = configuration_data.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Ausgabe hinzufügen",
        EINZELBUCHUNGEN_AUSGABE_ADD,
        AddBuchungContext {
            database: &database,
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            einzelbuchungen_changes: &einzelbuchungen_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: None,
            ausgeschlossene_kategorien: &configuration
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_ausgabe_template,
        configuration.database_configuration.name.clone(),
    ))
}

#[post("addausgabe/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    einzelbuchungen_changes: Data<EinzelbuchungenChanges>,
    extra_kategorie: Data<AdditionalKategorie>,
    configuration_data: Data<ConfigurationData>,
    form: Form<EditFormData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.db_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }
    let config_guard = configuration_data.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Ausgabe editieren",
        EINZELBUCHUNGEN_AUSGABE_ADD,
        AddBuchungContext {
            database: &database_guard,
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            einzelbuchungen_changes: &einzelbuchungen_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: Some(form.edit_index),
            ausgeschlossene_kategorien: &config_guard
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_ausgabe_template,
        config_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    db_version: String,
}

#[post("addausgabe/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    einzelbuchung_changes: Data<EinzelbuchungenChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let configuration = configuration.configuration.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.db_version.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                kategorie: Kategorie::new(form_data.kategorie.clone()),
                wert: Betrag::from_user_input(&form_data.wert),
                datum: Datum::from_iso_string(&form_data.date),
            },
        },
        &einzelbuchung_changes.changes,
        submit_ausgabe,
        &configuration.database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[post("addausgabe/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    einzelbuchung_changes: Data<EinzelbuchungenChanges>,
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
        &einzelbuchung_changes.changes,
        delete_ausgabe,
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
    db_version: String,
}

#[derive(Deserialize)]
struct SubmitFormData {
    db_version: String,
    edit_index: Option<u32>,
    name: String,
    kategorie: String,
    wert: String,
    date: String,
}
