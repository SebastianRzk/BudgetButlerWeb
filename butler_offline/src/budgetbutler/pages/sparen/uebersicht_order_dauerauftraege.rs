use crate::budgetbutler::database::select::functions::keyextractors::{
    start_ende_aggregation, StartEndeAggregation,
};
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtOrderDauerauftraegeViewResult {
    pub aktuelle_dauerauftraege: Vec<Indiziert<OrderDauerauftrag>>,
    pub vergangene_dauerauftraege: Vec<Indiziert<OrderDauerauftrag>>,
    pub zukuenftige_dauerauftraege: Vec<Indiziert<OrderDauerauftrag>>,
    pub database_version: DatabaseVersion,
}

pub struct UebersichtOrderDauerauftraegeContext<'a> {
    pub database: &'a Database,
    pub today: Datum,
}

pub fn handle_view(
    context: UebersichtOrderDauerauftraegeContext,
) -> UebersichtOrderDauerauftraegeViewResult {
    let result = context
        .database
        .order_dauerauftraege
        .select()
        .group_as_list_by(start_ende_aggregation(context.today.clone()));

    UebersichtOrderDauerauftraegeViewResult {
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
    use crate::budgetbutler::pages::sparen::uebersicht_order_dauerauftraege::UebersichtOrderDauerauftraegeContext;
    use crate::model::database::order_dauerauftrag::builder::order_dauerauftrag_with_range;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::generate_database_with_order_dauerauftraege;

    #[test]
    pub fn test_handle_view() {
        let heute = Datum::new(1, 1, 2021);
        let vergangener_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2020),
            Datum::new(31, 12, 2020),
            Rhythmus::Halbjaehrlich,
        );
        let aktueller_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2020),
            Datum::new(31, 12, 2024),
            Rhythmus::Halbjaehrlich,
        );
        let zukuenftiger_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2024),
            Datum::new(31, 12, 2024),
            Rhythmus::Halbjaehrlich,
        );

        let database = generate_database_with_order_dauerauftraege(vec![
            aktueller_dauerauftrag,
            vergangener_dauerauftrag,
            zukuenftiger_dauerauftrag,
        ]);

        let result = super::handle_view(UebersichtOrderDauerauftraegeContext {
            database: &database,
            today: heute,
        });

        assert_eq!(result.aktuelle_dauerauftraege.len(), 1);
        assert_eq!(result.vergangene_dauerauftraege.len(), 1);
        assert_eq!(result.zukuenftige_dauerauftraege.len(), 1);
    }
}
