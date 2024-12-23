use crate::budgetbutler::pages::gemeinsame_buchungen::add_gemeinsame_buchung::AddGemeinsameBuchungViewResult;
use crate::io::html::input::select::Select;
use crate::io::html::views::templates::kategorie::flatmap_kategorien_option;
pub use askama::Template;

#[derive(Template)]
#[template(path = "gemeinsame_buchungen/addgemeinsam.html")]
pub struct AddGemeinsameBuchungenTemplate {
    pub database_id: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub default_item: DefaultItemTemplate,
    pub kategorien: Select<String>,
    pub personen: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub datum: String,
    pub name: String,
    pub wert: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub datum: String,
    pub person: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub fn render_add_gemeinsame_buchung_template(template: AddGemeinsameBuchungViewResult) -> String {
    let as_template: AddGemeinsameBuchungenTemplate = map_to_template(template);
    as_template.render().unwrap()
}

pub fn map_to_template(
    view_result: AddGemeinsameBuchungViewResult,
) -> AddGemeinsameBuchungenTemplate {
    AddGemeinsameBuchungenTemplate {
        database_id: view_result.database_version.as_string(),
        kategorien: flatmap_kategorien_option(
            view_result.kategorien,
            view_result.default_item.kategorie,
        ),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            datum: view_result.default_item.datum.to_iso_string(),
            name: view_result.default_item.name.get_name().clone(),
            wert: view_result.default_item.wert.abs().to_input_string(),
        },
        approve_title: view_result.action_title.clone(),
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.fa.clone(),
                datum: x.datum.clone(),
                person: x.person.clone(),
                name: x.name.clone(),
                kategorie: x.kategorie.clone(),
                wert: x.wert.clone(),
            })
            .collect(),
        personen: Select::new(
            view_result
                .personen
                .iter()
                .map(|x| x.person.clone())
                .collect(),
            Some(view_result.default_item.person.person.clone()),
        ),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::gemeinsame_buchungen::add_gemeinsame_buchung::{
        AddGemeinsameBuchungViewResult, DefaultItem, LetzteErfassung,
    };
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag::Vorzeichen::Negativ;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::Person;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    pub fn test_map_to_template() {
        let view_result = AddGemeinsameBuchungViewResult {
            database_version: DatabaseVersion {
                name: "test".to_string(),
                version: 0,
                session_random: 0,
            },
            bearbeitungsmodus: false,
            action_headline: "Dauerauftrag erfassen".to_string(),
            default_item: DefaultItem {
                index: 0,
                datum: Datum::new(1, 1, 2020),
                person: Person::new("Ein Name".to_string()),
                name: name("Ein Name"),
                kategorie: kategorie("Eine Kategorie"),
                wert: Betrag::new(Negativ, 10, 0),
            },
            kategorien: vec![kategorie("Eine Kategorie"), kategorie("Weitere Kategorie")],
            personen: vec![Person::new("Ein Name".to_string())],
            action_title: "Dauerauftrag erfassen".to_string(),
            letzte_erfassungen: vec![LetzteErfassung {
                fa: "FA".to_string(),
                datum: Datum::new(1, 1, 2020).to_german_string(),
                person: "Ein Name".to_string(),
                name: "Ein Name".to_string(),
                kategorie: "Eine Kategorie".to_string(),
                wert: "10,00".to_string(),
            }],
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.database_id, "test-0-0");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.element_titel, "Dauerauftrag erfassen");
        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.datum, "2020-01-01");
        assert_eq!(result.default_item.name, "Ein Name");
        assert_eq!(result.default_item.wert, "10,00");
        assert_eq!(result.approve_title, "Dauerauftrag erfassen");

        assert_eq!(result.kategorien.items.len(), 2);
        assert_eq!(result.kategorien.items[0].value, "Eine Kategorie");
        assert_eq!(result.kategorien.items[0].selected, true);
        assert_eq!(result.kategorien.items[1].value, "Weitere Kategorie");
        assert_eq!(result.kategorien.items[1].selected, false);

        assert_eq!(result.personen.items.len(), 1);
        assert_eq!(result.personen.items[0].value, "Ein Name");
        assert_eq!(result.personen.items[0].selected, true);

        assert_eq!(result.letzte_erfassung.len(), 1);
        assert_eq!(result.letzte_erfassung[0].fa, "FA");
        assert_eq!(result.letzte_erfassung[0].datum, "01.01.2020");
        assert_eq!(result.letzte_erfassung[0].name, "Ein Name");
        assert_eq!(result.letzte_erfassung[0].kategorie, "Eine Kategorie");
        assert_eq!(result.letzte_erfassung[0].wert, "10,00");
        assert_eq!(result.letzte_erfassung[0].person, "Ein Name");
    }
}
