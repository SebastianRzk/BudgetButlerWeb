use crate::database::DbPool;
use crate::einzelbuchungen::model::{Einzelbuchung, NeueEinzelbuchung};
use crate::einzelbuchungen::output_db;
use crate::result_dto::result_success;
use crate::user::model::User;
use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use bigdecimal::BigDecimal;
use serde::{Deserialize, Serialize};
use time::macros::format_description;
use time::Date;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct NeueEinzelbuchungDto {
    pub name: String,
    pub kategorie: String,
    pub datum: String,
    pub wert: BigDecimal,
}

impl NeueEinzelbuchungDto {
    pub fn to_domain(&self, user: String) -> NeueEinzelbuchung {
        NeueEinzelbuchung {
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            datum: Date::parse(
                self.datum.as_str(),
                format_description!("[year]-[month]-[day]"),
            )
            .unwrap(),
            user,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct EinzelbuchungDto {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: String,
    pub user: String,
}

#[post("/einzelbuchung")]
pub async fn add_einzelbuchung(
    pool: web::Data<DbPool>,
    form: web::Json<NeueEinzelbuchungDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _einzelbuchung = web::block(move || {
        let mut conn = pool.get()?;
        output_db::insert_new_einzelbuchung(&mut conn, form.to_domain(user))
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
    let users = web::block(move || {
        let mut conn = pool.get()?;
        output_db::find_all_einzelbuchungen(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    let dtos = users
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
        output_db::delete_einzelbuchung(&mut conn, user, einzelbuchung_id)
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
        return output_db::delete_all_einzelbuchungen(&mut conn, user);
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    Ok(HttpResponse::Ok())
}

impl Einzelbuchung {
    pub fn to_dto(&self) -> EinzelbuchungDto {
        EinzelbuchungDto {
            datum: self.datum.to_string(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
        }
    }
}
