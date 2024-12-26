use serde::Serialize;

use crate::database::DbPool;
use crate::kategorien::output_db;
use actix_web::{delete, error, get, post, web, HttpResponse, Responder};
use uuid::Uuid;

use crate::kategorien::model::{Kategorie, NeueKategorie};
use crate::user::model::User;

#[derive(Debug, Clone, Serialize)]
pub struct KategorieDto {
    pub id: String,
    pub name: String,
    pub user: String,
}

#[post("/kategorien")]
pub async fn add_kategorie(
    pool: web::Data<DbPool>,
    form: web::Json<String>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let einzelbuchung = web::block(move || {
        let mut conn = pool.get()?;
        output_db::insert_new_kategorie(
            &mut conn,
            NeueKategorie {
                name: form.into_inner(),
                user: username,
            },
        )
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(einzelbuchung.to_dto()))
}

#[post("/kategorien/batch")]
pub async fn add_kategorien(
    pool: web::Data<DbPool>,
    form: web::Json<Vec<String>>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let username: String = user.sub;
    let kategorien = form
        .iter()
        .map(|k| NeueKategorie {
            name: k.clone(),
            user: username.clone(),
        })
        .collect::<Vec<NeueKategorie>>();
    let gespeicherte_kategorien = web::block(move || {
        let mut conn = pool.get()?;
        output_db::insert_new_kategorien(&mut conn, kategorien)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;

    Ok(HttpResponse::Created().json(
        gespeicherte_kategorien
            .iter()
            .map(Kategorie::to_dto)
            .collect::<Vec<KategorieDto>>(),
    ))
}

#[get("/kategorien")]
pub async fn get_kategorien(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let users = web::block(move || {
        let mut conn = pool.get()?;
        output_db::find_all_kategorien(&mut conn, user)
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    let dtos = users
        .iter()
        .map(Kategorie::to_dto)
        .collect::<Vec<KategorieDto>>();
    Ok(HttpResponse::Ok().json(dtos))
}

#[delete("/kategorie/{kategorie_id}")]
pub async fn delete_kategorie(
    pool: web::Data<DbPool>,
    kategorie_id: web::Path<Uuid>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let kategorie_id = kategorie_id.into_inner();
    let _ = web::block(move || {
        let mut conn = pool.get()?;
        output_db::delete_kategorie(&mut conn, user, kategorie_id)
    })
    .await?
    .map_err(error::ErrorInternalServerError);
    Ok(HttpResponse::Ok())
}

#[delete("/kategorien")]
pub async fn delete_kategorien(
    pool: web::Data<DbPool>,
    user: User,
) -> actix_web::Result<impl Responder> {
    let user: String = user.sub;
    let _result = web::block(move || {
        let mut conn = pool.get()?;
        return output_db::delete_all_kategorien(&mut conn, user);
    })
    .await?
    .map_err(error::ErrorInternalServerError)?;
    Ok(HttpResponse::Ok())
}

impl Kategorie {
    pub fn to_dto(&self) -> KategorieDto {
        KategorieDto {
            name: self.name.clone(),
            user: self.user.clone(),
            id: self.id.clone(),
        }
    }
}
