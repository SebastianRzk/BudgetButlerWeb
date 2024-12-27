use crate::database::DbError;
use bigdecimal::BigDecimal;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use time::Date;
use uuid::Uuid;

use crate::einzelbuchungen::model::{Einzelbuchung, NeueEinzelbuchung};
use crate::schema::einzelbuchungen;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = einzelbuchungen)]
pub struct EinzelbuchungEntity {
    pub id: String,
    pub name: String,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub datum: Date,
    pub user: String,
}

impl NeueEinzelbuchung {
    pub fn to_entity(self, id: String) -> EinzelbuchungEntity {
        EinzelbuchungEntity {
            id,
            name: self.name.clone(),
            kategorie: self.kategorie.clone(),
            wert: self.wert,
            datum: self.datum,
            user: self.user.clone(),
        }
    }
}

impl EinzelbuchungEntity {
    pub fn to_domain(&self) -> Einzelbuchung {
        Einzelbuchung {
            datum: self.datum.clone(),
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            user: self.user.clone(),
        }
    }
}

pub fn find_all_einzelbuchungen(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<Vec<Einzelbuchung>, DbError> {
    use crate::schema::einzelbuchungen::dsl::*;

    let alle_einzelbuchungen = einzelbuchungen
        .filter(user.eq(user_name))
        .order(datum.asc())
        .get_results(conn);

    Ok(alle_einzelbuchungen
        .unwrap()
        .iter()
        .map(EinzelbuchungEntity::to_domain)
        .collect::<Vec<Einzelbuchung>>())
}

pub fn insert_new_einzelbuchung(
    conn: &mut MysqlConnection,
    neue_einzelbuchung: NeueEinzelbuchung,
) -> Result<Einzelbuchung, DbError> {
    use crate::schema::einzelbuchungen::dsl::*;

    let neue_einzelbuchung_entity = neue_einzelbuchung.to_entity(Uuid::new_v4().to_string());

    diesel::insert_into(einzelbuchungen)
        .values(&neue_einzelbuchung_entity)
        .execute(conn)?;

    Ok(neue_einzelbuchung_entity.to_domain())
}

pub struct DeleteResult {}

pub fn delete_einzelbuchung(
    conn: &mut MysqlConnection,
    user_name: String,
    uuid: Uuid,
) -> Result<DeleteResult, DbError> {
    use crate::schema::einzelbuchungen::dsl::*;

    diesel::delete(einzelbuchungen)
        .filter(user.eq(user_name))
        .filter(id.eq(uuid.to_string()))
        .execute(conn)?;

    Ok(DeleteResult {})
}

pub fn delete_all_einzelbuchungen(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<DeleteResult, DbError> {
    use crate::schema::einzelbuchungen::dsl::*;

    diesel::delete(einzelbuchungen)
        .filter(user.eq(user_name))
        .execute(conn)?;

    Ok(DeleteResult {})
}
