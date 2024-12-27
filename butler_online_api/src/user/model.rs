use openid::{Token, Userinfo};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize, Debug, Default, Clone)]
#[serde(rename_all = "camelCase")]
pub struct User {
    pub id: String,
    pub login: Option<String>,
    pub first_name: Option<String>,
    pub last_name: Option<String>,
    pub sub: String,
    pub email: Option<String>,
    pub image_url: Option<String>,
    pub activated: bool,
    pub lang_key: Option<String>,
    pub authorities: Vec<String>,
}

pub struct Sessions {
    pub map: HashMap<String, (User, Token, Userinfo)>,
}
