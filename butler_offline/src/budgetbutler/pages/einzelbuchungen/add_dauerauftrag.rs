use crate::budgetbutler::database::util::calc_kategorien;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::rhythmus::Rhythmus;
use crate::model::state::non_persistent_application_state::DauerauftragChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddDauerauftragViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub kategorien: Vec<Kategorie>,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
}

pub struct LetzteErfassung {
    pub fa: String,
    pub start_datum: String,
    pub rhythmus: Rhythmus,
    pub ende_datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub struct AddDauerauftragContext<'a> {
    pub database: &'a Database,
    pub dauerauftraege_changes: &'a Vec<DauerauftragChange>,
    pub extra_kategorie: &'a Option<Kategorie>,
    pub ausgeschlossene_kategorien: &'a Vec<Kategorie>,
    pub edit_buchung: Option<u32>,
    pub today: Datum,
}

pub struct DefaultItem {
    pub index: u32,
    pub start_datum: Datum,
    pub ende_datum: Datum,
    pub rhythmus: Rhythmus,
    pub name: Name,
    pub kategorie: Kategorie,
    pub wert: Betrag,
}

pub fn handle_view(context: AddDauerauftragContext) -> AddDauerauftragViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        start_datum: context.today.clone(),
        ende_datum: context.today.clone(),
        rhythmus: Rhythmus::Monatlich,
        name: Name::empty(),
        kategorie: Kategorie::empty(),
        wert: Betrag::zero(),
    };
    let mut action_headline = "Dauerauftrag erfassen".to_string();
    let mut action_title = "Dauerauftrag erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.dauerauftraege.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            start_datum: edit_buchung.value.start_datum.clone(),
            ende_datum: edit_buchung.value.ende_datum.clone(),
            rhythmus: edit_buchung.value.rhythmus.clone(),
            name: edit_buchung.value.name,
            kategorie: edit_buchung.value.kategorie,
            wert: edit_buchung.value.betrag,
        };
        bearbeitungsmodus = true;
        action_headline = "Dauerauftrag bearbeiten".to_string();
        action_title = "Dauerauftrag bearbeiten".to_string();
    }

    let result = AddDauerauftragViewResult {
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
            .dauerauftraege_changes
            .iter()
            .map(|change| LetzteErfassung {
                fa: change.icon.clone(),
                start_datum: change.start_datum.to_german_string(),
                ende_datum: change.ende_datum.to_german_string(),
                rhythmus: change.rhythmus.clone(),
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
    use crate::budgetbutler::pages::einzelbuchungen::add_dauerauftrag::{
        handle_view, AddDauerauftragContext,
    };
    use crate::model::database::dauerauftrag::Dauerauftrag;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_kategorie;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::{kategorie, Kategorie};
    use crate::model::primitives::name::{name, Name};
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::non_persistent_application_state::DauerauftragChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_dauerauftraege, generate_database_with_einzelbuchungen,
        generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_einzelbuchungen(vec![einzelbuchung_with_kategorie(
            "test_kategorie",
        )]);
        let context = AddDauerauftragContext {
            database: &database,
            dauerauftraege_changes: &vec![],
            extra_kategorie: &None,
            edit_buchung: None,
            today: Datum::new(1, 1, 2020),
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Dauerauftrag erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.start_datum, Datum::new(1, 1, 2020));
        assert_eq!(result.default_item.ende_datum, Datum::new(1, 1, 2020));
        assert_eq!(result.default_item.rhythmus, Rhythmus::Monatlich);
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.kategorie, Kategorie::empty());
        assert_eq!(result.default_item.wert, Betrag::zero());

        assert_eq!(result.kategorien, vec![kategorie("test_kategorie")]);
        assert_eq!(result.action_title, "Dauerauftrag erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_dauerauftraege(vec![Dauerauftrag {
            start_datum: Datum::new(11, 11, 2011),
            ende_datum: Datum::new(11, 11, 2020),
            rhythmus: Rhythmus::Vierteljaehrlich,
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
        }]);
        let changes = vec![];
        let context = AddDauerauftragContext {
            database: &database,
            edit_buchung: Some(1),
            extra_kategorie: &None,
            today: Datum::new(1, 1, 2020),
            dauerauftraege_changes: &changes,
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Dauerauftrag bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.start_datum, Datum::new(11, 11, 2011));
        assert_eq!(result.default_item.ende_datum, Datum::new(11, 11, 2020));
        assert_eq!(result.default_item.rhythmus, Rhythmus::Vierteljaehrlich);
        assert_eq!(result.default_item.name, name("test_name"));
        assert_eq!(result.default_item.kategorie, kategorie("test_kategorie"));
        assert_eq!(
            result.default_item.wert,
            Betrag::new(Vorzeichen::Negativ, 10, 0)
        );

        assert_eq!(result.kategorien, vec![]);
        assert_eq!(result.action_title, "Dauerauftrag bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![DauerauftragChange {
            icon: "fa fa-plus".to_string(),
            start_datum: Datum::new(11, 11, 2011),
            ende_datum: Datum::new(11, 11, 2020),
            rhythmus: Rhythmus::Vierteljaehrlich,
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
        }];
        let context = AddDauerauftragContext {
            database: &database,
            extra_kategorie: &None,
            edit_buchung: None,
            today: Datum::new(1, 1, 2020),
            dauerauftraege_changes: &changes,
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].fa, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].start_datum, "11.11.2011");
        assert_eq!(result.letzte_erfassungen[0].ende_datum, "11.11.2020");
        assert_eq!(
            result.letzte_erfassungen[0].rhythmus,
            Rhythmus::Vierteljaehrlich
        );
        assert_eq!(result.letzte_erfassungen[0].name, "test_name");
        assert_eq!(result.letzte_erfassungen[0].kategorie, "test_kategorie");
        assert_eq!(result.letzte_erfassungen[0].wert, "-10,00");
    }

    #[test]
    fn should_append_extra_kategorie() {
        let database = generate_empty_database();
        let extra_kategorie = Some(kategorie("extra_kategorie"));
        let context = AddDauerauftragContext {
            database: &database,
            edit_buchung: None,
            extra_kategorie: &extra_kategorie,
            today: Datum::new(1, 1, 2020),
            dauerauftraege_changes: &vec![],
            ausgeschlossene_kategorien: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.kategorien, vec![kategorie("extra_kategorie")]);
    }
}
