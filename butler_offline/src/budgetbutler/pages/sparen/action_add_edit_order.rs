use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_ORDER_ADD;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::order::Order;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::primitives::order_betrag::OrderBetrag;
use crate::model::state::non_persistent_application_state::OrderChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::order::Orders;

pub struct SubmitOrderContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub datum: Datum,
    pub name: Name,
    pub konto: KontoReferenz,
    pub depotwert: DepotwertReferenz,
    pub wert: OrderBetrag,
}

pub fn submit_order(context: SubmitOrderContext) -> RedirectResult<OrderChange> {
    let buchung = Order {
        name: context.name.clone(),
        konto: context.konto.clone(),
        depotwert: context.depotwert.clone(),
        wert: context.wert.clone(),
        datum: context.datum.clone(),
    };
    let neue_orders: Orders;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_orders = context.database.order.change().edit(index, buchung.clone())
    } else {
        icon = PLUS;
        neue_orders = context.database.order.change().insert(buchung.clone())
    }

    let new_database = context.database.change_order(neue_orders);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: SPAREN_ORDER_ADD.to_string(),
            },
        },
        change: OrderChange {
            icon,
            name: buchung.name.clone(),
            konto: buchung.konto.clone(),
            depotwert: buchung.depotwert.clone(),
            wert: buchung.wert.clone(),
            datum: buchung.datum.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_order::SubmitOrderContext;
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::builder::demo_order_betrag;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_order() {
        let database = generate_empty_database();

        let result = super::submit_order(SubmitOrderContext {
            database: &database,
            edit_index: None,
            name: demo_name(),
            konto: demo_konto_referenz(),
            depotwert: demo_depotwert_referenz(),
            wert: demo_order_betrag(),
            datum: demo_datum(),
        });

        assert_eq!(result.result.changed_database.order.select().count(), 1);
        assert_eq!(
            result.result.changed_database.order.get(0).value,
            Order {
                name: demo_name(),
                konto: demo_konto_referenz(),
                depotwert: demo_depotwert_referenz(),
                wert: demo_order_betrag(),
                datum: demo_datum(),
            }
        );

        assert_eq!(result.change.icon, PLUS);
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.konto, demo_konto_referenz());
        assert_eq!(result.change.depotwert, demo_depotwert_referenz());
        assert_eq!(result.change.wert, demo_order_betrag());
        assert_eq!(result.change.datum, demo_datum());
    }
}
