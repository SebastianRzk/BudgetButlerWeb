use crate::budgetbutler::pages::sparen::add_sparbuchung::AddSparbuchungenViewResult;
use crate::io::disk::primitive::sparbuchungtyp::write_sparbuchungtyp;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/add_sparbuchung.html")]
pub struct AddSparbuchungTemplate {
    pub database_id: String,
    pub bearbeitungsmodus: bool,
    pub element_title: String,
    pub default_item: DefaultItemTemplate,
    pub kontos: Select<String>,
    pub typen: Select<String>,
    pub approve_title: String,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
}

pub struct DefaultItemTemplate {
    pub edit_index: u32,
    pub name: String,
    pub datum: String,
    pub wert: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub datum: String,
    pub name: String,
    pub konto: String,
    pub wert: String,
    pub typ: String,
}

pub fn render_add_sparbuchung_template(view_result: AddSparbuchungenViewResult) -> String {
    let as_template: AddSparbuchungTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddSparbuchungenViewResult) -> AddSparbuchungTemplate {
    let konto_select = Select::new(
        view_result
            .kontos
            .iter()
            .map(|x| x.value.name.name.clone())
            .collect(),
        Some(view_result.default_item.konto.konto_name.name),
    );
    let typen_selekt = Select::new(
        view_result
            .typen
            .iter()
            .map(|x| write_sparbuchungtyp(x).element)
            .collect(),
        Some(write_sparbuchungtyp(&view_result.default_item.typ).element),
    );

    AddSparbuchungTemplate {
        database_id: view_result.database_version.as_string(),
        element_title: view_result.action_headline.clone(),
        bearbeitungsmodus: view_result.bearbeitungsmodus,
        default_item: DefaultItemTemplate {
            edit_index: view_result.default_item.index,
            name: view_result.default_item.name.get_name().clone(),
            datum: view_result.default_item.datum.to_iso_string(),
            wert: view_result.default_item.wert.to_input_string(),
        },
        approve_title: view_result.action_title.clone(),
        kontos: konto_select,
        typen: typen_selekt,
        letzte_erfassung: view_result
            .letzte_erfassungen
            .iter()
            .map(|x| LetzteErfassungTemplate {
                fa: x.icon.clone(),
                name: x.name.get_name().clone(),
                datum: x.datum.to_german_string(),
                konto: x.konto.konto_name.name.clone(),
                wert: x.wert.to_german_string(),
                typ: write_sparbuchungtyp(&x.typ).element,
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {}
