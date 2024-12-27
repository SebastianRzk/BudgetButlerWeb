use crate::budgetbutler::pages::sparen::uebersicht_depotauszuege::UebersichtDepotauszuegeViewResult;
use crate::io::html::input::select::Select;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_depotauszuege.html")]
pub struct UebersichtDepotauszuegeTemplate {
    pub database_version: String,
    pub jahre: Select<i32>,
    pub depotauszuege: Vec<DepotauszugTemplate>,
}

pub struct DepotauszugTemplate {
    pub konto_name: String,
    pub datum: String,
    pub datum_iso: String,
    pub buchungen: Vec<DepotwertTemplate>,
}

pub struct DepotwertTemplate {
    depotwert: String,
    wert: String,
}

pub fn render_uebersicht_depotauszuege_template(
    view_result: UebersichtDepotauszuegeViewResult,
) -> String {
    let as_template: UebersichtDepotauszuegeTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(
    view_result: UebersichtDepotauszuegeViewResult,
) -> UebersichtDepotauszuegeTemplate {
    UebersichtDepotauszuegeTemplate {
        database_version: view_result.database_version.as_string(),
        depotauszuege: view_result
            .konten
            .iter()
            .map(|depotauszug| DepotauszugTemplate {
                konto_name: depotauszug.konto.konto_name.name.clone(),
                datum: depotauszug.datum.to_german_string(),
                datum_iso: depotauszug.datum.to_iso_string(),
                buchungen: depotauszug
                    .einzelne_werte
                    .iter()
                    .map(|depotwert| DepotwertTemplate {
                        depotwert: depotwert.depotwert.isin.isin.clone(),
                        wert: depotwert.wert.to_string(),
                    })
                    .collect(),
            })
            .collect(),
        jahre: Select::new(
            view_result.verfuegbare_jahre.clone(),
            Some(view_result.selektiertes_jahr),
        ),
    }
}

#[cfg(test)]
mod tests {
    //TODO
}
