use crate::database::DbError;
use bigdecimal::BigDecimal;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use time::Date;
use uuid::Uuid;

use crate::gemeinsame_buchungen::model::{GemeinsameBuchung, NeueGemeinsameBuchung};
use crate::partner;
use crate::schema::gemeinsame_buchungen;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = gemeinsame_buchungen)]
pub struct GemeinsameBuchungEntity {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
    pub zielperson: String,
}

impl NeueGemeinsameBuchung {
    pub fn to_entity(&self, id: String) -> GemeinsameBuchungEntity {
        GemeinsameBuchungEntity {
            id,
            name: self.name.clone(),
            kategorie: self.kategorie.clone(),
            wert: self.wert.clone(),
            datum: self.datum,
            user: self.user.clone(),
            zielperson: self.zielperson.clone(),
        }
    }
}

impl GemeinsameBuchungEntity {
    pub fn to_domain(&self) -> GemeinsameBuchung {
        GemeinsameBuchung {
            datum: self.datum.clone(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
            zielperson: self.zielperson.clone(),
        }
    }
}

pub fn find_all_gemeinsame_buchungen(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<Vec<GemeinsameBuchung>, DbError> {
    use crate::schema::gemeinsame_buchungen::dsl::*;
    let alle_gemeinsame_buchungen;
    let partnerstatus =
        partner::output_db::calculate_partnerstatus(conn, user_name.clone()).unwrap();

    if partnerstatus.clone().bestaetigt {
        alle_gemeinsame_buchungen = gemeinsame_buchungen
            .filter(
                user.eq(user_name.clone())
                    .or(user.eq(partnerstatus.zielperson)),
            )
            .order(datum.asc())
            .get_results(conn);
    } else {
        alle_gemeinsame_buchungen = gemeinsame_buchungen
            .filter(user.eq(user_name.clone()))
            .order(datum.asc())
            .get_results(conn);
    }

    Ok(alle_gemeinsame_buchungen
        .unwrap()
        .iter()
        .map(GemeinsameBuchungEntity::to_domain)
        .collect::<Vec<GemeinsameBuchung>>())
}

pub fn insert_new_gemeinsame_buchung(
    conn: &mut MysqlConnection,
    neue_gemeinsame_buchung: NeueGemeinsameBuchung,
) -> Result<GemeinsameBuchung, DbError> {
    use crate::schema::gemeinsame_buchungen::dsl::*;

    let neue_gemeinsame_buchungen_entity =
        neue_gemeinsame_buchung.to_entity(Uuid::new_v4().to_string());

    diesel::insert_into(gemeinsame_buchungen)
        .values(&neue_gemeinsame_buchungen_entity)
        .execute(conn)?;

    Ok(neue_gemeinsame_buchungen_entity.to_domain())
}
pub fn insert_new_gemeinsame_buchungen(
    conn: &mut MysqlConnection,
    neue_gemeinsame_buchungen: Vec<NeueGemeinsameBuchung>,
) -> Result<Vec<GemeinsameBuchung>, DbError> {
    use crate::schema::gemeinsame_buchungen::dsl::*;

    let neue_gemeinsame_buchungen_entity = neue_gemeinsame_buchungen
        .iter()
        .map(|neue_gemeinsame_buchung| {
            neue_gemeinsame_buchung.to_entity(Uuid::new_v4().to_string())
        })
        .collect::<Vec<GemeinsameBuchungEntity>>();

    diesel::insert_into(gemeinsame_buchungen)
        .values(&neue_gemeinsame_buchungen_entity)
        .execute(conn)?;

    Ok(neue_gemeinsame_buchungen_entity
        .iter()
        .map(GemeinsameBuchungEntity::to_domain)
        .collect::<Vec<GemeinsameBuchung>>())
}

pub struct DeleteResult {}

pub fn delete_gemeinsame_buchung(
    conn: &mut MysqlConnection,
    user_name: String,
    uuid: Uuid,
) -> Result<DeleteResult, DbError> {
    use crate::schema::gemeinsame_buchungen::dsl::*;

    let partnerstatus =
        partner::output_db::calculate_partnerstatus(conn, user_name.clone()).unwrap();
    if partnerstatus.clone().bestaetigt {
        diesel::delete(gemeinsame_buchungen)
            .filter(
                user.eq(user_name.clone())
                    .or(user.eq(partnerstatus.zielperson)),
            )
            .filter(id.eq(uuid.to_string()))
            .execute(conn)?;
    } else {
        diesel::delete(gemeinsame_buchungen)
            .filter(user.eq(user_name))
            .filter(id.eq(uuid.to_string()))
            .execute(conn)?;
    }

    Ok(DeleteResult {})
}

pub fn delete_all_gemeinsame_buchungen(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<DeleteResult, DbError> {
    use crate::schema::gemeinsame_buchungen::dsl::*;

    let partnerstatus =
        partner::output_db::calculate_partnerstatus(conn, user_name.clone()).unwrap();
    if partnerstatus.clone().bestaetigt {
        diesel::delete(gemeinsame_buchungen)
            .filter(
                user.eq(user_name.clone())
                    .or(user.eq(partnerstatus.zielperson)),
            )
            .execute(conn)?;
    } else {
        diesel::delete(gemeinsame_buchungen)
            .filter(user.eq(user_name))
            .execute(conn)?;
    }

    Ok(DeleteResult {})
}
