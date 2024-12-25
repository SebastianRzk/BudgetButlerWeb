use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::SPAREN_SPARBUCHUNGEN_UEBERSICHT;
use crate::model::state::non_persistent_application_state::SparbuchungChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_sparbuchung(context: DeleteContext) -> RedirectResult<SparbuchungChange> {
    let to_delete = context.database.sparbuchungen.get(context.delete_index);

    let neue_sparbuchungen = context
        .database
        .sparbuchungen
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_sparbuchungen(neue_sparbuchungen),
            target: Redirect {
                target: SPAREN_SPARBUCHUNGEN_UEBERSICHT.to_string(),
            },
        },
        change: SparbuchungChange {
            icon: DELETE,
            name: to_delete.value.name.clone(),
            datum: to_delete.value.datum.clone(),
            konto: to_delete.value.konto.clone(),
            typ: to_delete.value.typ.clone(),
            wert: to_delete.value.wert.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::sparbuchung::builder::any_sparbuchung;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparbuchungen;

    #[test]
    fn test_delete_dauerauftrag() {
        let database = generate_database_with_sparbuchungen(vec![any_sparbuchung()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_sparbuchung(context);

        assert_eq!(
            result
                .result
                .changed_database
                .sparbuchungen
                .select()
                .count(),
            0
        );
        assert_eq!(result.change.icon, DELETE);
        assert_eq!(result.change.name, demo_konto().name);
        assert_eq!(result.change.datum, any_sparbuchung().datum);
        assert_eq!(result.change.konto, any_sparbuchung().konto);
        assert_eq!(result.change.typ, any_sparbuchung().typ);
        assert_eq!(result.change.wert, any_sparbuchung().wert);
    }
}
