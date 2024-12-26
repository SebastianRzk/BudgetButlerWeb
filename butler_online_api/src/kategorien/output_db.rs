use crate::database::DbError;
use diesel::prelude::*;
use serde::{Deserialize, Serialize};
use uuid::Uuid;

use crate::kategorien::model::{Kategorie, NeueKategorie};
use crate::schema::kategorien;

#[derive(Debug, Clone, Serialize, Deserialize, Queryable, Insertable)]
#[diesel(table_name = kategorien)]
pub struct KategorieEntity {
    pub id: String,
    pub name: String,
    pub user: String,
}

impl NeueKategorie {
    pub fn to_entity(&self, id: String) -> KategorieEntity {
        KategorieEntity {
            id,
            name: self.name.clone(),
            user: self.user.clone(),
        }
    }
}

impl KategorieEntity {
    pub fn to_domain(&self) -> Kategorie {
        Kategorie {
            id: self.id.clone(),
            name: self.name.clone(),
            user: self.user.clone(),
        }
    }
}

pub fn find_all_kategorien(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<Vec<Kategorie>, DbError> {
    use crate::schema::kategorien::dsl::*;

    let alle_kategorien = kategorien
        .filter(user.eq(user_name))
        .order(name.asc())
        .get_results(conn);

    Ok(alle_kategorien
        .unwrap()
        .iter()
        .map(KategorieEntity::to_domain)
        .collect::<Vec<Kategorie>>())
}

pub fn insert_new_kategorie(
    conn: &mut MysqlConnection,
    neue_kategorie: NeueKategorie,
) -> Result<Kategorie, DbError> {
    use crate::schema::kategorien::dsl::*;

    let kategorie_entity = neue_kategorie.to_entity(Uuid::new_v4().to_string());

    diesel::insert_into(kategorien)
        .values(&kategorie_entity)
        .execute(conn)?;

    Ok(kategorie_entity.to_domain())
}

pub fn insert_new_kategorien(
    conn: &mut MysqlConnection,
    neue_kategorien: Vec<NeueKategorie>,
) -> Result<Vec<Kategorie>, DbError> {
    use crate::schema::kategorien::dsl::*;

    let neue_kategorien_entity = neue_kategorien
        .iter()
        .map(|k| k.to_entity(Uuid::new_v4().to_string()))
        .collect::<Vec<KategorieEntity>>();

    diesel::insert_into(kategorien)
        .values(&neue_kategorien_entity)
        .execute(conn)?;

    Ok(neue_kategorien_entity
        .iter()
        .map(KategorieEntity::to_domain)
        .collect::<Vec<Kategorie>>())
}

pub struct DeleteResult {}

pub fn delete_kategorie(
    conn: &mut MysqlConnection,
    user_name: String,
    uuid: Uuid,
) -> Result<DeleteResult, DbError> {
    use crate::schema::kategorien::dsl::*;

    diesel::delete(kategorien)
        .filter(user.eq(user_name))
        .filter(id.eq(uuid.to_string()))
        .execute(conn)?;

    Ok(DeleteResult {})
}

pub fn delete_all_kategorien(
    conn: &mut MysqlConnection,
    user_name: String,
) -> Result<DeleteResult, DbError> {
    use crate::schema::kategorien::dsl::*;

    diesel::delete(kategorien)
        .filter(user.eq(user_name))
        .execute(conn)?;

    Ok(DeleteResult {})
}
