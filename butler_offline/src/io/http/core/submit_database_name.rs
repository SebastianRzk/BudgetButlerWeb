use crate::budgetbutler::pages::core::action_rename_database::{
    action_rename_database, RenameDatabaseContext,
};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::budgetbutler::view::request_handler::Redirect;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::disk::updater::update_database;
use crate::io::disk::writer::create_database_backup;
use crate::io::http::redirect::http_redirect;
use crate::io::time::{now, today};
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::RootPath;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, HttpResponse};
use serde::Deserialize;

#[post("configuration/submit/database_name")]
pub async fn submit(
    data: Data<ApplicationState>,
    configuration: Data<ConfigurationData>,
    root_path: Data<RootPath>,
    form: Form<SubmitDatabaseNameFormData>,
) -> HttpResponse {
    let mut database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_id, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }
    let mut config = configuration.configuration.lock().unwrap();

    let result = action_rename_database(RenameDatabaseContext {
        new_database_name: form.database_name.clone(),
        database: &database_guard,
        config: &config,
    });

    create_database_backup(
        &database_guard,
        &config.backup_configuration,
        today(),
        now(),
        "before_rename",
    );
    let refreshed_database = update_database(
        &result.new_config.database_configuration,
        result.new_database,
    );
    *database_guard = refreshed_database;
    create_database_backup(
        &database_guard,
        &result.new_config.backup_configuration,
        today(),
        now(),
        "after_rename",
    );

    let refreshed_config = update_configuration(&root_path.path, result.new_config);
    *config = refreshed_config;

    drop(database_guard);
    drop(config);

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}

#[derive(Deserialize)]
struct SubmitDatabaseNameFormData {
    database_name: String,
    database_id: String,
}
