use crate::budgetbutler::pages::sparen::add_konto::AddKontoViewResult;
use crate::io::disk::primitive::sparkontotyp::write_sparkontotyp;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/add_konto.html")]
pub struct AddKontoTemplate {
    pub database_id: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub default_item: DefaultItemTemplate,
    pub kontotypen: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub name: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub name: String,
    pub kontotyp: String,
}

pub fn render_add_konto_template(view_result: AddKontoViewResult) -> String {
    let as_template: AddKontoTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddKontoViewResult) -> AddKontoTemplate {
    let kontotyp_select = Select::new(
        view_result
            .kontotypen
            .iter()
            .map(|x| write_sparkontotyp(x.clone()).element)
            .collect(),
        Some(write_sparkontotyp(view_result.default_item.typ).element),
    );
    AddKontoTemplate {
        database_id: view_result.database_version.as_string(),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            name: view_result.default_item.name.get_name().clone(),
        },
        approve_title: view_result.action_title.clone(),
        kontotypen: kontotyp_select,
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.fa.clone(),
                name: x.name.get_name().clone(),
                kontotyp: write_sparkontotyp(x.typ.clone()).element,
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_konto::{
        AddKontoViewResult, DefaultItem, LetzteErfassung,
    };
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    pub fn test_map_to_template() {
        let view_result = AddKontoViewResult {
            database_version: DatabaseVersion {
                name: "test".to_string(),
                version: 0,
                session_random: 0,
            },
            bearbeitungsmodus: false,
            action_headline: "Konto erfassen".to_string(),
            default_item: DefaultItem {
                index: 0,
                name: name("Ein Name"),
                typ: Kontotyp::Sparkonto,
            },
            action_title: "Konto erfassen".to_string(),
            letzte_erfassungen: vec![LetzteErfassung {
                fa: "FA".to_string(),
                name: name("Ein Name"),
                typ: Kontotyp::Sparkonto,
            }],
            kontotypen: vec![
                Kontotyp::Sparkonto,
                Kontotyp::GenossenschaftsAnteile,
                Kontotyp::Depot,
            ],
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.database_id, "test-0-0");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.element_titel, "Konto erfassen");
        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, "Ein Name");
        assert_eq!(result.approve_title, "Konto erfassen");

        assert_eq!(result.kontotypen.items.len(), 3);
        assert_eq!(result.kontotypen.items[0].value, "Sparkonto");
        assert_eq!(result.kontotypen.items[0].selected, true);
        assert_eq!(result.kontotypen.items[1].value, "Genossenschafts-Anteile");
        assert_eq!(result.kontotypen.items[1].selected, false);
        assert_eq!(result.kontotypen.items[2].value, "Depot");
        assert_eq!(result.kontotypen.items[2].selected, false);

        assert_eq!(result.letzte_erfassung.len(), 1);
        assert_eq!(result.letzte_erfassung[0].fa, "FA");
        assert_eq!(result.letzte_erfassung[0].name, "Ein Name");
        assert_eq!(result.letzte_erfassung[0].kontotyp, "Sparkonto");
    }
}
