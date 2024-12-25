use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::UebersichtGemeinsameBuchungenViewResult;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
pub use askama::Template;

#[derive(Template)]
#[template(path = "gemeinsame_buchungen/uebersicht_gemeinsam.html")]
pub struct UebersichtGemeinsameBuchungenTemplate {
    pub buchungen: Vec<GemeinsameBuchungTemplate>,
    pub database_id: String,
}

pub struct GemeinsameBuchungTemplate {
    pub index: u32,
    pub datum: String,
    pub name: String,
    pub kategorie: String,
    pub wert: String,
    pub person: String,
}

pub fn render_uebersicht_gemeinsame_buchungen_template(
    template: UebersichtGemeinsameBuchungenViewResult,
) -> String {
    let as_template: UebersichtGemeinsameBuchungenTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_buchung_to_template(buchung: &Indiziert<GemeinsameBuchung>) -> GemeinsameBuchungTemplate {
    GemeinsameBuchungTemplate {
        kategorie: buchung.value.kategorie.kategorie.clone(),
        datum: buchung.value.datum.to_german_string(),
        index: buchung.index,
        wert: buchung.value.betrag.to_german_string(),
        person: buchung.value.person.person.clone(),
        name: buchung.value.name.get_name().clone(),
    }
}

fn map_to_template(
    view_result: UebersichtGemeinsameBuchungenViewResult,
) -> UebersichtGemeinsameBuchungenTemplate {
    let buchungen: Vec<GemeinsameBuchungTemplate> = view_result
        .liste
        .iter()
        .map(|x| map_buchung_to_template(&x))
        .collect();
    UebersichtGemeinsameBuchungenTemplate {
        buchungen,
        database_id: view_result.database_version.as_string(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::UebersichtGemeinsameBuchungenViewResult;
    use crate::io::html::views::gemeinsame_buchungen::uebersicht_gemeinsame_buchungen::map_to_template;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::person;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    fn test_map_to_template() {
        let view_result = UebersichtGemeinsameBuchungenViewResult {
            database_version: demo_database_version(),
            liste: vec![Indiziert {
                index: 0,
                value: GemeinsameBuchung {
                    betrag: zwei(),
                    datum: Datum::new(1, 1, 2024),
                    kategorie: kategorie("NeueKategorie"),
                    name: name("Normal"),
                    person: person("Person"),
                },
                dynamisch: false,
            }],
        };
        let template = map_to_template(view_result);

        assert_eq!(template.buchungen.len(), 1);
        assert_eq!(template.buchungen[0].datum, "01.01.2024");
        assert_eq!(template.buchungen[0].index, 0);
        assert_eq!(template.buchungen[0].kategorie, "NeueKategorie");
        assert_eq!(template.buchungen[0].name, "Normal");
        assert_eq!(template.buchungen[0].person, "Person");
        assert_eq!(template.buchungen[0].wert, "2,00");
        assert_eq!(template.database_id, demo_database_version().as_string());
    }
}
