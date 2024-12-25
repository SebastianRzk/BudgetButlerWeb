use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_DEPOTWERTE_UEBERSICHT;
use crate::model::state::non_persistent_application_state::DepotwertChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_depotwert(context: DeleteContext) -> RedirectResult<DepotwertChange> {
    let to_delete = context.database.depotwerte.get(context.delete_index);

    let neue_depotwerte = context
        .database
        .depotwerte
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_depotwerte(neue_depotwerte),
            target: Redirect {
                target: SPAREN_DEPOTWERTE_UEBERSICHT.to_string(),
            },
        },
        change: DepotwertChange {
            icon: DELETE,
            name: to_delete.value.name.clone(),
            typ: to_delete.value.typ.clone(),
            isin: to_delete.value.isin.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::state::persistent_application_state::builder::generate_database_with_depotwerte;

    #[test]
    fn test_delete_depotwert() {
        let database = generate_database_with_depotwerte(vec![any_depotwert()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_depotwert(context);

        assert_eq!(
            result.result.changed_database.sparkontos.select().count(),
            0
        );
        assert_eq!(result.change.icon, DELETE);
        assert_eq!(result.change.name, any_depotwert().name);
        assert_eq!(result.change.typ, any_depotwert().typ);
        assert_eq!(result.change.isin, any_depotwert().isin);
    }
}
