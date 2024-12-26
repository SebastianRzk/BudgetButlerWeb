use crate::budgetbutler::view::icons::{Icon, PENCIL, PLUS};
use crate::budgetbutler::view::request_handler::{ModificationResult, Redirect, RedirectResult};
use crate::budgetbutler::view::routes::EINZELBUCHUNGEN_DAUERAUFTRAG_ADD;
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::state::non_persistent_application_state::DauerauftragChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;

pub struct SubmitDauerauftragContext<'a> {
    pub database: &'a Database,
    pub edit_index: Option<u32>,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub rhythmus: Rhythmus,
    pub name: Name,
    pub kategorie: Kategorie,
    pub wert: Betrag,
}

pub fn submit_dauerauftrag(
    context: SubmitDauerauftragContext,
) -> RedirectResult<DauerauftragChange> {
    let dauerauftrag = Dauerauftrag {
        start_datum: context.start_datum.clone(),
        ende_datum: context.ende_datum.clone(),
        rhythmus: context.rhythmus.clone(),
        name: context.name.clone(),
        kategorie: context.kategorie.clone(),
        betrag: context.wert.clone(),
    };
    let neue_dauerauftraege: Dauerauftraege;
    let icon: Icon;

    if let Some(index) = context.edit_index {
        icon = PENCIL;
        neue_dauerauftraege = context
            .database
            .dauerauftraege
            .change()
            .edit(index, dauerauftrag);
    } else {
        icon = PLUS;
        neue_dauerauftraege = context
            .database
            .dauerauftraege
            .change()
            .insert(Dauerauftrag {
                start_datum: context.start_datum.clone(),
                ende_datum: context.ende_datum.clone(),
                rhythmus: context.rhythmus.clone(),
                name: context.name.clone(),
                kategorie: context.kategorie.clone(),
                betrag: context.wert.clone(),
            });
    }

    let new_database = context.database.change_dauerauftraege(neue_dauerauftraege);

    RedirectResult {
        result: ModificationResult {
            changed_database: new_database,
            target: Redirect {
                target: EINZELBUCHUNGEN_DAUERAUFTRAG_ADD.to_string(),
            },
        },
        change: DauerauftragChange {
            icon: icon.as_fa.to_string(),
            start_datum: context.start_datum.clone(),
            ende_datum: context.ende_datum.clone(),
            rhythmus: context.rhythmus.clone(),
            name: context.name.clone(),
            kategorie: context.kategorie.clone(),
            betrag: context.wert.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::dauerauftrag::builder::demo_dauerauftrag;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_dauerauftraege, generate_empty_database,
    };

    #[test]
    fn test_submit_dauerauftrag() {
        let database = generate_empty_database();
        let context = SubmitDauerauftragContext {
            database: &database,
            edit_index: None,
            start_datum: any_datum(),
            ende_datum: any_datum(),
            rhythmus: Rhythmus::Monatlich,
            name: demo_name(),
            kategorie: demo_kategorie(),
            wert: zwei(),
        };
        let result = submit_dauerauftrag(context);

        assert_eq!(
            result
                .result
                .changed_database
                .dauerauftraege
                .select()
                .count(),
            1
        );
        assert_eq!(
            result.result.changed_database.dauerauftraege.get(0).value,
            Dauerauftrag {
                start_datum: any_datum(),
                ende_datum: any_datum(),
                rhythmus: Rhythmus::Monatlich,
                name: demo_name(),
                kategorie: demo_kategorie(),
                betrag: zwei(),
            }
        );

        assert_eq!(result.change.icon, "fa fa-plus");
        assert_eq!(result.change.start_datum, any_datum());
        assert_eq!(result.change.ende_datum, any_datum());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.kategorie, demo_kategorie());
        assert_eq!(result.change.betrag, zwei());
    }

    #[test]
    fn test_submit_einnahme_edit() {
        let database = generate_database_with_dauerauftraege(vec![demo_dauerauftrag()]);
        let context = SubmitDauerauftragContext {
            database: &database,
            edit_index: Some(1),
            start_datum: any_datum(),
            ende_datum: any_datum(),
            name: demo_name(),
            kategorie: kategorie("changed kategorie"),
            wert: zwei(),
            rhythmus: Rhythmus::Monatlich,
        };

        let result = submit_dauerauftrag(context);

        assert_eq!(
            result
                .result
                .changed_database
                .dauerauftraege
                .select()
                .count(),
            1
        );
        assert_eq!(
            result.result.changed_database.dauerauftraege.get(1).value,
            Dauerauftrag {
                start_datum: any_datum(),
                ende_datum: any_datum(),
                rhythmus: Rhythmus::Monatlich,
                name: demo_name(),
                kategorie: kategorie("changed kategorie"),
                betrag: zwei(),
            }
        );

        assert_eq!(result.change.icon, "fa fa-pencil");
        assert_eq!(result.change.start_datum, any_datum());
        assert_eq!(result.change.ende_datum, any_datum());
        assert_eq!(result.change.name, demo_name());
        assert_eq!(result.change.kategorie, kategorie("changed kategorie"));
        assert_eq!(result.change.betrag, zwei());
    }
}
