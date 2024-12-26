use crate::budgetbutler::database::abrechnen::abrechnen::history::PreparedAbrechnung;
use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_abrechnungen::UebersichtAbrechnungenViewResult;
use crate::io::disk::diskrepresentation::line::as_string;
pub use askama::Template;

#[derive(Template)]
#[template(path = "gemeinsame_buchungen/uebersicht_abrechnungen.html")]
struct UebersichtAbrechnungenTemplate {
    pub abrechnungen: Vec<AbrechnungTemplate>,
}

struct AbrechnungTemplate {
    title: String,
    original_name: String,
    content: String,
}

pub fn render_uebersicht_gemeinsame_abrechnungen_template(
    template: UebersichtAbrechnungenViewResult,
) -> String {
    let as_template: UebersichtAbrechnungenTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_to_template(
    view_result: UebersichtAbrechnungenViewResult,
) -> UebersichtAbrechnungenTemplate {
    UebersichtAbrechnungenTemplate {
        abrechnungen: view_result
            .abrechnugnen
            .iter()
            .map(|abrechnung: &PreparedAbrechnung| AbrechnungTemplate {
                title: abrechnung.abrechnung_title.clone(),
                original_name: abrechnung.file_name_original.clone(),
                content: as_string(&abrechnung.file_content),
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::history::PreparedAbrechnung;
    use crate::budgetbutler::pages::gemeinsame_buchungen::uebersicht_abrechnungen::UebersichtAbrechnungenViewResult;
    use crate::io::disk::diskrepresentation::line::builder::line;

    #[test]
    fn test_map_to_template() {
        let view_result = UebersichtAbrechnungenViewResult {
            abrechnugnen: vec![PreparedAbrechnung {
                abrechnung_title: "title".to_string(),
                file_name_original: "original".to_string(),
                file_content: vec![line("asdf"), line("sdfg")],
            }],
        };
        let template = super::map_to_template(view_result);
        assert_eq!(template.abrechnungen.len(), 1);
        assert_eq!(template.abrechnungen[0].title, "title");
        assert_eq!(template.abrechnungen[0].original_name, "original");
        assert_eq!(template.abrechnungen[0].content, "asdf\nsdfg");
    }
}
