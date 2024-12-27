use crate::budgetbutler::pages::einzelbuchungen::add_ausgabe::AddBuchungViewResult;
use crate::io::html::input::select::Select;
use crate::io::html::views::templates::kategorie::flatmap_kategorien_option;
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/add_einnahme.html")]
pub struct AddEinnahmeTemplate {
    pub id: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub default_item: DefaultItemTemplate,
    pub kategorien: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
}

pub fn render_add_einnahme_template(template: AddBuchungViewResult) -> String {
    let as_template: AddEinnahmeTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_to_template(view_result: AddBuchungViewResult) -> AddEinnahmeTemplate {
    AddEinnahmeTemplate {
        id: view_result.database_version.as_string(),
        kategorien: flatmap_kategorien_option(
            view_result.kategorien,
            view_result.default_item.kategorie.clone(),
        ),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            datum: view_result.default_item.datum.to_iso_string(),
            name: view_result.default_item.name.get_name().clone(),
            kategorie: view_result.default_item.kategorie.kategorie.clone(),
            wert: view_result.default_item.wert.to_input_string(),
        },
        approve_title: view_result.action_title.clone(),
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.fa.clone(),
                datum: x.datum.clone(),
                name: x.name.clone(),
                kategorie: x.kategorie.clone(),
                wert: x.wert.clone(),
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::add_ausgabe::{
        AddBuchungViewResult, DefaultItem, LetzteErfassung,
    };
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    pub fn test_map_to_template() {
        let view_result = AddBuchungViewResult {
            database_version: DatabaseVersion {
                name: "test".to_string(),
                version: 0,
                session_random: 0,
            },
            bearbeitungsmodus: false,
            action_headline: "Ausgabe erfassen".to_string(),
            default_item: DefaultItem {
                index: 0,
                datum: Datum::new(1, 1, 2020),
                name: name("Ein Name"),
                kategorie: kategorie("Eine Kategorie"),
                wert: Betrag::new(Vorzeichen::Positiv, 10, 0),
            },
            kategorien: vec![kategorie("Eine Kategorie"), kategorie("Weitere Kategorie")],
            action_title: "Ausgabe erfassen".to_string(),
            letzte_erfassungen: vec![LetzteErfassung {
                fa: "FA".to_string(),
                datum: "2020-01-01".to_string(),
                name: "Ein Name".to_string(),
                kategorie: "Eine Kategorie".to_string(),
                wert: "10.00".to_string(),
            }],
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.id, "test-0-0");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.element_titel, "Ausgabe erfassen");
        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.datum, "2020-01-01");
        assert_eq!(result.default_item.name, "Ein Name");
        assert_eq!(result.default_item.kategorie, "Eine Kategorie");
        assert_eq!(result.default_item.wert, "10,00");
        assert_eq!(result.approve_title, "Ausgabe erfassen");

        assert_eq!(result.kategorien.items.len(), 2);
        assert_eq!(result.kategorien.items[0].value, "Eine Kategorie");
        assert_eq!(result.kategorien.items[0].selected, true);
        assert_eq!(result.kategorien.items[1].value, "Weitere Kategorie");
        assert_eq!(result.kategorien.items[1].selected, false);

        assert_eq!(result.letzte_erfassung.len(), 1);
        assert_eq!(result.letzte_erfassung[0].fa, "FA");
        assert_eq!(result.letzte_erfassung[0].datum, "2020-01-01");
        assert_eq!(result.letzte_erfassung[0].name, "Ein Name");
        assert_eq!(result.letzte_erfassung[0].kategorie, "Eine Kategorie");
        assert_eq!(result.letzte_erfassung[0].wert, "10.00");
    }
}
