use crate::budgetbutler::database::util::calc_kategorien;
use crate::budgetbutler::pages::einzelbuchungen::add_ausgabe::{
    AddBuchungContext, AddBuchungViewResult, DefaultItem, LetzteErfassung,
};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;

pub fn handle_view(context: AddBuchungContext) -> AddBuchungViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        datum: context.today,
        name: Name::empty(),
        kategorie: Kategorie::empty(),
        wert: Betrag::zero(),
    };
    let mut action_headline = "Einnahme erfassen".to_string();
    let mut action_title = "Einnahme erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.einzelbuchungen.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            datum: edit_buchung.value.datum,
            name: edit_buchung.value.name,
            kategorie: edit_buchung.value.kategorie,
            wert: edit_buchung.value.betrag.abs(),
        };
        bearbeitungsmodus = true;
        action_headline = "Einnahme bearbeiten".to_string();
        action_title = "Einnahme bearbeiten".to_string();
    }

    let result = AddBuchungViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        kategorien: calc_kategorien(
            &context.database.einzelbuchungen,
            context.extra_kategorie,
            context.ausgeschlossene_kategorien,
        ),
        action_title,
        letzte_erfassungen: context
            .einzelbuchungen_changes
            .iter()
            .map(|change| LetzteErfassung {
                fa: change.icon.clone(),
                datum: change.datum.to_german_string(),
                name: change.name.to_string(),
                kategorie: change.kategorie.to_string(),
                wert: change.betrag.to_german_string(),
            })
            .collect(),
    };
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::add_einnahme::{
        handle_view, AddBuchungContext,
    };
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::{kategorie, Kategorie};
    use crate::model::primitives::name::{name, Name};
    use crate::model::state::non_persistent_application_state::EinzelbuchungChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_einzelbuchungen, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "test_kategorie",
        )]);
        let einzelbuchungen_changes = vec![];
        let context = AddBuchungContext {
            database: &database,
            edit_buchung: None,
            extra_kategorie: &None,
            today: Datum::new(1, 1, 2020),
            einzelbuchungen_changes: &einzelbuchungen_changes,
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Einnahme erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.datum, Datum::new(1, 1, 2020));
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.kategorie, Kategorie::empty());
        assert_eq!(result.default_item.wert, Betrag::zero());

        assert_eq!(result.kategorien, vec![kategorie("test_kategorie")]);
        assert_eq!(result.action_title, "Einnahme erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_einzelbuchungen(vec![Einzelbuchung {
            datum: Datum::new(11, 11, 2011),
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Positiv, 10, 0),
        }]);
        let einzelbuchungen_changes = vec![];
        let context = AddBuchungContext {
            database: &database,
            edit_buchung: Some(1),
            extra_kategorie: &None,
            today: Datum::new(1, 1, 2020),
            einzelbuchungen_changes: &einzelbuchungen_changes,
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Einnahme bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.datum, Datum::new(11, 11, 2011));
        assert_eq!(result.default_item.name, name("test_name"));
        assert_eq!(result.default_item.kategorie, kategorie("test_kategorie"));
        assert_eq!(
            result.default_item.wert,
            Betrag::new(Vorzeichen::Positiv, 10, 0)
        );

        assert_eq!(result.kategorien, vec![kategorie("test_kategorie")]);
        assert_eq!(result.action_title, "Einnahme bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let einzelbuchungen_changes = vec![EinzelbuchungChange {
            icon: "fa fa-plus".to_string(),
            datum: Datum::new(11, 11, 2011),
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
        }];
        let context = AddBuchungContext {
            database: &database,
            extra_kategorie: &None,
            edit_buchung: None,
            today: Datum::new(1, 1, 2020),
            einzelbuchungen_changes: &einzelbuchungen_changes,
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].fa, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].datum, "11.11.2011");
        assert_eq!(result.letzte_erfassungen[0].name, "test_name");
        assert_eq!(result.letzte_erfassungen[0].kategorie, "test_kategorie");
        assert_eq!(result.letzte_erfassungen[0].wert, "-10,00");
    }

    #[test]
    fn should_append_extra_kategorie() {
        let database = generate_empty_database();
        let extra_kategorie = Some(kategorie("extra_kategorie"));
        let context = AddBuchungContext {
            database: &database,
            edit_buchung: None,
            extra_kategorie: &extra_kategorie,
            today: Datum::new(1, 1, 2020),
            einzelbuchungen_changes: &vec![],
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.kategorien, vec![kategorie("extra_kategorie")]);
    }
}
