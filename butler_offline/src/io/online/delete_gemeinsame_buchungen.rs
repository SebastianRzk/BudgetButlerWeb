use crate::io::online::request::{delete_request, ErrorOnRequest};
use crate::io::online::routes::gemeinsame_buchungen_route;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;

pub async fn delete_gemeinsame_buchungen(
    server_configuration: &ServerConfiguration,
    login_credentials: LoginCredentials,
) -> Result<(), ErrorOnRequest> {
    let url = gemeinsame_buchungen_route(server_configuration);
    delete_request(url, login_credentials.clone()).await?;
    Ok(())
}
