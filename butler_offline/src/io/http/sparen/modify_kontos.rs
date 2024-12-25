use crate::budgetbutler::pages::sparen::action_add_edit_konto::{
    submit_sparkonto, SubmitKontoContext,
};
use crate::budgetbutler::pages::sparen::action_delete_sparkonto::delete_sparkonto;
use crate::budgetbutler::pages::sparen::action_delete_sparkonto::DeleteContext;
use crate::budgetbutler::pages::sparen::add_konto::{handle_view, AddKontoContext};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::SPAREN_SPARKONTO_ADD;
use crate::io::disk::primitive::segment_reader::Element;
use crate::io::disk::primitive::sparkontotyp::read_sparkontotyp;
use crate::io::html::views::sparen::add_konto::render_add_konto_template;
use crate::io::http::redirect::http_redirect;
use crate::model::primitives::name::Name;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::KontoChanges;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("add_konto/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    konto_changes: Data<KontoChanges>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Neues Sparkonto hinzufügen",
        SPAREN_SPARKONTO_ADD,
        AddKontoContext {
            database: &database_guard,
            konto_changes: &konto_changes.changes.lock().unwrap(),
            edit_buchung: None,
        },
        handle_view,
        render_add_konto_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("add_kontos/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    konto_changes: Data<KontoChanges>,
    form: Form<EditFormData>,
    config: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.db_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Konto editieren",
        SPAREN_SPARKONTO_ADD,
        AddKontoContext {
            database: &database_guard,
            konto_changes: &konto_changes.changes.lock().unwrap(),
            edit_buchung: Some(form.edit_index),
        },
        handle_view,
        render_add_konto_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_index: u32,
    db_version: String,
}

#[post("add_konto/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    add_konto_changes: Data<KontoChanges>,
    form_data: Form<SubmitFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: SubmitKontoContext {
                database: &database,
                edit_index: form_data.edit_index,
                name: Name::new(form_data.name.clone()),
                kontotyp: read_sparkontotyp(Element::new(form_data.typ.clone())),
            },
        },
        &add_konto_changes.changes,
        submit_sparkonto,
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

#[post("add_konto/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    konto_changes: Data<KontoChanges>,
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
        &konto_changes.changes,
        delete_sparkonto,
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
    database_id: String,
    edit_index: Option<u32>,
    name: String,
    typ: String,
}
