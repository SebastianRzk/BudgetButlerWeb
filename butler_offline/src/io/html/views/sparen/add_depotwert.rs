use crate::budgetbutler::pages::sparen::add_depotwert::AddDepotwertViewResult;
use crate::io::disk::primitive::depotwerttyp::write_depotwerttyp;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/add_depotwert.html")]
pub struct AddDepotwertTemplate {
    pub database_id: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub default_item: DefaultItemTemplate,
    pub typen: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub name: String,
    pub isin: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub name: String,
    pub typ: String,
    pub isin: String,
}

pub fn render_add_depotwert_template(view_result: AddDepotwertViewResult) -> String {
    let as_template: AddDepotwertTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddDepotwertViewResult) -> AddDepotwertTemplate {
    let kontotyp_select = Select::new(
        view_result
            .typen
            .iter()
            .map(|x| write_depotwerttyp(x.clone()).element)
            .collect(),
        Some(write_depotwerttyp(view_result.default_item.typ.clone()).element),
    );
    AddDepotwertTemplate {
        database_id: view_result.database_version.as_string(),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            name: view_result.default_item.name.get_name().clone(),
            isin: view_result.default_item.isin.isin.clone(),
        },
        approve_title: view_result.action_title.clone(),
        typen: kontotyp_select,
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.icon.clone(),
                name: x.name.get_name().clone(),
                typ: write_depotwerttyp(x.typ.clone()).element,
                isin: x.isin.clone(),
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::add_depotwert::{
        AddDepotwertViewResult, DefaultItem, LetzteErfassung,
    };
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::primitives::isin::builder::{demo_isin, isin};
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    pub fn test_map_to_template() {
        let view_result = AddDepotwertViewResult {
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
                typ: DepotwertTyp::ETF,
                isin: isin("DE000ETF"),
            },
            action_title: "Konto erfassen".to_string(),
            letzte_erfassungen: vec![LetzteErfassung {
                icon: "FA".to_string(),
                name: name("Ein Name"),
                typ: DepotwertTyp::ETF,
                isin: demo_isin().isin,
            }],
            typen: vec![DepotwertTyp::ETF],
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.database_id, "test-0-0");
        assert_eq!(result.bearbeitungsmodus, false);
        assert_eq!(result.element_titel, "Konto erfassen");
        assert_eq!(result.default_item.index, 0);
        assert_eq!(result.default_item.name, "Ein Name");
        assert_eq!(result.approve_title, "Konto erfassen");

        assert_eq!(result.typen.items.len(), 1);
        assert_eq!(result.typen.items[0].value, "ETF");
        assert_eq!(result.typen.items[0].selected, true);

        assert_eq!(result.letzte_erfassung.len(), 1);
        assert_eq!(result.letzte_erfassung[0].fa, "FA");
        assert_eq!(result.letzte_erfassung[0].name, "Ein Name");
    }
}
