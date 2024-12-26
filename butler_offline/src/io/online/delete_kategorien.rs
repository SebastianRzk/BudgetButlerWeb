use crate::io::online::request::{delete_request, ErrorOnRequest};
use crate::io::online::routes::kategorien_route;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;

pub async fn request_delete_kategorien(
    server_configuration: &ServerConfiguration,
    login_credentials: LoginCredentials,
) -> Result<(), ErrorOnRequest> {
    let url = kategorien_route(server_configuration);
    delete_request(url, login_credentials).await?;
    Ok(())
}
