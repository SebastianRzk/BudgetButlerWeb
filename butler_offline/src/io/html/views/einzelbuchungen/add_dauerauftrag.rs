use crate::budgetbutler::pages::einzelbuchungen::add_dauerauftrag::AddDauerauftragViewResult;
use crate::io::html::input::select::Select;
use crate::io::html::views::templates::kategorie::flatmap_kategorien_option;
use crate::io::html::views::templates::rhythmen_select_renderer::create_rhythmen_select;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::betrag::Vorzeichen::Positiv;
use crate::model::primitives::rhythmus::Rhythmus;
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/add_dauerauftrag.html")]
pub struct AddDauerauftragTemplate {
    pub database_id: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub default_item: DefaultItemTemplate,
    pub kategorien: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
    pub rhythmen: Select<String>,
    pub typen: Select<String>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub start_datum: String,
    pub ende_datum: String,
    pub name: String,
    pub wert: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub start_datum: String,
    pub ende_datum: String,
    pub name: String,
    pub kategorie: String,
    pub rhythmus: String,
    pub wert: String,
}

pub fn render_add_dauerauftrag_template(template: AddDauerauftragViewResult) -> String {
    let as_template: AddDauerauftragTemplate = map_to_template(template);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddDauerauftragViewResult) -> AddDauerauftragTemplate {
    AddDauerauftragTemplate {
        database_id: view_result.database_version.as_string(),
        kategorien: flatmap_kategorien_option(
            view_result.kategorien,
            view_result.default_item.kategorie.clone(),
        ),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            start_datum: view_result.default_item.start_datum.to_iso_string(),
            ende_datum: view_result.default_item.ende_datum.to_iso_string(),
            name: view_result.default_item.name.get_name().clone(),
            wert: view_result.default_item.wert.abs().to_input_string(),
        },
        approve_title: view_result.action_title.clone(),
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.fa.clone(),
                start_datum: x.start_datum.clone(),
                ende_datum: x.ende_datum.clone(),
                rhythmus: x.rhythmus.to_german_string(),
                name: x.name.clone(),
                kategorie: x.kategorie.clone(),
                wert: x.wert.clone(),
            })
            .collect(),
        rhythmen: create_rhythmen_select(
            view_result.default_item.rhythmus,
            vec![
                Rhythmus::Monatlich,
                Rhythmus::Vierteljaehrlich,
                Rhythmus::Halbjaehrlich,
                Rhythmus::Jaehrlich,
            ],
        ),
        typen: Select::new(
            vec!["Einnahme".to_string(), "Ausgabe".to_string()],
            Some(map_betrag_to_typ(&view_result.default_item.wert)),
        ),
    }
}

fn map_betrag_to_typ(betrag: &Betrag) -> String {
    if betrag.vorzeichen == Positiv {
        "Einnahme".to_string()
    } else {
        "Ausgabe".to_string()
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::add_dauerauftrag::{
        AddDauerauftragViewResult, DefaultItem, LetzteErfassung,
    };
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag::Vorzeichen::Negativ;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    pub fn test_map_to_template() {
        let view_result = AddDauerauftragViewResult {
            database_version: DatabaseVersion {
                name: "test".to_string(),
                version: 0,
                session_random: 0,
            },
            bearbeitungsmodus: false,
            action_headline: "Dauerauftrag erfassen".to_string(),
            default_item: DefaultItem {
                index: 0,
                start_datum: Datum::new(1, 1, 2020),
                ende_datum: Datum::new(1, 1, 2021),
                rhythmus: Rhythmus::Vierteljaehrlich,
                name: name("Ein Name"),
                kategorie: kategorie("Eine Kategorie"),
                wert: Betrag::new(Negativ, 10, 0),
            },
            kategorien: vec![kategorie("Eine Kategorie"), kategorie("Weitere Kategorie")],
            action_title: "Dauerauftrag erfassen".to_string(),
            letzte_erfassungen: vec![LetzteErfassung {
                fa: "FA".to_string(),
                start_datum: Datum::new(1, 1, 2020).to_german_string(),
                ende_datum: Datum::new(1, 1, 2021).to_german_string(),
                rhythmus: Rhythmus::Vierteljaehrlich,
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
        assert_eq!(result.default_item.start_datum, "2020-01-01");
        assert_eq!(result.default_item.ende_datum, "2021-01-01");
        assert_eq!(result.default_item.name, "Ein Name");
        assert_eq!(result.default_item.wert, "10,00");
        assert_eq!(result.approve_title, "Dauerauftrag erfassen");

        assert_eq!(result.kategorien.items.len(), 2);
        assert_eq!(result.kategorien.items[0].value, "Eine Kategorie");
        assert_eq!(result.kategorien.items[0].selected, true);
        assert_eq!(result.kategorien.items[1].value, "Weitere Kategorie");
        assert_eq!(result.kategorien.items[1].selected, false);

        assert_eq!(result.rhythmen.items.len(), 4);
        assert_eq!(result.rhythmen.items[0].value, "monatlich");
        assert_eq!(result.rhythmen.items[0].selected, false);
        assert_eq!(result.rhythmen.items[1].value, "vierteljährlich");
        assert_eq!(result.rhythmen.items[1].selected, true);
        assert_eq!(result.rhythmen.items[2].value, "halbjährlich");
        assert_eq!(result.rhythmen.items[2].selected, false);
        assert_eq!(result.rhythmen.items[3].value, "jährlich");
        assert_eq!(result.rhythmen.items[3].selected, false);

        assert_eq!(result.typen.items.len(), 2);
        assert_eq!(result.typen.items[0].value, "Einnahme");
        assert_eq!(result.typen.items[0].selected, false);
        assert_eq!(result.typen.items[1].value, "Ausgabe");
        assert_eq!(result.typen.items[1].selected, true);

        assert_eq!(result.letzte_erfassung.len(), 1);
        assert_eq!(result.letzte_erfassung[0].fa, "FA");
        assert_eq!(result.letzte_erfassung[0].start_datum, "01.01.2020");
        assert_eq!(result.letzte_erfassung[0].ende_datum, "01.01.2021");
        assert_eq!(result.letzte_erfassung[0].name, "Ein Name");
        assert_eq!(result.letzte_erfassung[0].kategorie, "Eine Kategorie");
        assert_eq!(result.letzte_erfassung[0].wert, "10,00");
    }
}
