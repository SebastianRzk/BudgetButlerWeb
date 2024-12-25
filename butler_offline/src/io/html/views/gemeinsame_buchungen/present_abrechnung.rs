use crate::io::disk::diskrepresentation::line::Line;
use crate::model::primitives::person::Person;
pub use askama::Template;

#[derive(Template)]
#[template(path = "gemeinsame_buchungen/present_abrechnung.html")]
pub struct PresendAbrechnungTemplate {
    pub database_name: String,
    pub partner_name: String,
    pub partner_abrechnungstext: String,
    pub self_abrechnungstext: String,
}

pub struct PresentAbrechnungContextResult {
    pub database_name: String,
    pub partner_name: Person,
    pub partner_abrechnungstext: Vec<Line>,
    pub self_abrechnungstext: Vec<Line>,
}

pub fn render_present_abrechnung_template(result: PresentAbrechnungContextResult) -> String {
    let as_template: PresendAbrechnungTemplate = map_to_template(result);
    as_template.render().unwrap()
}

fn map_to_template(view_result: PresentAbrechnungContextResult) -> PresendAbrechnungTemplate {
    PresendAbrechnungTemplate {
        database_name: view_result.database_name,
        partner_name: view_result.partner_name.person,
        partner_abrechnungstext: view_result
            .partner_abrechnungstext
            .iter()
            .map(|line| line.line.clone())
            .collect::<Vec<String>>()
            .join("\n"),
        self_abrechnungstext: view_result
            .self_abrechnungstext
            .iter()
            .map(|line| line.line.clone())
            .collect::<Vec<String>>()
            .join("\n"),
    }
}

#[cfg(test)]
mod tests {
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::io::html::views::gemeinsame_buchungen::present_abrechnung::PresentAbrechnungContextResult;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_map_to_template() {
        let result = PresentAbrechnungContextResult {
            database_name: "test database name".to_string(),
            partner_name: person("test"),
            partner_abrechnungstext: vec![line("asdf"), line("qwer")],
            self_abrechnungstext: vec![line("2asdf"), line("2qwer")],
        };

        let template = super::map_to_template(result);

        assert_eq!(template.database_name, "test database name");
        assert_eq!(template.partner_name, "test");
        assert_eq!(template.partner_abrechnungstext, "asdf\nqwer");
        assert_eq!(template.self_abrechnungstext, "2asdf\n2qwer");
    }
}
