use crate::core::rhythmus::rhythmus_from_string;
use crate::database::DbError;
use bigdecimal::BigDecimal;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use time::Date;
use uuid::Uuid;

use crate::gemeinsame_dauerauftraege::model::{
    GemeinsamerDauerauftrag, NeuerGemeinsamerDauerauftrag,
};
use crate::schema::gemeinsame_dauerauftraege;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = gemeinsame_dauerauftraege)]
pub struct GemeinsamerDauerauftragEntity {
    pub id: String,
    pub name: String,
    pub start_datum: Date,
    pub ende_datum: Date,
    pub kategorie: String,
    pub wert: BigDecimal,
    pub user: String,
    pub rhythmus: String,
    pub letzte_ausfuehrung: Option<Date>,
    pub zielperson: String,
}

impl NeuerGemeinsamerDauerauftrag {
    pub fn to_entity(self, id: String) -> GemeinsamerDauerauftragEntity {
        GemeinsamerDauerauftragEntity {
            id,
            name: self.name.clone(),
            kategorie: self.kategorie.clone(),
            wert: self.wert,
            start_datum: self.start_datum,
            ende_datum: self.ende_datum,
            rhythmus: self.rhythmus.to_string(),
            user: self.user.clone(),
            letzte_ausfuehrung: None,
            zielperson: self.zielperson.clone(),
        }
    }
}

impl GemeinsamerDauerauftragEntity {
    pub fn to_domain(&self) -> GemeinsamerDauerauftrag {
        GemeinsamerDauerauftrag {
            id: self.id.clone(),
            kategorie: self.kategorie.clone(),
            name: self.name.clone(),
            wert: self.wert.clone(),
            start_datum: self.start_datum,
            ende_datum: self.ende_datum,
            rhythmus: rhythmus_from_string(self.rhythmus.clone()).unwrap(),
            letzte_ausfuehrung: self.letzte_ausfuehrung,
            user: self.user.clone(),
            zielperson: self.zielperson.clone(),
        }
    }
}

impl GemeinsamerDauerauftrag {
    pub fn to_entity(&self) -> GemeinsamerDauerauftragEntity {
        GemeinsamerDauerauftragEntity {
            id: self.id.clone(),
            ende_datum: self.ende_datum.clone(),
            start_datum: self.start_datum.clone(),
            rhythmus: self.rhythmus.to_string(),
            user: self.user.clone(),
            kategorie: self.kategorie.clone(),
            wert: self.wert.clone(),
            name: self.name.clone(),
            letzte_ausfuehrung: self.letzte_ausfuehrung,
            zielperson: self.zielperson.clone(),
        }
    }
}

pub fn finde_alle_gemeinsame_dauerauftraege(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<Vec<GemeinsamerDauerauftrag>, DbError> {
    use crate::schema::gemeinsame_dauerauftraege::dsl::*;

    let alle_dauerauftraege = gemeinsame_dauerauftraege
        .filter(user.eq(user_name))
        .order(start_datum.asc())
        .get_results(conn);

    Ok(alle_dauerauftraege
        .unwrap()
        .iter()
        .map(GemeinsamerDauerauftragEntity::to_domain)
        .collect::<Vec<GemeinsamerDauerauftrag>>())
}

pub fn insert_neuer_gemeinsamer_dauerauftrag(
    conn: &mut MysqlConnection,
    neuer_dauerauftrag: NeuerGemeinsamerDauerauftrag,
) -> Result<GemeinsamerDauerauftrag, DbError> {
    use crate::schema::gemeinsame_dauerauftraege::dsl::*;

    let neuer_dauerauftrag_entity = neuer_dauerauftrag.to_entity(Uuid::new_v4().to_string());

    diesel::insert_into(gemeinsame_dauerauftraege)
        .values(&neuer_dauerauftrag_entity)
        .execute(conn)?;

    Ok(neuer_dauerauftrag_entity.to_domain())
}

pub fn aktualisiere_letzte_ausfuehrung(
    conn: &mut MysqlConnection,
    uid: String,
    letzte_ausfuehrung_value: Date,
) -> Result<String, DbError> {
    use crate::schema::gemeinsame_dauerauftraege::dsl::*;

    diesel::update(gemeinsame_dauerauftraege.filter(id.eq(uid.clone())))
        .set(letzte_ausfuehrung.eq(Some(letzte_ausfuehrung_value)))
        .execute(conn)?;

    Ok(uid)
}

pub struct DeleteResult {}

pub fn delete_dauerauftrag(
    conn: &mut MysqlConnection,
    user_name: String,
    uuid: Uuid,
) -> Result<DeleteResult, DbError> {
    use crate::schema::gemeinsame_dauerauftraege::dsl::*;

    diesel::delete(gemeinsame_dauerauftraege)
        .filter(user.eq(user_name))
        .filter(id.eq(uuid.to_string()))
        .execute(conn)?;

    Ok(DeleteResult {})
}
