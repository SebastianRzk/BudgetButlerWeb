use crate::budgetbutler::view::redirect_targets::redirect_to_dashboard;
use crate::io::disk::reader::read_database;
use crate::io::http::redirect::http_redirect;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse};

#[get("reload_database/")]
pub async fn submit_reload_database(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
) -> HttpResponse {
    let mut database = data.database.lock().unwrap();
    let conf = configuration_data.configuration.lock().unwrap();

    let refreshed_database = read_database(
        &conf.database_configuration,
        database.db_version.increment(),
    );

    *database = refreshed_database;
    drop(database);

    http_redirect(redirect_to_dashboard())
}
