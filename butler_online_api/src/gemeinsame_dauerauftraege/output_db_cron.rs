use crate::database::DbError;
use diesel::prelude::*;

use crate::gemeinsame_dauerauftraege::model::GemeinsamerDauerauftrag;
use crate::gemeinsame_dauerauftraege::output_db::GemeinsamerDauerauftragEntity;

pub fn finde_alle_gemeinsame_dauerauftraege_without_user(
    conn: &mut MysqlConnection,
) -> Result<Vec<GemeinsamerDauerauftrag>, DbError> {
    use crate::schema::gemeinsame_dauerauftraege::dsl::*;

    let alle_dauerauftraege = gemeinsame_dauerauftraege.get_results(conn);

    Ok(alle_dauerauftraege
        .unwrap()
        .iter()
        .map(GemeinsamerDauerauftragEntity::to_domain)
        .collect::<Vec<GemeinsamerDauerauftrag>>())
}
