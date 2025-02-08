use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use uuid::Uuid;
use crate::database::DbPool;
use crate::einzelbuchungen::input_http::dtos::{EinzelbuchungDto, NeueEinzelbuchungDto};
use crate::einzelbuchungen::model::Einzelbuchung;
use crate::einzelbuchungen::output_db::repository;
use crate::result_dto::result_success;
use crate::user::model::User;

#[post("/einzelbuchung")]
pub async fn add_einzelbuchung(
    pool: web::Data<DbPool>,
    form: web::Json<NeueEinzelbuchungDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _einzelbuchung = web::block(move || {
        let mut conn = pool.get()?;
        repository::insert_new_einzelbuchung(&mut conn, form.to_domain(user))
    })
        .await?
        .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(result_success("Buchung erfolgreich gespeichert")))
}

#[get("/einzelbuchungen")]
pub async fn get_einzelbuchungen(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    eprintln!("rufe daten ab für {:?}", user.clone());
    let buchungen = web::block(move || {
        let mut conn = pool.get()?;
        repository::find_all_einzelbuchungen(&mut conn, user)
    })
        .await?
        .map_err(error::ErrorInternalServerError)?;
    let dtos = buchungen
        .iter()
        .map(Einzelbuchung::to_dto)
        .collect::<Vec<EinzelbuchungDto>>();
    Ok(HttpResponse::Ok().json(dtos))
}

#[delete("/einzelbuchung/{einzelbuchung_id}")]
pub async fn delete_einzelbuchung(
    pool: web::Data<DbPool>,
    einzelbuchung_id: web::Path<Uuid>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let einzelbuchung_id = einzelbuchung_id.into_inner();
    let _ = web::block(move || {
        let mut conn = pool.get()?;
        repository::delete_einzelbuchung(&mut conn, user, einzelbuchung_id)
    })
        .await?
        .map_err(error::ErrorInternalServerError);
    Ok(HttpResponse::Ok().json(result_success("Buchung erfolgreich gelöscht")))
}

#[delete("/einzelbuchungen")]
pub async fn delete_einzelbuchungen(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _result = web::block(move || {
        let mut conn = pool.get()?;
        return repository::delete_all_einzelbuchungen(&mut conn, user);
    })
        .await?
        .map_err(error::ErrorInternalServerError)?;
    Ok(HttpResponse::Ok())
}