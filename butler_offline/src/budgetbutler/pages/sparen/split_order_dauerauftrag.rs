use crate::budgetbutler::database::reader::rhythmus::get_monatsdelta_for_rhythmus;
use crate::model::metamodel::datum_selektion::DatumSelektion;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct SplitOrderDauerauftragViewResult {
    pub database_version: DatabaseVersion,
    pub order_dauerauftrag_id: u32,
    pub wert: BetragOhneVorzeichen,
    pub datum: Vec<DatumSelektion>,
}

pub struct SplitOrderDauerauftragContext<'a> {
    pub database: &'a Database,
    pub order_dauerauftrag_id: u32,
}

pub fn handle_split_order_dauerauftrag(
    context: SplitOrderDauerauftragContext,
) -> SplitOrderDauerauftragViewResult {
    let selected_dauerauftrag = context
        .database
        .order_dauerauftraege
        .get(context.order_dauerauftrag_id);
    let mut laufdatum = selected_dauerauftrag.value.start_datum.clone();

    let mut datum = Vec::new();

    while laufdatum <= selected_dauerauftrag.value.ende_datum.clone() {
        let can_be_chosen = laufdatum != selected_dauerauftrag.value.start_datum.clone();
        datum.push(DatumSelektion {
            datum: laufdatum.clone(),
            can_be_chosen,
        });
        laufdatum = laufdatum.add_months(get_monatsdelta_for_rhythmus(
            selected_dauerauftrag.value.rhythmus,
        ));
    }

    if datum.len() > 1 {
        let letztes_datum = datum.pop().unwrap();
        datum.push(DatumSelektion {
            datum: letztes_datum.datum,
            can_be_chosen: false,
        });
    }

    SplitOrderDauerauftragViewResult {
        database_version: context.database.db_version.clone(),
        order_dauerauftrag_id: context.order_dauerauftrag_id,
        wert: selected_dauerauftrag.value.wert.get_realer_wert().clone(),
        datum,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::split_order_dauerauftrag::handle_split_order_dauerauftrag;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::database::order::OrderTyp::Verkauf;
    use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::primitives::rhythmus::Rhythmus::Monatlich;
    use crate::model::state::persistent_application_state::builder::generate_database_with_order_dauerauftraege;

    #[test]
    pub fn test_handle_split() {
        let database = generate_database_with_order_dauerauftraege(vec![OrderDauerauftrag {
            start_datum: Datum::new(1, 1, 2021),
            ende_datum: Datum::new(2, 4, 2021),
            wert: OrderBetrag::new(u_zwei(), Verkauf),
            konto: demo_konto().as_reference(),
            depotwert: any_depotwert().as_referenz(),
            rhythmus: Monatlich,
            name: demo_name(),
        }]);

        let result = handle_split_order_dauerauftrag(super::SplitOrderDauerauftragContext {
            database: &database,
            order_dauerauftrag_id: 1,
        });

        assert_eq!(result.wert, u_zwei());
        assert_eq!(result.datum.len(), 4);
        assert_eq!(result.datum[0].can_be_chosen, false);
        assert_eq!(result.datum[0].datum, Datum::new(1, 1, 2021));
        assert_eq!(result.datum[1].can_be_chosen, true);
        assert_eq!(result.datum[1].datum, Datum::new(1, 2, 2021));
        assert_eq!(result.datum[2].can_be_chosen, true);
        assert_eq!(result.datum[2].datum, Datum::new(1, 3, 2021));
        assert_eq!(result.datum[3].can_be_chosen, false);
        assert_eq!(result.datum[3].datum, Datum::new(1, 4, 2021));
    }
}
