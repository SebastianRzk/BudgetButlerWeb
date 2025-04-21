use crate::budgetbutler::pages::sparen::alternative_isin::AlternativeIsin;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/aktualisiere_isin_alternativ.html")]
pub struct AlternativeIsinTemplate {
    pub isin: String,
    pub isin_alternativen: Vec<IsinAlternativeTemplate>,
}

pub struct IsinAlternativeTemplate {
    isin: String,
    display_name: String,
}

pub fn render_alternative_isin_template(view_result: AlternativeIsin) -> String {
    let as_template: AlternativeIsinTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

pub fn map_to_template(view_result: AlternativeIsin) -> AlternativeIsinTemplate {
    AlternativeIsinTemplate {
        isin: view_result.isin.isin.to_string(),
        isin_alternativen: view_result
            .isin_alternativen
            .iter()
            .map(|alternative| IsinAlternativeTemplate {
                isin: alternative.isin.isin.to_string(),
                display_name: alternative.display_name.clone(),
            })
            .collect(),
    }
}

#[cfg(test)]
mod tests {

    #[test]
    fn test_alternative_isin_template() {
        let template = super::AlternativeIsinTemplate {
            isin: "DE000A0D9PT0".to_string(),
            isin_alternativen: vec![
                super::IsinAlternativeTemplate {
                    isin: "DE000A0D9PT1".to_string(),
                    display_name: "Alternative 1".to_string(),
                },
                super::IsinAlternativeTemplate {
                    isin: "DE000A0D9PT2".to_string(),
                    display_name: "Alternative 2".to_string(),
                },
            ],
        };
        assert_eq!(template.isin, "DE000A0D9PT0");
        assert_eq!(template.isin_alternativen.len(), 2);
        assert_eq!(template.isin_alternativen[0].isin, "DE000A0D9PT1");
        assert_eq!(template.isin_alternativen[0].display_name, "Alternative 1");
        assert_eq!(template.isin_alternativen[1].isin, "DE000A0D9PT2");
        assert_eq!(template.isin_alternativen[1].display_name, "Alternative 2");
    }
}
