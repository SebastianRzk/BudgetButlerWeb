use crate::budgetbutler::pages::sparen::add_order::AddOrderViewResult;
use crate::io::disk::primitive::order_typ::write_ordertyp;
use crate::io::html::input::select::{new_select_with_description, DescriptiveSelectItem, Select};
use crate::model::primitives::type_description::TypeDescription;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/add_order.html")]
pub struct AddOrderTemplate {
    pub database_version: String,
    pub bearbeitungsmodus: bool,
    pub element_titel: String,
    pub approve_title: String,
    pub default_item: DefaultItemTemplate,
    pub typen: Select<DescriptiveSelectItem>,
    pub kontos: Select<String>,
    pub depotwerte: Select<DescriptiveSelectItem>,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub index: u32,
    pub name: String,
    pub datum: String,
    pub wert: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub datum: String,
    pub name: String,
    pub konto: String,
    pub depotwert: String,
    pub typ: String,
    pub wert: String,
}

pub fn render_add_order_template(view_result: AddOrderViewResult) -> String {
    let as_template: AddOrderTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddOrderViewResult) -> AddOrderTemplate {
    AddOrderTemplate {
        database_version: view_result.database_version.as_string(),
        element_titel: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            index: view_result.default_item.index,
            name: view_result.default_item.name.get_name().clone(),
            datum: view_result.default_item.datum.to_iso_string(),
            wert: view_result
                .default_item
                .wert
                .get_realer_wert()
                .to_input_string(),
        },
        approve_title: view_result.action_title.clone(),
        typen: new_select_with_description(
            view_result
                .typen
                .iter()
                .map(|x| TypeDescription {
                    value: write_ordertyp(x.value.clone()).element,
                    description: x.description.clone(),
                })
                .collect(),
            Some(write_ordertyp(view_result.default_item.wert.get_typ()).element),
        ),
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.icon.clone(),
                name: x.name.get_name().clone(),
                datum: x.datum.to_german_string(),
                konto: x.konto.konto_name.get_name().clone(),
                depotwert: x.depotwert.isin.isin.clone(),
                typ: write_ordertyp(x.wert.get_typ()).element,
                wert: x.wert.get_realer_wert().to_german_string(),
            })
            .collect(),
        kontos: Select::new(
            view_result
                .depots
                .iter()
                .map(|x| x.value.name.get_name().clone())
                .collect(),
            Some(view_result.default_item.konto.konto_name.get_name().clone()),
        ),
        depotwerte: new_select_with_description(
            view_result
                .depotwerte
                .iter()
                .map(|x| TypeDescription {
                    value: x.value.clone(),
                    description: x.description.clone(),
                })
                .collect(),
            Some(view_result.default_item.depotwert.isin.isin.clone()),
        ),
    }
}

#[cfg(test)]
mod tests {
    //TODO
}
