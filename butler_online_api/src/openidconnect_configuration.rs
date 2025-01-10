use actix_identity::Identity;
use actix_web::{HttpMessage, HttpResponse};
use dotenvy;

use actix_web::{get, post};

use crate::user::model::{Sessions, User};
use actix_web::web::{Data, Query, Redirect};
use actix_web::{error, http, HttpRequest, Responder};
use openid::{DiscoveredClient, Options, Token, Userinfo};
use serde::{Deserialize, Serialize};
use std::sync::RwLock;
use url::form_urlencoded;
use url::Url;

#[derive(Serialize, Deserialize, Debug)]
#[serde(rename_all = "camelCase")]
struct Logout {
    id_token: String,
    logout_url: Option<Url>,
}

#[derive(Serialize, Deserialize, Debug)]
struct Failure {
    error: String,
}

pub struct AllowedRedirects {
    pub allowed: Vec<String>,
}

#[get("/oauth2/authorization/oidc")]
async fn authorize(oidc_client: Data<DiscoveredClient>) -> impl Responder {
    let auth_url = oidc_client.auth_url(&Options {
        scope: Some("profile".to_string()),
        ..Default::default()
    });

    eprintln!("authorize: {}", auth_url);

    HttpResponse::Found()
        .append_header((http::header::LOCATION, auth_url.to_string()))
        .finish()
}

#[derive(Deserialize, Debug)]
struct LoginQuery {
    code: String,
}

async fn request_token(
    oidc_client: Data<DiscoveredClient>,
    query: Query<LoginQuery>,
) -> Result<Option<(Token, Userinfo)>, error::Error> {
    let mut token: Token = oidc_client
        .request_token(&query.code)
        .await
        .map_err(error::ErrorInternalServerError)
        .unwrap()
        .into();

    if let Some(mut id_token) = token.id_token.as_mut() {
        oidc_client.decode_token(&mut id_token).unwrap();
        oidc_client.validate_token(&id_token, None, None).unwrap();
    } else {
        return Ok(None);
    }
    let userinfo = oidc_client
        .request_userinfo(&token)
        .await
        .map_err(error::ErrorInternalServerError)
        .unwrap();
    Ok(Some((token, userinfo)))
}

#[get("/login/oauth2/code/oidc")]
async fn login(
    oidc_client: Data<DiscoveredClient>,
    query: Query<LoginQuery>,
    sessions: Data<RwLock<Sessions>>,
    http_request: HttpRequest,
) -> impl Responder {
    match request_token(oidc_client, query).await {
        Ok(Some((token, userinfo))) => {
            let id = uuid::Uuid::new_v4().to_string();

            let login = userinfo.preferred_username.clone();
            let email = userinfo.email.clone();
            let sub: String = userinfo.sub.clone().unwrap_or_default();
            let user = User {
                id: sub.clone(),
                login,
                last_name: userinfo.family_name.clone(),
                first_name: userinfo.name.clone(),
                email,
                sub: userinfo.sub.clone().unwrap(),
                activated: userinfo.email_verified,
                image_url: userinfo.picture.clone().map(|x| x.to_string()),
                lang_key: Some("en".to_string()),
                authorities: vec!["ROLE_USER".to_string()], //FIXME: read from token
            };
            eprintln!("{:?}", user);
            sessions
                .write()
                .unwrap()
                .map
                .insert(id.clone(), (user, token, userinfo));
            Identity::login(&http_request.extensions(), id).unwrap();

            Redirect::to("/").temporary()
        }
        Ok(None) => {
            eprintln!("login error in call: no id_token found");

            Redirect::to("/").temporary()
        }
        Err(err) => {
            eprintln!("login error in call: {:?}", err);
            Redirect::to("/").temporary()
        }
    }
}

#[derive(Debug, Deserialize)]
pub struct OfflineAccessParams {
    pub redirect: Option<String>,
}

#[get("/offline/access")]
async fn offline_access(
    user: User,
    http_message: HttpRequest,
    request_params: Query<OfflineAccessParams>,
    allowed_redirects: Data<AllowedRedirects>,
) -> impl Responder {
    let cookie = http_message
        .headers()
        .get("Cookie")
        .unwrap()
        .to_str()
        .unwrap();
    let params = form_urlencoded::Serializer::new(String::new())
        .append_pair("user", &user.sub)
        .append_pair("session", cookie)
        .finish();

    let redirect_location = request_params
        .redirect
        .clone()
        .unwrap_or("http://localhost:5000".to_string());

    eprintln!("offline_access: {:?}", redirect_location);
    if !allowed_redirects
        .allowed
        .iter()
        .any(|e| e == &redirect_location)
    {
        eprintln!("offline_access: redirect not allowed");
        eprintln!(
            "redirect is not in allowed list: {:?}",
            allowed_redirects.allowed
        );
        eprintln!(
            "offline_access: redirect to {} without token",
            redirect_location
        );
        return Redirect::to(redirect_location.to_string());
    }
    eprintln!("offline_access: redirect allowed");

    let url = format!("{}/butler-online-callback?{}", redirect_location, params);
    Redirect::to(url)
}

#[post("/logout")]
async fn logout(
    oidc_client: Data<DiscoveredClient>,
    sessions: Data<RwLock<Sessions>>,
    identity: Identity,
) -> impl Responder {
    if let Some(id) = identity.id().ok() {
        if let Some((user, token, _userinfo)) = sessions.write().unwrap().map.remove(&id) {
            eprintln!("logout user: {:?}", user);

            identity.logout();
            let id_token = token.bearer.access_token.into();
            let logout_url = oidc_client.config().end_session_endpoint.clone();

            return HttpResponse::Ok().json(Logout {
                id_token,
                logout_url,
            });
        }
    }
    HttpResponse::Unauthorized().finish()
}

pub fn compute_allowed_redirects() -> AllowedRedirects {
    let conf = dotenvy::var("ALLOWED_REDIRECTS").unwrap_or("http://localhost:5000".to_string());
    if conf.contains(',') {
        let allowed = conf.split(',').map(|x| x.to_string()).collect();
        eprintln!("allowed offline redirects: {:?}", allowed);
        return AllowedRedirects { allowed };
    }
    eprintln!("allowed offline redirects: {:?}", conf);
    let allowed = vec![conf];
    AllowedRedirects { allowed }
}

pub async fn generate_discovery_client() -> Result<openid::Client, error::Error> {
    let client_id = dotenvy::var("CLIENT_ID").unwrap();
    let client_secret = dotenvy::var("CLIENT_SECRET").unwrap();
    let redirect = Some(host("/api/login/login/oauth2/code/oidc"));
    let issuer = Url::parse(&dotenvy::var("ISSUER").unwrap().as_str()).unwrap();
    let client = DiscoveredClient::discover(client_id, client_secret, redirect, issuer)
        .await
        .map_err(error::ErrorInternalServerError)
        .unwrap();

    Ok(client)
}

pub fn host(path: &str) -> String {
    dotenvy::var("HOSTNAME").unwrap() + path
}
