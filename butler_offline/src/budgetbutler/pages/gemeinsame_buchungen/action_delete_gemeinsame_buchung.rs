use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_UEBERSICHT;
use crate::model::state::non_persistent_application_state::GemeinsameBuchungChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_gemeinsame_buchung(
    context: DeleteContext,
) -> RedirectResult<GemeinsameBuchungChange> {
    let to_delete = context
        .database
        .gemeinsame_buchungen
        .get(context.delete_index);

    let neue_gemeinsame_buchungen = context
        .database
        .gemeinsame_buchungen
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context
                .database
                .change_gemeinsame_buchungen(neue_gemeinsame_buchungen),
            target: Redirect {
                target: GEMEINSAME_BUCHUNGEN_UEBERSICHT.to_string(),
            },
        },
        change: GemeinsameBuchungChange {
            icon: DELETE.as_fa.to_string(),
            datum: to_delete.value.datum.clone(),
            person: to_delete.value.person.clone(),
            name: to_delete.value.name.clone(),
            kategorie: to_delete.value.kategorie.clone(),
            betrag: to_delete.value.betrag,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::gemeinsame_buchung::builder::demo_gemeinsame_buchung;
    use crate::model::state::persistent_application_state::builder::generate_database_with_gemeinsamen_buchungen;

    #[test]
    fn test_delete_dauerauftrag() {
        let database =
            generate_database_with_gemeinsamen_buchungen(vec![demo_gemeinsame_buchung()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_gemeinsame_buchung(context);

        assert_eq!(
            result
                .result
                .changed_database
                .gemeinsame_buchungen
                .select()
                .count(),
            0
        );
        assert_eq!(result.change.icon, DELETE.as_fa.to_string());
        assert_eq!(result.change.betrag, demo_gemeinsame_buchung().betrag);
        assert_eq!(result.change.kategorie, demo_gemeinsame_buchung().kategorie);
        assert_eq!(result.change.name, demo_gemeinsame_buchung().name);
        assert_eq!(result.change.person, demo_gemeinsame_buchung().person);
    }
}
