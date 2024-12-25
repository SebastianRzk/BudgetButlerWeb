use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ADD;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::state::non_persistent_application_state::GemeinsameBuchungChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;

pub struct SubmitGemeinsameBuchungContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub datum: Datum,
    pub name: Name,
    pub kategorie: Kategorie,
    pub wert: Betrag,
    pub person: Person,
}

pub fn submit_gemeinsame_ausgabe(
    context: SubmitGemeinsameBuchungContext,
) -> RedirectResult<GemeinsameBuchungChange> {
    let buchung = GemeinsameBuchung {
        datum: context.datum.clone(),
        name: context.name.clone(),
        kategorie: context.kategorie.clone(),
        betrag: context.wert.negativ(),
        person: context.person.clone(),
    };
    let neue_buchung: GemeinsameBuchungen;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_buchung = context
            .database
            .gemeinsame_buchungen
            .change()
            .edit(index, buchung.clone())
    } else {
        icon = PLUS;
        neue_buchung = context
            .database
            .gemeinsame_buchungen
            .change()
            .insert(buchung.clone())
    }

    let new_database = context.database.change_gemeinsame_buchungen(neue_buchung);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: GEMEINSAME_BUCHUNGEN_ADD.to_string(),
            },
        },
        change: GemeinsameBuchungChange {
            icon: icon.as_fa.to_string(),
            datum: buchung.datum.clone(),
            name: buchung.name.clone(),
            kategorie: buchung.kategorie.clone(),
            betrag: buchung.betrag,
            person: buchung.person.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::gemeinsame_buchungen::action_add_edit_gemeinsame_buchung::{
        submit_gemeinsame_ausgabe, SubmitGemeinsameBuchungContext,
    };
    use crate::budgetbutler::view::icons::PLUS;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::builder::{minus_zwei, zwei};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::person::builder::demo_person;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_submit_gemeinsame_ausgabe() {
        let database = generate_empty_database();

        let result = submit_gemeinsame_ausgabe(SubmitGemeinsameBuchungContext {
            database: &database,
            edit_index: None,
            datum: any_datum(),
            name: demo_name(),
            kategorie: demo_kategorie(),
            wert: zwei(),
            person: demo_person(),
        });

        assert_eq!(
            result
                .result
                .changed_database
                .gemeinsame_buchungen
                .select()
                .count(),
            1
        );
        assert_eq!(
            result
                .result
                .changed_database
                .gemeinsame_buchungen
                .get(0)
                .value,
            GemeinsameBuchung {
                datum: any_datum(),
                name: demo_name(),
                kategorie: demo_kategorie(),
                betrag: minus_zwei(),
                person: demo_person(),
            }
        );

        assert_eq!(result.change.icon, PLUS.as_fa.to_string());
        assert_eq!(result.change.betrag, minus_zwei());
        assert_eq!(result.change.person, demo_person());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.kategorie, demo_kategorie());
    }
}
