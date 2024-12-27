use crate::budgetbutler::database::util::calc_kategorien;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;
use crate::model::primitives::person::Person;
use crate::model::state::config::Configuration;
use crate::model::state::non_persistent_application_state::GemeinsameBuchungChange;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct AddGemeinsameBuchungViewResult {
    pub database_version: DatabaseVersion,
    pub bearbeitungsmodus: bool,
    pub action_headline: String,
    pub default_item: DefaultItem,
    pub kategorien: Vec<Kategorie>,
    pub personen: Vec<Person>,
    pub action_title: String,
    pub letzte_erfassungen: Vec<LetzteErfassung>,
}

pub struct LetzteErfassung {
    pub fa: String,
    pub datum: String,
    pub person: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub struct AddGemeinsameBuchungContext<'a> {
    pub database: &'a Database,
    pub gemeinsame_buchungen_changes: &'a Vec<GemeinsameBuchungChange>,
    pub extra_kategorie: &'a Option<Kategorie>,
    pub edit_buchung: Option<u32>,
    pub today: Datum,
    pub configuration: Configuration,
}

pub struct DefaultItem {
    pub index: u32,
    pub datum: Datum,
    pub person: Person,
    pub name: Name,
    pub kategorie: Kategorie,
    pub wert: Betrag,
}

pub fn handle_view(context: AddGemeinsameBuchungContext) -> AddGemeinsameBuchungViewResult {
    let mut default_item = DefaultItem {
        index: 0,
        datum: context.today.clone(),
        person: Person::empty(),
        name: Name::empty(),
        kategorie: Kategorie::empty(),
        wert: Betrag::zero(),
    };
    let mut action_headline = "Gemeinsame Buchung erfassen".to_string();
    let mut action_title = "Gemeinsame Buchung erfassen".to_string();
    let mut bearbeitungsmodus = false;

    if let Some(edit_index) = context.edit_buchung {
        let edit_buchung = context.database.gemeinsame_buchungen.get(edit_index);
        default_item = DefaultItem {
            index: edit_index,
            datum: edit_buchung.value.datum.clone(),
            name: edit_buchung.value.name,
            kategorie: edit_buchung.value.kategorie,
            wert: edit_buchung.value.betrag,
            person: edit_buchung.value.person,
        };
        bearbeitungsmodus = true;
        action_headline = "Gemeinsame Buchung bearbeiten".to_string();
        action_title = "Gemeinsame Buchung bearbeiten".to_string();
    }

    let result = AddGemeinsameBuchungViewResult {
        database_version: context.database.db_version.clone(),
        bearbeitungsmodus,
        action_headline,
        default_item,
        personen: vec![
            context.configuration.user_configuration.self_name.clone(),
            context
                .configuration
                .user_configuration
                .partner_name
                .clone(),
        ],
        kategorien: calc_kategorien(
            &context.database.einzelbuchungen,
            context.extra_kategorie,
            &context
                .configuration
                .erfassungs_configuration
                .ausgeschlossene_kategorien,
        ),
        action_title,
        letzte_erfassungen: context
            .gemeinsame_buchungen_changes
            .iter()
            .map(|change| LetzteErfassung {
                fa: change.icon.clone(),
                datum: change.datum.to_german_string(),
                person: change.person.person.clone(),
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
    use crate::budgetbutler::pages::gemeinsame_buchungen::add_gemeinsame_buchung::{
        handle_view, AddGemeinsameBuchungContext,
    };
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::{kategorie, Kategorie};
    use crate::model::primitives::name::{name, Name};
    use crate::model::primitives::person::Person;
    use crate::model::state::config::builder::demo_configuration;
    use crate::model::state::non_persistent_application_state::GemeinsameBuchungChange;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_einzel_und_gemeinsamen_buchungen,
        generate_database_with_gemeinsamen_buchungen, generate_empty_database,
    };

    #[test]
    pub fn test_handle_view_without_edit_index() {
        let database = generate_database_with_einzel_und_gemeinsamen_buchungen(
            vec![demo_einzelbuchung()],
            vec![GemeinsameBuchung {
                datum: Datum::new(11, 11, 2011),
                name: name("test_name"),
                kategorie: kategorie("test_kategorie"),
                betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
                person: Person::new("test_person".to_string()),
            }],
        );
        let context = AddGemeinsameBuchungContext {
            database: &database,
            extra_kategorie: &None,
            gemeinsame_buchungen_changes: &vec![],
            edit_buchung: None,
            configuration: demo_configuration(),
            today: Datum::new(1, 1, 2020),
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.name, "empty");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.action_headline, "Gemeinsame Buchung erfassen");

        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.datum, Datum::new(1, 1, 2020));
        assert_eq!(result.default_item.person, Person::empty());
        assert_eq!(result.default_item.name, Name::empty());
        assert_eq!(result.default_item.kategorie, Kategorie::empty());
        assert_eq!(result.default_item.wert, Betrag::zero());

        assert_eq!(
            result.kategorien,
            vec![demo_kategorie(), kategorie("test_kategorie")]
        );
        assert_eq!(result.action_title, "Gemeinsame Buchung erfassen");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_with_edit_index() {
        let database = generate_database_with_gemeinsamen_buchungen(vec![GemeinsameBuchung {
            datum: Datum::new(11, 11, 2020),
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
            person: Person::new("test_person".to_string()),
        }]);
        let changes = vec![];
        let context = AddGemeinsameBuchungContext {
            database: &database,
            edit_buchung: Some(1),
            extra_kategorie: &None,
            configuration: demo_configuration(),
            today: Datum::new(1, 1, 2020),
            gemeinsame_buchungen_changes: &changes,
        };

        let result = handle_view(context);

        assert_eq!(result.database_version.as_string(), "empty-1-0");
        assert_eq!(result.bearbeitungsmodus, true);
        assert_eq!(result.action_headline, "Gemeinsame Buchung bearbeiten");

        assert_eq!(result.default_item.index, 1);
        assert_eq!(result.default_item.datum, Datum::new(11, 11, 2020));
        assert_eq!(
            result.default_item.person,
            Person::new("test_person".to_string())
        );
        assert_eq!(result.default_item.name, name("test_name"));
        assert_eq!(result.default_item.kategorie, kategorie("test_kategorie"));
        assert_eq!(
            result.default_item.wert,
            Betrag::new(Vorzeichen::Negativ, 10, 0)
        );

        assert_eq!(result.kategorien, vec![kategorie("test_kategorie")]);
        assert_eq!(result.action_title, "Gemeinsame Buchung bearbeiten");
        assert_eq!(result.letzte_erfassungen.len(), 0);
    }

    #[test]
    pub fn test_handle_view_should_preset_changes() {
        let database = generate_empty_database();
        let changes = vec![GemeinsameBuchungChange {
            icon: "fa fa-plus".to_string(),
            datum: Datum::new(11, 11, 2020),
            person: Person::new("test_person".to_string()),
            name: name("test_name"),
            kategorie: kategorie("test_kategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 10, 0),
        }];
        let context = AddGemeinsameBuchungContext {
            database: &database,
            extra_kategorie: &None,
            edit_buchung: None,
            configuration: demo_configuration(),
            today: Datum::new(1, 1, 2020),
            gemeinsame_buchungen_changes: &changes,
        };

        let result = handle_view(context);

        assert_eq!(result.letzte_erfassungen.len(), 1);
        assert_eq!(result.letzte_erfassungen[0].fa, "fa fa-plus");
        assert_eq!(result.letzte_erfassungen[0].datum, "11.11.2020");
        assert_eq!(result.letzte_erfassungen[0].person, "test_person");
        assert_eq!(result.letzte_erfassungen[0].name, "test_name");
        assert_eq!(result.letzte_erfassungen[0].kategorie, "test_kategorie");
        assert_eq!(result.letzte_erfassungen[0].wert, "-10,00");
    }

    #[test]
    fn should_append_extra_kategorie() {
        let database = generate_empty_database();
        let extra_kategorie = Some(kategorie("extra_kategorie"));
        let context = AddGemeinsameBuchungContext {
            database: &database,
            edit_buchung: None,
            configuration: demo_configuration(),
            extra_kategorie: &extra_kategorie,
            today: Datum::new(1, 1, 2020),
            gemeinsame_buchungen_changes: &vec![],
        };

        let result = handle_view(context);

        assert_eq!(result.kategorien, vec![kategorie("extra_kategorie")]);
    }
}
