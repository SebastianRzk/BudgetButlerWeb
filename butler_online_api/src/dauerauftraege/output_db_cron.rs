use crate::database::DbError;
use diesel::prelude::*;

use crate::dauerauftraege::model::Dauerauftrag;
use crate::dauerauftraege::output_db::DauerauftragEntity;

pub fn find_all_dauerauftraege_without_user(
    conn: &mut MysqlConnection,
) -> Result<Vec<Dauerauftrag>, DbError> {
    use crate::schema::dauerauftraege::dsl::*;

    let alle_dauerauftraege = dauerauftraege.get_results(conn);

    Ok(alle_dauerauftraege
        .unwrap()
        .iter()
        .map(DauerauftragEntity::to_domain)
        .collect::<Vec<Dauerauftrag>>())
}
