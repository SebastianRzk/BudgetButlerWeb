use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_SPARKONTO_UEBERSICHT;
use crate::model::state::non_persistent_application_state::KontoChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_sparkonto(context: DeleteContext) -> RedirectResult<KontoChange> {
    let to_delete = context.database.sparkontos.get(context.delete_index);

    let neue_sparkontos = context
        .database
        .sparkontos
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_sparkontos(neue_sparkontos),
            target: Redirect {
                target: SPAREN_SPARKONTO_UEBERSICHT.to_string(),
            },
        },
        change: KontoChange {
            icon: DELETE.as_fa.to_string(),
            name: to_delete.value.name.clone(),
            typ: to_delete.value.kontotyp.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparkontos;

    #[test]
    fn test_delete_dauerauftrag() {
        let database = generate_database_with_sparkontos(vec![demo_konto()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_sparkonto(context);

        assert_eq!(
            result.result.changed_database.sparkontos.select().count(),
            0
        );
        assert_eq!(result.change.icon, DELETE.as_fa.to_string());
        assert_eq!(result.change.name, demo_konto().name);
        assert_eq!(result.change.typ, demo_konto().kontotyp);
    }
}
