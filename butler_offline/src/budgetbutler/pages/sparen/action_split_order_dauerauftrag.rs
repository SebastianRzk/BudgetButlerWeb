use crate::budgetbutler::view::icons::GEAR;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::state::non_persistent_application_state::OrderDauerauftragChange;
use crate::model::state::persistent_application_state::Database;

pub struct ActionSplitOrderDauerauftragContext<'a> {
    pub database: &'a Database,
    pub order_dauerauftrag_id: u32,
    pub betrag: BetragOhneVorzeichen,
    pub erste_neue_buchung: Datum,
}

pub fn submit_split_order_dauerauftrag(
    context: ActionSplitOrderDauerauftragContext,
) -> RedirectResult<OrderDauerauftragChange> {
    let to_change = context
        .database
        .order_dauerauftraege
        .get(context.order_dauerauftrag_id);

    let letzter_buchungstag = context.erste_neue_buchung.ziehe_einen_tag_ab();

    let geaenderter_dauerauftrag = OrderDauerauftrag {
        start_datum: to_change.value.start_datum.clone(),
        konto: to_change.value.konto.clone(),
        depotwert: to_change.value.depotwert.clone(),
        ende_datum: letzter_buchungstag,
        name: to_change.value.name.clone(),
        wert: to_change.value.wert.clone(),
        rhythmus: to_change.value.rhythmus.clone(),
    };

    let mut neue_order_dauerauftraege = context
        .database
        .order_dauerauftraege
        .change()
        .edit(context.order_dauerauftrag_id, geaenderter_dauerauftrag);

    let neuer_order_dauerauftrag = OrderDauerauftrag {
        start_datum: context.erste_neue_buchung.clone(),
        ende_datum: to_change.value.ende_datum.clone(),
        name: to_change.value.name.clone(),
        wert: OrderBetrag::new(context.betrag.clone(), to_change.value.wert.get_typ()),
        konto: to_change.value.konto.clone(),
        depotwert: to_change.value.depotwert.clone(),
        rhythmus: to_change.value.rhythmus.clone(),
    };

    neue_order_dauerauftraege = neue_order_dauerauftraege
        .change()
        .insert(neuer_order_dauerauftrag);

    RedirectResult {
        result: ModificationResult {
            changed_database: context
                .database
                .change_order_dauerauftraege(neue_order_dauerauftraege),
            target: Redirect {
                target: SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT.to_string(),
            },
        },
        change: OrderDauerauftragChange {
            icon: GEAR,
            start_datum: to_change.value.start_datum.clone(),
            ende_datum: to_change.value.ende_datum.clone(),
            name: to_change.value.name.clone(),
            wert: to_change.value.wert.clone(),
            konto: to_change.value.konto.clone(),
            depotwert: to_change.value.depotwert.clone(),
            rhythmus: to_change.value.rhythmus.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::action_split_dauerauftrag::{
        submit_split_dauerauftrag, ActionSplitDauerauftragContext,
    };
    use crate::model::database::dauerauftrag::Dauerauftrag;
    use crate::model::eigenschaften::besitzt_start_und_ende_datum::BesitztStartUndEndeDatum;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::rhythmus::Rhythmus::Monatlich;
    use crate::model::state::persistent_application_state::builder::generate_database_with_dauerauftraege;

    #[test]
    fn test_submit_split_dauerauftrag() {
        let database = generate_database_with_dauerauftraege(vec![Dauerauftrag {
            start_datum: Datum::new(1, 1, 2021),
            ende_datum: Datum::new(31, 12, 2022),
            name: demo_name(),
            kategorie: demo_kategorie(),
            betrag: zwei(),
            rhythmus: Monatlich,
        }]);

        let context = ActionSplitDauerauftragContext {
            database: &database,
            dauerauftrag_id: 1,
            betrag: vier(),
            erste_neue_buchung: Datum::new(1, 1, 2022),
        };

        let result = submit_split_dauerauftrag(context);

        let alter_auftrag = result
            .result
            .changed_database
            .dauerauftraege
            .dauerauftraege
            .get(0)
            .unwrap();
        assert_eq!(alter_auftrag.start_datum(), &Datum::new(1, 1, 2021));
        assert_eq!(alter_auftrag.ende_datum(), &Datum::new(31, 12, 2021));
        assert_eq!(alter_auftrag.value.betrag, zwei());
        let neuer_auftrag = result
            .result
            .changed_database
            .dauerauftraege
            .dauerauftraege
            .get(1)
            .unwrap();
        assert_eq!(neuer_auftrag.start_datum(), &Datum::new(1, 1, 2022));
        assert_eq!(neuer_auftrag.ende_datum(), &Datum::new(31, 12, 2022));
        assert_eq!(neuer_auftrag.value.betrag, vier());
    }
}
