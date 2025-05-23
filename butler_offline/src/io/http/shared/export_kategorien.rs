use crate::io::http::redirect::http_redirect;
use crate::io::http::shared::server_url_updater::update_server_url;
use crate::io::online::begleiterapp::login::request_login;
use crate::model::local::LocalServerName;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    OnlineRedirectAction, OnlineRedirectActionType, OnlineRedirectActionWrapper,
    OnlineRedirectState, UserApplicationDirectory,
};
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, Responder};
use serde::Deserialize;

#[post("/import/kategorien")]
pub async fn export_kategorien_request(
    online_redirect_state: Data<OnlineRedirectState>,
    form: Form<ImportFormData>,
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    root_path: Data<UserApplicationDirectory>,
    local_server_name: Data<LocalServerName>,
) -> impl Responder {
    let database = data.database.lock().unwrap();

    let mut online_redirect = online_redirect_state.redirect_state.lock().unwrap();
    *online_redirect = OnlineRedirectActionWrapper {
        action: Some(OnlineRedirectAction {
            typ: OnlineRedirectActionType::UploadKategorien,
            database_version: database.db_version.clone(),
        }),
    };
    drop(online_redirect);

    let server_config = update_server_url(form.server_url.clone(), config, &root_path);

    http_redirect(request_login(&server_config, &local_server_name))
}

#[derive(Deserialize)]
struct ImportFormData {
    pub server_url: String,
}
