use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_ORDER_UEBERSICHT;
use crate::model::state::non_persistent_application_state::OrderChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_order(context: DeleteContext) -> RedirectResult<OrderChange> {
    let to_delete = context.database.order.get(context.delete_index);

    let neue_order = context.database.order.change().delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_order(neue_order),
            target: Redirect {
                target: SPAREN_ORDER_UEBERSICHT.to_string(),
            },
        },
        change: OrderChange {
            icon: DELETE,
            name: to_delete.value.name.clone(),
            datum: to_delete.value.datum,
            konto: to_delete.value.konto.clone(),
            depotwert: to_delete.value.depotwert.clone(),
            wert: to_delete.value.wert.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::order::builder::any_order;
    use crate::model::state::persistent_application_state::builder::generate_database_with_orders;

    #[test]
    fn test_delete_order() {
        let database = generate_database_with_orders(vec![any_order()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_order(context);

        assert_eq!(result.result.changed_database.order.select().count(), 0);
        assert_eq!(result.change.icon, DELETE);
        assert_eq!(result.change.name, any_order().name);
        assert_eq!(result.change.datum, any_order().datum);
        assert_eq!(result.change.konto, any_order().konto);
        assert_eq!(result.change.depotwert, any_order().depotwert);
        assert_eq!(result.change.wert, any_order().wert);
    }
}
