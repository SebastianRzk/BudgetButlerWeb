use crate::budgetbutler::pages::einzelbuchungen::uebersicht_dauerauftraege::UebersichtDauerauftraegeViewResult;
use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::indiziert::Indiziert;
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/uebersicht_dauerauftraege.html")]
pub struct UebersichtDauerauftraegeTemplate {
    pub id: String,
    pub dauerauftraegegruppen: Vec<DauerauftraegeGruppeTemplate>,
}

pub struct DauerauftraegeGruppeTemplate {
    pub name: String,
    pub dauerauftraege: Vec<DauerauftragTemplate>,
}

pub struct DauerauftragTemplate {
    pub index: u32,
    pub start_datum: String,
    pub ende_datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
    pub rhythmus: String,
}

pub fn render_uebersicht_dauerauftraege_template(
    view_result: UebersichtDauerauftraegeViewResult,
) -> String {
    let as_template: UebersichtDauerauftraegeTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_dauerauftrag(dauerauftrag: &Indiziert<Dauerauftrag>) -> DauerauftragTemplate {
    DauerauftragTemplate {
        index: dauerauftrag.index,
        start_datum: dauerauftrag.value.start_datum.to_german_string(),
        ende_datum: dauerauftrag.value.ende_datum.to_german_string(),
        name: dauerauftrag.value.name.to_string(),
        kategorie: dauerauftrag.value.kategorie.to_string(),
        wert: dauerauftrag.value.betrag.to_german_string(),
        rhythmus: dauerauftrag.value.rhythmus.to_german_string(),
    }
}

fn map_to_template(
    view_result: UebersichtDauerauftraegeViewResult,
) -> UebersichtDauerauftraegeTemplate {
    UebersichtDauerauftraegeTemplate {
        id: view_result.database_version.as_string(),
        dauerauftraegegruppen: vec![
            DauerauftraegeGruppeTemplate {
                name: "Aktuelle Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .aktuelle_dauerauftraege
                    .iter()
                    .map(|d| map_dauerauftrag(d))
                    .collect(),
            },
            DauerauftraegeGruppeTemplate {
                name: "Zukünftige Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .zukuenftige_dauerauftraege
                    .iter()
                    .map(|d| map_dauerauftrag(d))
                    .collect(),
            },
            DauerauftraegeGruppeTemplate {
                name: "Vergangene Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .vergangene_dauerauftraege
                    .iter()
                    .map(|d| map_dauerauftrag(d))
                    .collect(),
            },
        ],
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::einzelbuchungen::uebersicht_dauerauftraege::UebersichtDauerauftraegeViewResult;
    use crate::model::database::dauerauftrag::builder::dauerauftrag_mit_start_ende_datum;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    fn test_map_to_template() {
        let aktueller_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2020), Datum::new(31, 12, 2020));
        let vergangener_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2021), Datum::new(31, 12, 2021));
        let zukuenftiger_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2022), Datum::new(31, 12, 2022));

        let view_result = UebersichtDauerauftraegeViewResult {
            aktuelle_dauerauftraege: vec![indiziert(aktueller_dauerauftrag)],
            vergangene_dauerauftraege: vec![indiziert(vergangener_dauerauftrag)],
            zukuenftige_dauerauftraege: vec![indiziert(zukuenftiger_dauerauftrag)],
            database_version: demo_database_version(),
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.dauerauftraegegruppen.len(), 3);
        assert_eq!(result.dauerauftraegegruppen[0].dauerauftraege.len(), 1);
        assert_eq!(
            result.dauerauftraegegruppen[0].name,
            "Aktuelle Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[0].dauerauftraege[0].start_datum,
            "01.01.2020"
        );

        assert_eq!(result.dauerauftraegegruppen[1].dauerauftraege.len(), 1);
        assert_eq!(
            result.dauerauftraegegruppen[1].name,
            "Zukünftige Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[1].dauerauftraege[0].start_datum,
            "01.01.2022"
        );

        assert_eq!(result.dauerauftraegegruppen[2].dauerauftraege.len(), 1);
        assert_eq!(
            result.dauerauftraegegruppen[2].name,
            "Vergangene Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[2].dauerauftraege[0].start_datum,
            "01.01.2021"
        );
    }
}
