use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Deserialize, Serialize)]
pub struct ServerConfiguration {
    pub server_url: String,
}

impl ServerConfiguration {
    pub fn new(server_url: String) -> ServerConfiguration {
        ServerConfiguration { server_url }
    }
}
