use crate::database::DbPool;
use crate::einzelbuchungen::output_db::repository;
use crate::gemeinsame_buchungen::output_db;
use crate::uebersicht::uebersicht_service::berechne_uebersicht;
use crate::user::model::User;
use actix_web::{error, get, web, HttpResponse, Responder};

#[get("/einzelbuchungen_uebersicht")]
pub async fn get_einzelbuchungen_uebersicht(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;

    let buchungen = web::block(move || {
        let mut conn = pool.get()?;
        repository::find_all_einzelbuchungen(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    let uebersicht = berechne_uebersicht(&buchungen);

    Ok(HttpResponse::Ok().json(uebersicht.to_dto()))
}

#[get("/gemeinsame_buchungen_uebersicht")]
pub async fn get_gemeinsame_buchungen_uebersicht(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let buchungen = web::block(move || {
        let mut conn = pool.get()?;
        output_db::find_all_gemeinsame_buchungen(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    let uebersicht = berechne_uebersicht(&buchungen);

    Ok(HttpResponse::Ok().json(uebersicht.to_dto()))
}
