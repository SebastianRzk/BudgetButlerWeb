use crate::budgetbutler::view::request_handler::Redirect;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::disk::writer::create_database_backup;
use crate::io::http::redirect::http_redirect;
use crate::io::time::{now, today};
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{post, HttpResponse};

#[post("configuration/submit/backup")]
pub async fn submit(
    state: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    user_application_directory: Data<UserApplicationDirectory>,
) -> HttpResponse {
    let database_guard = state.database.lock().unwrap();
    let config_guard = config.configuration.lock().unwrap();
    create_database_backup(
        &database_guard,
        &config_guard.backup_configuration,
        &user_application_directory,
        today(),
        now(),
        "manual_backup",
    );

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}
