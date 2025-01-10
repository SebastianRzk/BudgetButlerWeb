use crate::io::online::request::{post_request, ErrorOnRequest};
use crate::io::online::routes::kategorien_batch_route;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::remote::login::LoginCredentials;
use crate::model::remote::server::ServerConfiguration;

pub async fn request_set_kategorien(
    server_configuration: &ServerConfiguration,
    login_credentials: LoginCredentials,
    kategorien: Vec<Kategorie>,
) -> Result<(), ErrorOnRequest> {
    let url = kategorien_batch_route(server_configuration);
    let unpacked_kategorien: Vec<String> = kategorien.iter().map(|x| x.kategorie.clone()).collect();
    let kategorien_as_string = serde_json::to_string(&unpacked_kategorien).unwrap();
    eprintln!("Setting Kategorien to: {}", url);
    post_request(url, login_credentials, kategorien_as_string).await?;
    Ok(())
}
