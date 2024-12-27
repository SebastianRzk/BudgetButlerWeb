use crate::budgetbutler::pages::core::dashboard::DashboardViewResult;
use crate::io::html::json::list::{JSONBetragList, JSONStringList};
use crate::io::html::views::base_templates::BuchungTemplate;
pub use askama::Template;

#[derive(Template)]
#[template(path = "dashboard.html")]
pub struct DashboardTemplate {
    pub zusammenfassung_monatsliste: JSONStringList,
    pub zusammenfassung_einnahmenliste: JSONBetragList,
    pub zusammenfassung_ausgabenliste: JSONBetragList,
    pub ausgaben_des_aktuellen_monats: Vec<BuchungTemplate>,
}

pub fn render_dashboard_template(context: DashboardViewResult) -> String {
    let as_template: DashboardTemplate = map_to_template(context);
    as_template.render().unwrap()
}

fn map_to_template(view_result: DashboardViewResult) -> DashboardTemplate {
    DashboardTemplate {
        zusammenfassung_monatsliste: JSONStringList::new(
            view_result
                .zusammenfassung_monatsliste
                .iter()
                .map(|x| x.monat.clone())
                .collect(),
        ),
        zusammenfassung_einnahmenliste: JSONBetragList::new(
            view_result
                .zusammenfassung_einnahmenliste
                .iter()
                .map(|x| x.clone())
                .collect(),
        ),
        zusammenfassung_ausgabenliste: JSONBetragList::new(
            view_result
                .zusammenfassung_ausgabenliste
                .iter()
                .map(|x| x.clone())
                .collect(),
        ),
        ausgaben_des_aktuellen_monats: view_result
            .ausgaben_des_aktuellen_monats
            .iter()
            .map(|x| BuchungTemplate {
                index: x.index,
                datum: x.value.datum.to_german_string(),
                name: x.value.name.to_string(),
                kategorie: x.value.kategorie.to_string(),
                wert: x.value.betrag.to_german_string(),
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::dashboard::DashboardViewResult;
    use crate::io::html::views::core::dashboard::map_to_template;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::{monats_name, Datum};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;

    #[test]
    fn test_map_to_template() {
        let view_result = DashboardViewResult {
            zusammenfassung_monatsliste: vec![monats_name("Januar"), monats_name("Februar")],
            zusammenfassung_einnahmenliste: vec![
                Betrag::new(Vorzeichen::Positiv, 10, 10),
                Betrag::new(Vorzeichen::Positiv, 20, 20),
            ],
            zusammenfassung_ausgabenliste: vec![
                Betrag::new(Vorzeichen::Positiv, 30, 30),
                Betrag::new(Vorzeichen::Positiv, 40, 40),
            ],
            ausgaben_des_aktuellen_monats: vec![Indiziert {
                index: 0,
                dynamisch: false,
                value: Einzelbuchung {
                    datum: Datum::new(1, 1, 2024),
                    name: name("Normal"),
                    kategorie: kategorie("NeueKategorie"),
                    betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
                },
            }],
        };

        let template = map_to_template(view_result);

        assert_eq!(
            format!("{}", template.zusammenfassung_monatsliste),
            "[\"Januar\",\"Februar\"]"
        );
        assert_eq!(
            format!("{}", template.zusammenfassung_einnahmenliste),
            "[\"10.10\",\"20.20\"]"
        );
        assert_eq!(
            format!("{}", template.zusammenfassung_ausgabenliste),
            "[\"30.30\",\"40.40\"]"
        );

        assert_eq!(template.ausgaben_des_aktuellen_monats.len(), 1);
        let ausgabe = &template.ausgaben_des_aktuellen_monats[0];
        assert_eq!(ausgabe.index, 0);
        assert_eq!(ausgabe.datum, "01.01.2024");
        assert_eq!(ausgabe.name, "Normal");
        assert_eq!(ausgabe.kategorie, "NeueKategorie");
        assert_eq!(format!("{}", ausgabe.wert), "-123,12");
    }
}
