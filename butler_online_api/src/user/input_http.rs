use actix_web::{get, HttpResponse, Responder};
use serde::{Serialize};
use crate::user::model::User;


#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct UserInfoDto {
    logged_in: bool,
    user_name: String
}

#[get("/user")]
pub async fn user_info(user: Option<User>) -> actix_web::Result<impl Responder> {
    if user.is_some(){
        let user_: User = user.unwrap();
        return Ok(HttpResponse::Ok().json(UserInfoDto{
            user_name: user_.sub,
            logged_in: true
        }))
    }
    Ok(HttpResponse::Ok().json(UserInfoDto{
        user_name: "".to_string(),
        logged_in: false
    }))
}
