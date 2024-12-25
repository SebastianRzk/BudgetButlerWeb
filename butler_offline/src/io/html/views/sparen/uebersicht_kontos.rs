use crate::budgetbutler::pages::sparen::uebersicht_kontos::UebersichtKontosViewResult;
use crate::io::disk::primitive::sparkontotyp::write_sparkontotyp;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_kontos.html")]
pub struct UebersichtKontoTemplate {
    pub database_id: String,
    pub sparkontos: Vec<SparkontoTemplate>,
    pub gesamt_aufbuchungen: String,
    pub gesamt_difference: String,
    pub gesamt_difference_is_negativ: bool,
    pub gesamt_wert: String,
}

pub struct SparkontoTemplate {
    pub index: u32,
    pub kontoname: String,
    pub kontotyp: String,
    pub aufbuchungen: String,
    pub difference: String,
    pub difference_is_negativ: bool,
    pub wert: String,
}

pub fn render_uebersicht_kontos_template(view_result: UebersichtKontosViewResult) -> String {
    let as_template: UebersichtKontoTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: UebersichtKontosViewResult) -> UebersichtKontoTemplate {
    UebersichtKontoTemplate {
        database_id: view_result.database_version.as_string(),
        sparkontos: view_result
            .konten
            .iter()
            .map(|sparkonto| SparkontoTemplate {
                index: sparkonto.konto.index,
                kontoname: sparkonto.konto.value.name.name.clone(),
                kontotyp: write_sparkontotyp(sparkonto.konto.value.kontotyp.clone())
                    .element
                    .clone(),
                aufbuchungen: sparkonto.aufbuchungen.to_german_string(),
                difference: sparkonto.differenz.to_german_string(),
                difference_is_negativ: sparkonto.differenz.is_negativ(),
                wert: sparkonto.kontostand.to_german_string(),
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
