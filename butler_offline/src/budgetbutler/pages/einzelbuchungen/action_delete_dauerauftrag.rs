use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT;
use crate::model::eigenschaften::besitzt_start_und_ende_datum::BesitztStartUndEndeDatum;
use crate::model::state::non_persistent_application_state::DauerauftragChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_dauerauftrag(context: DeleteContext) -> RedirectResult<DauerauftragChange> {
    let to_delete = context.database.dauerauftraege.get(context.delete_index);

    let neue_dauerauftraege = context
        .database
        .dauerauftraege
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context.database.change_dauerauftraege(neue_dauerauftraege),
            target: Redirect {
                target: EINZELBUCHUNGEN_DAUERAUFTRAG_UEBERSICHT.to_string(),
            },
        },
        change: DauerauftragChange {
            icon: DELETE.as_fa.to_string(),
            start_datum: to_delete.start_datum().clone(),
            ende_datum: to_delete.ende_datum().clone(),
            name: to_delete.value.name.clone(),
            kategorie: to_delete.value.kategorie.clone(),
            betrag: to_delete.value.betrag,
            rhythmus: to_delete.value.rhythmus.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::dauerauftrag::builder::demo_dauerauftrag;
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::state::persistent_application_state::builder::generate_database_with_dauerauftraege;

    #[test]
    fn test_delete_dauerauftrag() {
        let database = generate_database_with_dauerauftraege(vec![demo_dauerauftrag()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_dauerauftrag(context);

        assert_eq!(
            result
                .result
                .changed_database
                .einzelbuchungen
                .select()
                .count(),
            0
        );
        assert_eq!(result.change.icon, DELETE.as_fa.to_string());
        assert_eq!(result.change.betrag, demo_einzelbuchung().betrag);
        assert_eq!(result.change.kategorie, demo_einzelbuchung().kategorie);
        assert_eq!(result.change.name, demo_einzelbuchung().name);
    }
}
