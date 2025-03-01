use crate::database::DbError;
use diesel::prelude::*;
use uuid::Uuid;

use crate::einzelbuchungen::model::{Einzelbuchung, NeueEinzelbuchung};
use crate::einzelbuchungen::output_db::entities::EinzelbuchungEntity;

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
