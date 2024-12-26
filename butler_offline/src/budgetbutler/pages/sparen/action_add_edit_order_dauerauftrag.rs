use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_ADD;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::state::non_persistent_application_state::OrderDauerauftragChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::order_dauerauftraege::OrderDauerauftraege;

pub struct SubmitOrderDauerauftragContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
    pub rhythmus: Rhythmus,
}

pub fn submit_order_dauerauftrag(
    context: SubmitOrderDauerauftragContext,
) -> RedirectResult<OrderDauerauftragChange> {
    let buchung = OrderDauerauftrag {
        name: context.name.clone(),
        konto: context.konto.clone(),
        depotwert: context.depotwert.clone(),
        wert: context.wert.clone(),
        start_datum: context.start_datum.clone(),
        ende_datum: context.ende_datum.clone(),
        rhythmus: context.rhythmus.clone(),
    };
    let neue_order_dauerauftraege: OrderDauerauftraege;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_order_dauerauftraege = context
            .database
            .order_dauerauftraege
            .change()
            .edit(index, buchung.clone())
    } else {
        icon = PLUS;
        neue_order_dauerauftraege = context
            .database
            .order_dauerauftraege
            .change()
            .insert(buchung.clone())
    }

    let new_database = context
        .database
        .change_order_dauerauftraege(neue_order_dauerauftraege);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_ORDERDAUERAUFTRAG_ADD.to_string(),
            },
        },
        change: OrderDauerauftragChange {
            icon,
            name: buchung.name.clone(),
            konto: buchung.konto.clone(),
            depotwert: buchung.depotwert.clone(),
            wert: buchung.wert.clone(),
            start_datum: buchung.start_datum.clone(),
            ende_datum: buchung.ende_datum.clone(),
            rhythmus: buchung.rhythmus.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_order_dauerauftrag::SubmitOrderDauerauftragContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::builder::demo_order_betrag;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_order_dauerauftrag() {
        let database = generate_empty_database();

        let result = super::submit_order_dauerauftrag(SubmitOrderDauerauftragContext {
            database: &database,
            edit_index: None,
            name: demo_name(),
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
            start_datum: demo_datum(),
            ende_datum: demo_datum(),
            rhythmus: Rhythmus::Monatlich,
        });

        assert_eq!(
            result
                .result
                .changed_database
                .order_dauerauftraege
                .select()
                .count(),
            1
        );
        assert_eq!(
            result
                .result
                .changed_database
                .order_dauerauftraege
                .get(0)
                .value,
            OrderDauerauftrag {
                name: demo_name(),
                konto: demo_konto_referenz(),
                depotwert: demo_depotwert_referenz(),
                wert: demo_order_betrag(),
                start_datum: demo_datum(),
                ende_datum: demo_datum(),
                rhythmus: Rhythmus::Monatlich,
            }
        );

        assert_eq!(result.change.icon, PLUS);
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.konto, demo_konto_referenz());
        assert_eq!(result.change.depotwert, demo_depotwert_referenz());
        assert_eq!(result.change.wert, demo_order_betrag());
        assert_eq!(result.change.start_datum, demo_datum());
        assert_eq!(result.change.ende_datum, demo_datum());
        assert_eq!(result.change.rhythmus, Rhythmus::Monatlich);
    }
}
