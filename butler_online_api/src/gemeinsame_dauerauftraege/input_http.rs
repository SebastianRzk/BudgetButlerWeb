use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use bigdecimal::BigDecimal;
use serde::{Deserialize, Serialize};
use time::macros::format_description;
use time::Date;
use uuid::Uuid;

use crate::core::rhythmus::rhythmus_from_string;
use crate::database::DbPool;
use crate::gemeinsame_dauerauftraege::model::{
    GemeinsamerDauerauftrag, NeuerGemeinsamerDauerauftrag,
};
use crate::gemeinsame_dauerauftraege::output_db;
use crate::result_dto::result_success;
use crate::user::model::User;
use crate::wiederkehrend::gemeinsame_buchung;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct NeuerGemeinsamerDauerauftragDto {
    pub name: String,
    pub kategorie: String,
    pub start_datum: String,
    pub ende_datum: String,
    pub rhythmus: String,
    pub wert: BigDecimal,
    pub eigene_buchung: bool,
}

impl NeuerGemeinsamerDauerauftragDto {
    pub fn to_domain(&self, user: String, partnerperson: String) -> NeuerGemeinsamerDauerauftrag {
        let mut zielperson: String = user.clone();
        if !self.eigene_buchung.clone() {
            zielperson = partnerperson
        }

        NeuerGemeinsamerDauerauftrag {
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            start_datum: Date::parse(
                self.start_datum.as_str(),
                format_description!("[year]-[month]-[day]"),
            )
            .unwrap(),
            ende_datum: Date::parse(
                self.ende_datum.as_str(),
                format_description!("[year]-[month]-[day]"),
            )
            .unwrap(),
            rhythmus: rhythmus_from_string(self.rhythmus.to_string()).unwrap(),
            zielperson,
            user,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct GemeinsamerDauerauftragDto {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: String,
    pub ende_datum: String,
    pub rhythmus: String,
    pub user: String,
    pub zielperson: String,
}

impl GemeinsamerDauerauftrag {
    pub fn to_dto(&self) -> GemeinsamerDauerauftragDto {
        GemeinsamerDauerauftragDto {
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            start_datum: self.start_datum.to_string(),
            ende_datum: self.ende_datum.to_string(),
            rhythmus: self.rhythmus.to_string(),
            user: self.user.clone(),
            zielperson: self.zielperson.clone(),
        }
    }
}

#[post("/gemeinsamer_dauerauftrag")]
pub async fn add_gemeinsamer_dauerauftrag(
    pool: web::Data<DbPool>,
    form: web::Json<NeuerGemeinsamerDauerauftragDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;

    web::block(move || {
        let mut conn = pool.get()?;
        let partner_configuration =
            crate::partner::output_db::calculate_partnerstatus(&mut conn, user.clone()).unwrap();
        let dauerauftrag = output_db::insert_neuer_gemeinsamer_dauerauftrag(
            &mut conn,
            form.to_domain(user, partner_configuration.zielperson),
        );
        gemeinsame_buchung::verarbeite_gemeinsame_buchung_dauerauftrag(
            &mut conn,
            &dauerauftrag.as_ref().unwrap(),
        );
        dauerauftrag
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(result_success(
        "Gemeinsamer Dauerauftrag erfolgreich gespeichert",
    )))
}

#[get("/gemeinsame_dauerauftraege")]
pub async fn get_gemeinsame_dauerauftraege(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    eprintln!("rufe daten ab für {:?}", user.clone());
    let users = web::block(move || {
        let mut conn = pool.get()?;
        output_db::finde_alle_gemeinsame_dauerauftraege(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    let dtos = users
        .iter()
        .map(GemeinsamerDauerauftrag::to_dto)
        .collect::<Vec<GemeinsamerDauerauftragDto>>();
    Ok(HttpResponse::Ok().json(dtos))
}

#[delete("/gemeinsamer_dauerauftrag/{dauerauftrag_id}")]
pub async fn delete_gemeinsamer_dauerauftrag(
    pool: web::Data<DbPool>,
    dauerauftrag_id: web::Path<Uuid>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let dauerauftrag_uid = dauerauftrag_id.into_inner();
    let _ = web::block(move || {
        let mut conn = pool.get()?;
        output_db::delete_dauerauftrag(&mut conn, user, dauerauftrag_uid)
    })
    .await?
    .map_err(error::ErrorInternalServerError);
    Ok(HttpResponse::Ok().json(result_success(
        "Gemeinsamer Dauerauftrag erfolgreich gelöscht",
    )))
}
