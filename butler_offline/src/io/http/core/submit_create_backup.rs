use crate::budgetbutler::view::request_handler::Redirect;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::disk::writer::create_database_backup;
use crate::io::http::redirect::http_redirect;
use crate::io::time::{now, today};
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{post, HttpResponse};

#[post("configuration/submit/backup")]
pub async fn submit(
    state: Data<ApplicationState>,
    config: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = state.database.lock().unwrap();
    let config_guard = config.configuration.lock().unwrap();
    create_database_backup(
        &database_guard,
        &config_guard.backup_configuration,
        today(),
        now(),
        "manual_backup",
    );

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}
