use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_ORDERDAUERAUFTRAG_UEBERSICHT;
use crate::model::state::non_persistent_application_state::OrderDauerauftragChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_order_dauerauftrag(
    context: DeleteContext,
) -> RedirectResult<OrderDauerauftragChange> {
    let to_delete = context
        .database
        .order_dauerauftraege
        .get(context.delete_index);

    let neue_order_dauerauftraege = context
        .database
        .order_dauerauftraege
        .change()
        .delete(context.delete_index);

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
            icon: DELETE,
            name: to_delete.value.name.clone(),
            start_datum: to_delete.value.start_datum,
            ende_datum: to_delete.value.ende_datum,
            konto: to_delete.value.konto.clone(),
            depotwert: to_delete.value.depotwert.clone(),
            wert: to_delete.value.wert.clone(),
            rhythmus: to_delete.value.rhythmus.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::order_dauerauftrag::builder::any_order_dauerauftrag;
    use crate::model::state::persistent_application_state::builder::generate_database_with_order_dauerauftraege;

    #[test]
    fn test_delete_order_dauerauftrag() {
        let database = generate_database_with_order_dauerauftraege(vec![any_order_dauerauftrag()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_order_dauerauftrag(context);

        assert_eq!(result.result.changed_database.order.select().count(), 0);
        assert_eq!(result.change.icon, DELETE);
        assert_eq!(result.change.name, any_order_dauerauftrag().name);
        assert_eq!(
            result.change.start_datum,
            any_order_dauerauftrag().start_datum
        );
        assert_eq!(
            result.change.ende_datum,
            any_order_dauerauftrag().ende_datum
        );
        assert_eq!(result.change.konto, any_order_dauerauftrag().konto);
        assert_eq!(result.change.depotwert, any_order_dauerauftrag().depotwert);
        assert_eq!(result.change.wert, any_order_dauerauftrag().wert);
        assert_eq!(result.change.rhythmus, any_order_dauerauftrag().rhythmus);
    }
}
