use crate::budgetbutler::database::select::functions::keyextractors::{
    start_ende_aggregation, StartEndeAggregation,
};
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtDauerauftraegeViewResult {
    pub aktuelle_dauerauftraege: Vec<Indiziert<Dauerauftrag>>,
    pub vergangene_dauerauftraege: Vec<Indiziert<Dauerauftrag>>,
    pub zukuenftige_dauerauftraege: Vec<Indiziert<Dauerauftrag>>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtDauerauftraegeContext<'a> {
    pub database: &'a Database,
    pub today: Datum,
}

pub fn handle_view(context: UebersichtDauerauftraegeContext) -> UebersichtDauerauftraegeViewResult {
    let result = context
        .database
        .dauerauftraege
        .select()
        .group_as_list_by(start_ende_aggregation(context.today.clone()));

    UebersichtDauerauftraegeViewResult {
        aktuelle_dauerauftraege: result
            .get(&StartEndeAggregation::Aktuelle)
            .unwrap_or(&vec![])
            .clone(),
        vergangene_dauerauftraege: result
            .get(&StartEndeAggregation::Vergangene)
            .unwrap_or(&vec![])
            .clone(),
        zukuenftige_dauerauftraege: result
            .get(&StartEndeAggregation::Zukuenftige)
            .unwrap_or(&vec![])
            .clone(),
        database_version: context.database.db_version.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_dauerauftraege::{
        handle_view, UebersichtDauerauftraegeContext,
    };
    use crate::model::database::dauerauftrag::builder::dauerauftrag_mit_start_ende_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_application_state::builder::generate_database_with_dauerauftraege;

    #[test]
    pub fn test_handle_view() {
        let heute = Datum::new(1, 1, 2021);
        let vergangener_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2020), Datum::new(31, 12, 2020));
        let aktueller_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2020), Datum::new(31, 12, 2024));
        let zukuenftiger_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2024), Datum::new(31, 12, 2024));

        let database = generate_database_with_dauerauftraege(vec![
            aktueller_dauerauftrag,
            vergangener_dauerauftrag,
            zukuenftiger_dauerauftrag,
        ]);

        let result = handle_view(UebersichtDauerauftraegeContext {
            database: &database,
            today: heute,
        });

        assert_eq!(result.aktuelle_dauerauftraege.len(), 1);
        assert_eq!(result.vergangene_dauerauftraege.len(), 1);
        assert_eq!(result.zukuenftige_dauerauftraege.len(), 1);
    }
}
