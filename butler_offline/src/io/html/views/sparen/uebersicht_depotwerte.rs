use crate::budgetbutler::pages::sparen::uebersicht_depotwerte::UebersichtDepotwerteViewResult;
use crate::io::disk::primitive::depotwerttyp::write_depotwerttyp;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_depotwerte.html")]
pub struct UebersichtKontoTemplate {
    pub database_id: String,
    pub depotwerte: Vec<DepotwerteTemplate>,
    pub gesamt_aufbuchungen: String,
    pub gesamt_difference: String,
    pub gesamt_difference_is_negativ: bool,
    pub gesamt_wert: String,
}

pub struct DepotwerteTemplate {
    pub index: u32,
    pub name: String,
    pub typ: String,
    pub isin: String,
    pub aufbuchungen: String,
    pub difference: String,
    pub difference_is_negativ: bool,
    pub wert: String,
}

pub fn render_uebersicht_depotwerte_template(
    view_result: UebersichtDepotwerteViewResult,
) -> String {
    let as_template: UebersichtKontoTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: UebersichtDepotwerteViewResult) -> UebersichtKontoTemplate {
    UebersichtKontoTemplate {
        database_id: view_result.database_version.as_string(),
        depotwerte: view_result
            .depotwerte
            .iter()
            .map(|depotwert| DepotwerteTemplate {
                index: depotwert.depotwert.index,
                name: depotwert.depotwert.value.name.name.clone(),
                typ: write_depotwerttyp(depotwert.depotwert.value.typ.clone())
                    .element
                    .clone(),
                aufbuchungen: depotwert.aufbuchungen.to_german_string(),
                difference: depotwert.differenz.to_german_string(),
                difference_is_negativ: depotwert.differenz.is_negativ(),
                wert: depotwert.kontostand.to_german_string(),
                isin: depotwert.depotwert.value.isin.isin.clone(),
            })
            .collect(),
        gesamt_aufbuchungen: view_result.aufbuchungen.to_german_string(),
        gesamt_difference: view_result.differenz.to_german_string(),
        gesamt_difference_is_negativ: view_result.differenz.is_negativ(),
        gesamt_wert: view_result.gesamt.to_german_string(),
    }
}

#[cfg(test)]
mod tests {
    //TODO
}
