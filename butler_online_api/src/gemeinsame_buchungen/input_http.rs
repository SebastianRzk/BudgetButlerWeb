use crate::database::DbPool;
use crate::gemeinsame_buchungen::model::{GemeinsameBuchung, NeueGemeinsameBuchung};
use crate::gemeinsame_buchungen::output_db;
use crate::partner::output_db::calculate_partnerstatus;
use crate::result_dto::result_success;
use crate::user::model::User;
use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use bigdecimal::BigDecimal;
use serde::{Deserialize, Serialize};
use time::macros::format_description;
use time::Date;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct NeueGemeinsameBuchungDto {
    pub name: String,
    pub kategorie: String,
    pub datum: String,
    pub wert: BigDecimal,
    pub eigene_buchung: bool,
}

impl NeueGemeinsameBuchungDto {
    pub fn to_domain(&self, user: String, partnerperson: String) -> NeueGemeinsameBuchung {
        let mut zielperson: String = user.clone();
        if !self.eigene_buchung.clone() {
            zielperson = partnerperson
        }

        NeueGemeinsameBuchung {
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            datum: Date::parse(
                self.datum.as_str(),
                format_description!("[year]-[month]-[day]"),
            )
            .unwrap(),
            user,
            zielperson,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
pub struct GemeinsameBuchungDto {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: String,
    pub user: String,
    pub zielperson: String,
}

#[post("/gemeinsame_buchung")]
pub async fn add_gemeinsame_buchung(
    pool: web::Data<DbPool>,
    form: web::Json<NeueGemeinsameBuchungDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let _einzelbuchung = web::block(move || {
        let mut conn = pool.get()?;

        let partner: String = calculate_partnerstatus(&mut conn, username.clone())
            .unwrap()
            .zielperson;

        output_db::insert_new_gemeinsame_buchung(&mut conn, form.to_domain(username, partner))
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(result_success("Buchung erfolgreich gespeichert")))
}

#[post("/gemeinsame_buchung/batch")]
pub async fn add_gemeinsame_buchungen(
    pool: web::Data<DbPool>,
    form: web::Json<Vec<NeueGemeinsameBuchungDto>>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub.clone();

    let _gespeichterte_gemeinsame_buchungen = web::block(move || {
        let mut connection = pool.get()?;
        let partnerstatus = calculate_partnerstatus(&mut connection, username.clone()).unwrap();

        let gemeinsame_buchungen = form
            .iter()
            .map(|gb| gb.to_domain(username.clone(), partnerstatus.zielperson.clone()))
            .collect::<Vec<NeueGemeinsameBuchung>>();

        output_db::insert_new_gemeinsame_buchungen(&mut connection, gemeinsame_buchungen)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(result_success("Buchungen erfolgreich gespeichert")))
}

#[get("/gemeinsame_buchungen")]
pub async fn get_gemeinsame_buchungen(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let users = web::block(move || {
        let mut conn = pool.get()?;
        output_db::find_all_gemeinsame_buchungen(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    let dtos = users
        .iter()
        .map(GemeinsameBuchung::to_dto)
        .collect::<Vec<GemeinsameBuchungDto>>();
    Ok(HttpResponse::Ok().json(dtos))
}

#[delete("/gemeinsame_buchung/{gemeinsame_buchung_id}")]
pub async fn delete_gemeinsame_buchung(
    pool: web::Data<DbPool>,
    gemeinsame_buchung_id: web::Path<Uuid>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let gemeinsame_buchung_id = gemeinsame_buchung_id.into_inner();
    let _ = web::block(move || {
        let mut conn = pool.get()?;
        output_db::delete_gemeinsame_buchung(&mut conn, user, gemeinsame_buchung_id)
    })
    .await?
    .map_err(error::ErrorInternalServerError);
    Ok(HttpResponse::Ok().json(result_success("Buchung erfolgreicht gelöscht")))
}

#[delete("/gemeinsame_buchungen")]
pub async fn delete_gemeinsame_buchungen(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _result = web::block(move || {
        let mut conn = pool.get()?;
        return output_db::delete_all_gemeinsame_buchungen(&mut conn, user);
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    Ok(HttpResponse::Ok())
}

impl GemeinsameBuchung {
    pub fn to_dto(&self) -> GemeinsameBuchungDto {
        GemeinsameBuchungDto {
            datum: self.datum.to_string(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
            zielperson: self.zielperson.clone(),
        }
    }
}
