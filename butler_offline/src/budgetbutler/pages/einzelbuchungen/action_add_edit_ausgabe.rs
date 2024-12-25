use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_AUSGABE_ADD;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::state::non_persistent_application_state::EinzelbuchungChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

pub struct SubmitContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub wert: Betrag,
}

pub fn submit_ausgabe(context: SubmitContext) -> RedirectResult<EinzelbuchungChange> {
    let einzelbuchung = Einzelbuchung {
        datum: context.datum.clone(),
        name: context.name.clone(),
        kategorie: context.kategorie.clone(),
        betrag: context.wert.negativ(),
    };
    let neue_einzelbuchungen: Einzelbuchungen;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_einzelbuchungen = context
            .database
            .einzelbuchungen
            .change()
            .edit(index, einzelbuchung);
    } else {
        icon = PLUS;
        neue_einzelbuchungen = context
            .database
            .einzelbuchungen
            .change()
            .insert(Einzelbuchung {
                datum: context.datum.clone(),
                name: context.name.clone(),
                kategorie: context.kategorie.clone(),
                betrag: context.wert.negativ(),
            });
    }

    let new_database = context
        .database
        .change_einzelbuchungen(neue_einzelbuchungen);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: EINZELBUCHUNGEN_AUSGABE_ADD.to_string(),
            },
        },
        change: EinzelbuchungChange {
            icon: icon.as_fa.to_string(),
            datum: context.datum.clone(),
            name: context.name.clone(),
            kategorie: context.kategorie.clone(),
            betrag: context.wert.negativ(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::primitives::betrag::builder::{minus_zwei, zwei};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_einzelbuchungen, generate_empty_database,
    };

    #[test]
    fn test_submit_ausgabe() {
        let database = generate_empty_database();
        let context = SubmitContext {
            database: &database,
            edit_index: None,
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            wert: zwei(),
        };
        let result = submit_ausgabe(context);

        assert_eq!(
            result
                .result
                .changed_database
                .einzelbuchungen
                .select()
                .count(),
            1
        );
        assert_eq!(
            result.result.changed_database.einzelbuchungen.get(0).value,
            Einzelbuchung {
                datum: any_datum(),
                name: demo_name(),
                kategorie: demo_kategorie(),
                betrag: zwei().negativ(),
            }
        );

        assert_eq!(result.change.icon, "fa fa-plus");
        assert_eq!(result.change.datum, any_datum());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.kategorie, demo_kategorie());
        assert_eq!(result.change.betrag, minus_zwei());
    }

    #[test]
    fn test_submit_ausgabe_edit() {
        let database = generate_database_with_einzelbuchungen(vec![demo_einzelbuchung()]);
        let context = SubmitContext {
            database: &database,
            edit_index: Some(1),
            datum: any_datum(),
            name: demo_name(),
            kategorie: kategorie("changed kategorie"),
            wert: zwei(),
        };

        let result = submit_ausgabe(context);

        assert_eq!(
            result
                .result
                .changed_database
                .einzelbuchungen
                .select()
                .count(),
            1
        );
        assert_eq!(
            result.result.changed_database.einzelbuchungen.get(1).value,
            Einzelbuchung {
                datum: any_datum(),
                name: demo_name(),
                kategorie: kategorie("changed kategorie"),
                betrag: zwei().negativ(),
            }
        );

        assert_eq!(result.change.icon, "fa fa-pencil");
        assert_eq!(result.change.datum, any_datum());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.kategorie, kategorie("changed kategorie"));
        assert_eq!(result.change.betrag, minus_zwei());
    }
}
