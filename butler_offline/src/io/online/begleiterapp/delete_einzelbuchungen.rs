use crate::io::online::begleiterapp::routes::einzelbuchungen_route;
use crate::io::online::request::{delete_request, ErrorOnRequest};
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;

pub async fn delete_einzelbuchungen(
    server_configuration: &ServerConfiguration,
    login_credentials: LoginCredentials,
) -> Result<(), ErrorOnRequest> {
    let url = einzelbuchungen_route(server_configuration);
    delete_request(url, login_credentials).await?;
    Ok(())
}
