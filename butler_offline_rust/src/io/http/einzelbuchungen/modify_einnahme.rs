use crate::budgetbutler::pages::einzelbuchungen::action_add_edit_ausgabe::SubmitContext;
use crate::budgetbutler::pages::einzelbuchungen::action_add_edit_einnahme::submit_einnahme;
use crate::budgetbutler::pages::einzelbuchungen::add_ausgabe::AddBuchungContext;
use crate::budgetbutler::pages::einzelbuchungen::add_einnahme::handle_view;
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_EINNAHME_ADD;
use crate::io::html::views::einzelbuchungen::add_einnahme::render_add_einnahme_template;
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

#[get("addeinnahme/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    einzelbuchungen_changes: Data<EinzelbuchungenChanges>,
    extra_kategorie: Data<AdditionalKategorie>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let config = configuration_data.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Einnahme hinzufügen",
        EINZELBUCHUNGEN_EINNAHME_ADD,
        AddBuchungContext {
            database: &database,
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            einzelbuchungen_changes: &einzelbuchungen_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: None,
            ausgeschlossene_kategorien: &config.erfassungs_configuration.ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_einnahme_template,
        config.database_configuration.name.clone(),
    ))
}

#[post("addeinnahme/")]
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
    let config = configuration_data.configuration.lock().unwrap();

    HttpResponse::Ok().body(handle_render_display_view(
        "Einnahme editieren",
        EINZELBUCHUNGEN_EINNAHME_ADD,
        AddBuchungContext {
            database: &database_guard,
            einzelbuchungen_changes: &einzelbuchungen_changes.changes.lock().unwrap(),
            today: today(),
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            edit_buchung: Some(form.edit_index),
            ausgeschlossene_kategorien: &config.erfassungs_configuration.ausgeschlossene_kategorien,
        },
        handle_view,
        render_add_einnahme_template,
        config.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    db_version: String,
}

#[post("addeinnahme/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    einzelbuchung_changes: Data<EinzelbuchungenChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

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
        submit_einnahme,
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
struct SubmitFormData {
    db_version: String,
    edit_index: Option<u32>,
    name: String,
    kategorie: String,
    wert: String,
    date: String,
}
