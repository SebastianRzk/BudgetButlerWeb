use crate::budgetbutler::pages::gemeinsame_buchungen::action_add_edit_gemeinsame_buchung::{
    submit_gemeinsame_ausgabe, SubmitGemeinsameBuchungContext,
};
use crate::budgetbutler::pages::gemeinsame_buchungen::action_delete_gemeinsame_buchung::{
    delete_gemeinsame_buchung, DeleteContext,
};
use crate::budgetbutler::pages::gemeinsame_buchungen::add_gemeinsame_buchung::{
    handle_view, AddGemeinsameBuchungContext,
};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ADD;
use crate::io::html::views::gemeinsame_buchungen::add_gemeinsame_buchungen::render_add_gemeinsame_buchung_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::state::config::Config;
use crate::model::state::non_persistent_application_state::{
    AdditionalKategorie, GemeinsameBuchungenChanges,
};
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("addgemeinsam/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    gemeinsame_buchungen_changes: Data<GemeinsameBuchungenChanges>,
    extra_kategorie: Data<AdditionalKategorie>,
    config: Data<Config>,
) -> impl Responder {
    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchung hinzufügen",
        GEMEINSAME_BUCHUNGEN_ADD,
        AddGemeinsameBuchungContext {
            database: &data.database.lock().unwrap(),
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            gemeinsame_buchungen_changes: &gemeinsame_buchungen_changes.changes.lock().unwrap(),
            user_configuration: config.user_configuration.clone(),
            today: today(),
            edit_buchung: None,
        },
        handle_view,
        render_add_gemeinsame_buchung_template,
    ))
}

#[post("addgemeinsam/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    gemeinsame_buchungen_changes: Data<GemeinsameBuchungenChanges>,
    form: Form<EditFormData>,
    extra_kategorie: Data<AdditionalKategorie>,
    config: Data<Config>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.db_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchung editieren",
        GEMEINSAME_BUCHUNGEN_ADD,
        AddGemeinsameBuchungContext {
            database: &database_guard,
            user_configuration: config.user_configuration.clone(),
            extra_kategorie: &extra_kategorie.kategorie.lock().unwrap(),
            gemeinsame_buchungen_changes: &gemeinsame_buchungen_changes.changes.lock().unwrap(),
            today: today(),
            edit_buchung: Some(form.edit_index),
        },
        handle_view,
        render_add_gemeinsame_buchung_template,
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    db_version: String,
}

#[post("addgemeinsam/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    gemeinsame_buchungen_changes: Data<GemeinsameBuchungenChanges>,
    form_data: Form<SubmitFormData>,
    database_configuration: Data<Config>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let betrag = Betrag::from_iso_string(&form_data.wert);

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitGemeinsameBuchungContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                kategorie: Kategorie::new(form_data.kategorie.clone()),
                wert: betrag,
                datum: Datum::from_iso_string(&form_data.datum),
                person: Person::new(form_data.person.clone()),
            },
        },
        &gemeinsame_buchungen_changes.changes,
        submit_gemeinsame_ausgabe,
        &database_configuration.database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[post("gemeinsame_buchung/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    gemeinsame_buchungen_changes: Data<GemeinsameBuchungenChanges>,
    form_data: Form<DeleteFormData>,
    database_configuration: Data<Config>,
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
        &gemeinsame_buchungen_changes.changes,
        delete_gemeinsame_buchung,
        &database_configuration.database_configuration,
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
    database_id: String,
    edit_index: Option<u32>,
    name: String,
    kategorie: String,
    wert: String,
    datum: String,
    person: String,
}
