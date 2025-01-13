use crate::budgetbutler::view::icons::DELETE;
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT_JAHR_PARAM;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_kategorie::BesitztKategorie;
use crate::model::state::non_persistent_application_state::EinzelbuchungChange;
use crate::model::state::persistent_application_state::Database;

pub struct DeleteContext<'a> {
    pub database: &'a Database,
    pub delete_index: u32,
}

pub fn delete_ausgabe(context: DeleteContext) -> RedirectResult<EinzelbuchungChange> {
    let to_delete = context.database.einzelbuchungen.get(context.delete_index);

    let jahr_von_delete_buchung = context
        .database
        .einzelbuchungen
        .get(context.delete_index)
        .datum()
        .jahr;

    let neue_einzelbuchungen = context
        .database
        .einzelbuchungen
        .change()
        .delete(context.delete_index);

    RedirectResult {
        result: ModificationResult {
            changed_database: context
                .database
                .change_einzelbuchungen(neue_einzelbuchungen),
            target: Redirect {
                target: format!(
                    "{}{}",
                    EINZELBUCHUNGEN_EINZELBUCHUNGEN_UEBERSICHT_JAHR_PARAM, jahr_von_delete_buchung
                ),
            },
        },
        change: EinzelbuchungChange {
            icon: DELETE.as_fa.to_string(),
            datum: to_delete.datum().clone(),
            name: to_delete.value.name.clone(),
            kategorie: to_delete.kategorie().clone(),
            betrag: to_delete.value.betrag,
        },
    }
}

#[cfg(test)]
mod tests {
    use super::DELETE;
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::state::persistent_application_state::builder::generate_database_with_einzelbuchungen;

    #[test]
    fn test_submit_delete_ausgabe() {
        let database = generate_database_with_einzelbuchungen(vec![demo_einzelbuchung()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_ausgabe(context);

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

    #[test]
    fn test_submit_delete_ausgabe_should_redirect_to_jahresuebersicht() {
        let database = generate_database_with_einzelbuchungen(vec![demo_einzelbuchung()]);

        let context = super::DeleteContext {
            database: &database,
            delete_index: 1,
        };

        let result = super::delete_ausgabe(context);

        assert_eq!(result.result.target.target, "/uebersicht/?jahr=2020");
    }
}
