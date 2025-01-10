use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::io::http::redirect::http_redirect;
use crate::io::http::shared::server_url_updater::update_server_url;
use crate::io::online::login::request_login;
use crate::model::local::LocalServerName;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    OnlineRedirectAction, OnlineRedirectActionType, OnlineRedirectActionWrapper,
    OnlineRedirectState, RootPath,
};
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, Responder};
use serde::Deserialize;

#[post("/import/gemeinsam")]
pub async fn import_gemeinsam_request(
    online_redirect_state: Data<OnlineRedirectState>,
    form: Form<ImportFormData>,
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    root_path: Data<RootPath>,
    local_server_name: Data<LocalServerName>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_id, database.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let mut online_redirect = online_redirect_state.redirect_state.lock().unwrap();
    *online_redirect = OnlineRedirectActionWrapper {
        action: Some(OnlineRedirectAction {
            typ: OnlineRedirectActionType::ImportGemeinsameBuchungen,
            database_version: database.db_version.clone(),
        }),
    };
    drop(online_redirect);

    let server_config = update_server_url(form.server_url.clone(), config, &root_path);

    http_redirect(request_login(&server_config, &local_server_name))
}

#[derive(Deserialize)]
struct ImportFormData {
    pub database_id: String,
    pub server_url: String,
}
