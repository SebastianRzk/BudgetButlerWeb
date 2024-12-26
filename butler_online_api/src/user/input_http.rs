use crate::user::model::{Sessions, User};
use actix_identity::Identity;
use actix_web::dev::Payload;
use actix_web::error::ErrorUnauthorized;
use actix_web::{error, get, web, FromRequest, HttpRequest, HttpResponse, Responder};
use serde::Serialize;
use std::future::Future;
use std::pin::Pin;
use std::sync::RwLock;

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct UserInfoDto {
    logged_in: bool,
    user_name: String,
}

#[get("/user")]
pub async fn user_info(user: Option<User>) -> actix_web::Result<impl Responder> {
    if user.is_some() {
        let user_: User = user.unwrap();
        return Ok(HttpResponse::Ok().json(UserInfoDto {
            user_name: user_.sub,
            logged_in: true,
        }));
    }
    Ok(HttpResponse::Ok().json(UserInfoDto {
        user_name: "".to_string(),
        logged_in: false,
    }))
}

impl FromRequest for User {
    type Error = error::Error;
    type Future = Pin<Box<dyn Future<Output = Result<User, error::Error>>>>;

    fn from_request(req: &HttpRequest, pl: &mut Payload) -> Self::Future {
        let fut = Identity::from_request(req, pl);
        let sessions: Option<&web::Data<RwLock<Sessions>>> = req.app_data();
        if sessions.is_none() {
            eprintln!("sessions is none!");
            return Box::pin(async { Err(ErrorUnauthorized("unauthorized")) });
        }
        let sessions = sessions.unwrap().clone();

        Box::pin(async move {
            let id = fut
                .await
                .map_err(error::ErrorInternalServerError)?
                .id()
                .ok();

            if let Some(identity) = id {
                if let Some(user) = sessions
                    .read()
                    .unwrap()
                    .map
                    .get(&identity)
                    .map(|x| x.0.clone())
                {
                    return Ok(user);
                }
            };

            Err(ErrorUnauthorized("unauthorized"))
        })
    }
}
