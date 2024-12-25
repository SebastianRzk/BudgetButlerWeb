use crate::budgetbutler::pages::sparen::add_depotauszug::{AddDepotauszugViewResult, KontoItem};
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/add_depotauszug.html")]
pub struct AddDepotauszugTemplate {
    pub bearbeitungsmodus: bool,
    pub database_version: String,
    pub kontos: Vec<KontoTemplate>,
    pub letzte_erfassung: Vec<LetzteErfassungTemplate>,
    pub element_titel: String,
    pub approve_titel: String,
}

pub struct KontoTemplate {
    kontoname: String,
    datum: String,
    filled_items: Vec<ItemTemplate>,
    empty_items: Vec<ItemTemplate>,
}

pub struct ItemTemplate {
    beschreibung: String,
    wert: String,
    isin: String,
}

pub struct LetzteErfassungTemplate {
    pub fa: String,
    pub datum: String,
    pub value: String,
    pub konto: String,
}

pub fn render_add_depotauszug_template(view_result: AddDepotauszugViewResult) -> String {
    let as_template: AddDepotauszugTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AddDepotauszugViewResult) -> AddDepotauszugTemplate {
    let kontos = view_result
        .kontos
        .iter()
        .map(|konto| {
            let filled_items = map_item(&konto.filled_items);
            let empty_items = map_item(&konto.empty_items);
            KontoTemplate {
                kontoname: konto.kontoname.clone(),
                datum: konto.datum.to_iso_string(),
                filled_items,
                empty_items,
            }
        })
        .collect();
    let letzte_erfassung = view_result
        .letzte_erfassung
        .iter()
        .map(|erfassung| LetzteErfassungTemplate {
            fa: erfassung.fa.clone(),
            datum: erfassung.datum.clone(),
            konto: erfassung.konto.clone(),
            value: erfassung.value.clone(),
        })
        .collect();
    AddDepotauszugTemplate {
        bearbeitungsmodus: view_result.bearbeitung,
        database_version: view_result.database_version.clone(),
        kontos,
        letzte_erfassung,
        element_titel: view_result.element_titel,
        approve_titel: view_result.approve_titel,
    }
}

fn map_item(items: &Vec<KontoItem>) -> Vec<ItemTemplate> {
    items
        .iter()
        .map(|item| ItemTemplate {
            beschreibung: item.beschreibung.description.clone(),
            wert: item.wert.to_german_string(),
            isin: item.beschreibung.value.clone(),
        })
        .collect()
}

#[cfg(test)]
mod tests {
    //TODO
}
