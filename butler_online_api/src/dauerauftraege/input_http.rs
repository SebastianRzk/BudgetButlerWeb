use crate::core::rhythmus::rhythmus_from_string;
use crate::database::DbPool;
use crate::dauerauftraege::model::{Dauerauftrag, NeuerDauerauftrag};
use crate::dauerauftraege::output_db;
use crate::result_dto::result_success;
use crate::user::model::User;
use crate::wiederkehrend::buchung;
use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use bigdecimal::BigDecimal;
use serde::{Deserialize, Serialize};
use time::macros::format_description;
use time::Date;
use uuid::Uuid;

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct NeuerDauerauftragDto {
    pub name: String,
    pub kategorie: String,
    pub start_datum: String,
    pub ende_datum: String,
    pub rhythmus: String,
    pub wert: BigDecimal,
}

impl NeuerDauerauftragDto {
    pub fn to_domain(&self, user: String) -> NeuerDauerauftrag {
        NeuerDauerauftrag {
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
            user,
        }
    }
}

#[derive(Debug, Clone, Serialize)]
#[serde(rename_all = "camelCase")]
pub struct DauerauftragDto {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub start_datum: String,
    pub ende_datum: String,
    pub rhythmus: String,
    pub user: String,
}

impl Dauerauftrag {
    pub fn to_dto(&self) -> DauerauftragDto {
        DauerauftragDto {
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            start_datum: self.start_datum.to_string(),
            ende_datum: self.ende_datum.to_string(),
            rhythmus: self.rhythmus.to_string(),
            user: self.user.clone(),
        }
    }
}

#[post("/dauerauftrag")]
pub async fn add_dauerauftrag(
    pool: web::Data<DbPool>,
    form: web::Json<NeuerDauerauftragDto>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _dauerauftrag = web::block(move || {
        let mut conn = pool.get()?;
        let dauerauftrag = output_db::insert_new_dauerauftrag(&mut conn, form.to_domain(user));
        buchung::verarbeite_dauerauftrag(&mut conn, &dauerauftrag.as_ref().unwrap());
        dauerauftrag
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(result_success("Dauerauftrag erfolgreich gespeichert")))
}

#[get("/dauerauftraege")]
pub async fn get_dauerauftraege(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    eprintln!("rufe daten ab für {:?}", user.clone());
    let users = web::block(move || {
        let mut conn = pool.get()?;
        output_db::find_all_dauerauftraege(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    let dtos = users
        .iter()
        .map(Dauerauftrag::to_dto)
        .collect::<Vec<DauerauftragDto>>();
    Ok(HttpResponse::Ok().json(dtos))
}

#[delete("/dauerauftrag/{dauerauftrag_id}")]
pub async fn delete_dauerauftrag(
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
    Ok(HttpResponse::Ok().json(result_success("Dauerauftrag erfolgreich gelöscht")))
}
