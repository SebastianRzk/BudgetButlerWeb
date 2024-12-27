use crate::budgetbutler::pages::sparen::uebersicht_order_dauerauftraege::UebersichtOrderDauerauftraegeViewResult;
use crate::io::disk::primitive::order_typ::write_ordertyp;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::indiziert::Indiziert;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_orderdauerauftrag.html")]
pub struct UebersichtOrderDauerauftraegeTemplate {
    pub database_version: String,
    pub dauerauftraegegruppen: Vec<DauerauftraegeGruppeTemplate>,
}

pub struct DauerauftraegeGruppeTemplate {
    pub name: String,
    pub dauerauftraege: Vec<OrderDauerauftragTemplate>,
}

pub struct OrderDauerauftragTemplate {
    pub index: u32,
    pub start_datum: String,
    pub ende_datum: String,
    pub depotwert: String,
    pub name: String,
    pub wert: String,
    pub rhythmus: String,
    pub typ: String,
    pub konto: String,
}

pub fn render_uebersicht_order_dauerauftraege_template(
    view_result: UebersichtOrderDauerauftraegeViewResult,
) -> String {
    let as_template: UebersichtOrderDauerauftraegeTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_orderdauerauftrag(dauerauftrag: &Indiziert<OrderDauerauftrag>) -> OrderDauerauftragTemplate {
    OrderDauerauftragTemplate {
        index: dauerauftrag.index,
        start_datum: dauerauftrag.value.start_datum.to_german_string(),
        ende_datum: dauerauftrag.value.ende_datum.to_german_string(),
        name: dauerauftrag.value.name.to_string(),
        wert: dauerauftrag.value.wert.get_realer_wert().to_german_string(),
        typ: write_ordertyp(dauerauftrag.value.wert.get_typ()).element,
        rhythmus: dauerauftrag.value.rhythmus.to_german_string(),
        konto: dauerauftrag.value.konto.konto_name.name.to_string(),
        depotwert: dauerauftrag.value.depotwert.isin.isin.to_string(),
    }
}

fn map_to_template(
    view_result: UebersichtOrderDauerauftraegeViewResult,
) -> UebersichtOrderDauerauftraegeTemplate {
    UebersichtOrderDauerauftraegeTemplate {
        database_version: view_result.database_version.as_string(),
        dauerauftraegegruppen: vec![
            DauerauftraegeGruppeTemplate {
                name: "Aktuelle Order-Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .aktuelle_dauerauftraege
                    .iter()
                    .map(|d| map_orderdauerauftrag(d))
                    .collect(),
            },
            DauerauftraegeGruppeTemplate {
                name: "Zukünftige Order-Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .zukuenftige_dauerauftraege
                    .iter()
                    .map(|d| map_orderdauerauftrag(d))
                    .collect(),
            },
            DauerauftraegeGruppeTemplate {
                name: "Vergangene Order-Daueraufträge".to_string(),
                dauerauftraege: view_result
                    .vergangene_dauerauftraege
                    .iter()
                    .map(|d| map_orderdauerauftrag(d))
                    .collect(),
            },
        ],
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_order_dauerauftraege::UebersichtOrderDauerauftraegeViewResult;
    use crate::model::database::order_dauerauftrag::builder::order_dauerauftrag_with_range;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    fn test_map_to_template() {
        let aktueller_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2020),
            Datum::new(31, 12, 2020),
            Rhythmus::Halbjaehrlich,
        );
        let vergangener_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2021),
            Datum::new(31, 12, 2021),
            Rhythmus::Halbjaehrlich,
        );
        let zukuenftiger_dauerauftrag = order_dauerauftrag_with_range(
            Datum::new(1, 1, 2022),
            Datum::new(31, 12, 2022),
            Rhythmus::Halbjaehrlich,
        );

        let view_result = UebersichtOrderDauerauftraegeViewResult {
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
            "Aktuelle Order-Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[0].dauerauftraege[0].start_datum,
            "01.01.2020"
        );

        assert_eq!(result.dauerauftraegegruppen[1].dauerauftraege.len(), 1);
        assert_eq!(
            result.dauerauftraegegruppen[1].name,
            "Zukünftige Order-Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[1].dauerauftraege[0].start_datum,
            "01.01.2022"
        );

        assert_eq!(result.dauerauftraegegruppen[2].dauerauftraege.len(), 1);
        assert_eq!(
            result.dauerauftraegegruppen[2].name,
            "Vergangene Order-Daueraufträge"
        );
        assert_eq!(
            result.dauerauftraegegruppen[2].dauerauftraege[0].start_datum,
            "01.01.2021"
        );
    }
}
