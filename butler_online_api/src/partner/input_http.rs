use serde::{Deserialize, Serialize};

use crate::database::DbPool;
use crate::partner::output_db;
use actix_web::{delete, error, get, post, web, HttpResponse, Responder};

use crate::partner::model::{NeuerPartnerStatus, PartnerStatus};
use crate::user::model::User;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeuerPartnerStatusDto {
    zielperson: String,
}

impl NeuerPartnerStatusDto {
    pub fn to_domain(&self, user: String) -> NeuerPartnerStatus {
        NeuerPartnerStatus {
            name: self.zielperson.clone(),
            user,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct PartnerStatusDto {
    pub zielperson: String,
    pub bestaetigt: bool,
}

#[post("/partnerstatus")]
pub async fn set_partnerstatus(
    pool: web::Data<DbPool>,
    form: web::Json<NeuerPartnerStatusDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let aktualisierter_partner_status = web::block(move || {
        let mut conn = pool.get()?;
        output_db::update_partnerstatus(&mut conn, form.to_domain(username))
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    Ok(HttpResponse::Created().json(aktualisierter_partner_status.to_dto()))
}

#[get("/partnerstatus")]
pub async fn get_partnerstatus(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let status = web::block(move || {
        let mut conn = pool.get()?;
        output_db::calculate_partnerstatus(&mut conn, username)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    Ok(web::Json(status.to_dto()))
}

#[delete("/partnerstatus")]
pub async fn delete_partnerstatus(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let _ = web::block(move || {
        let mut conn = pool.get()?;
        output_db::delete_partnerstatus(&mut conn, username)
    })
    .await?
    .map_err(error::ErrorInternalServerError);
    Ok(HttpResponse::Ok())
}

impl PartnerStatus {
    pub fn to_dto(&self) -> PartnerStatusDto {
        PartnerStatusDto {
            zielperson: self.zielperson.clone(),
            bestaetigt: self.bestaetigt.clone(),
        }
    }
}
