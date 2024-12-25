use crate::budgetbutler::pages::core::configuration::{ConfigurationViewResult, FarbenZuordnung};
pub use askama::Template;

#[derive(Template)]
#[template(path = "configuration.html")]
pub struct ConfigurationTemplate {
    database_id: String,
    database_name: String,

    kategorien: Vec<String>,
    partnername: String,

    themecolor: String,

    ausgeschlossene_kategorien: String,

    palette: Vec<FarbenZuordnungTemplate>,
}

pub struct FarbenZuordnungTemplate {
    pub farbe: String,
    pub kategorie: String,
    pub nummer: u32,
}

pub fn render_configuration_template(context: ConfigurationViewResult) -> String {
    let as_template: ConfigurationTemplate = map_to_template(context);
    as_template.render().unwrap()
}

fn map_to_template(view_result: ConfigurationViewResult) -> ConfigurationTemplate {
    let kategorien_liste_as_str: Vec<String> = view_result
        .ausgeschlossene_kategorien
        .iter()
        .map(|x| x.kategorie.clone())
        .collect();
    ConfigurationTemplate {
        palette: map_farbe_to_template(&view_result.palette),
        database_id: view_result.database_id.as_string(),
        themecolor: view_result.themecolor.as_string,
        database_name: view_result.database_name.to_string(),
        kategorien: view_result
            .kategorien
            .iter()
            .map(|x| x.to_string())
            .collect(),
        partnername: view_result.partner.person,
        ausgeschlossene_kategorien: kategorien_liste_as_str.join(","),
    }
}

fn map_farbe_to_template(palette: &Vec<FarbenZuordnung>) -> Vec<FarbenZuordnungTemplate> {
    let mut nummer = 100;
    let mut result = vec![];
    for farbe in palette {
        result.push(FarbenZuordnungTemplate {
            farbe: farbe.farbe.as_string.clone(),
            kategorie: farbe.kategorie.kategorie.clone(),
            nummer,
        });
        nummer += 1;
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::configuration::{
        ConfigurationViewResult, FarbenZuordnung,
    };
    use crate::model::primitives::farbe::builder::farbe;
    use crate::model::primitives::kategorie::builder::{any_kategorie_str, demo_kategorie};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::person::builder::{demo_partner, demo_partner_str};
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, demo_database_version_str,
    };

    #[test]
    fn test_map_to_template() {
        let view_result = ConfigurationViewResult {
            database_id: demo_database_version(),
            kategorien: vec![demo_kategorie()],
            themecolor: farbe("themecolor"),
            palette: vec![
                FarbenZuordnung {
                    farbe: farbe("farbe1"),
                    kategorie: kategorie("kategorie1"),
                },
                FarbenZuordnung {
                    farbe: farbe("farbe2"),
                    kategorie: kategorie("kategorie2"),
                },
            ],
            ausgeschlossene_kategorien: vec![kategorie("ausgeschlossen")],
            database_name: "database_name".to_string(),
            partner: demo_partner(),
        };

        let result = super::map_to_template(view_result);

        assert_eq!(result.database_id, demo_database_version_str());
        assert_eq!(result.database_name, "database_name");
        assert_eq!(result.kategorien, vec![any_kategorie_str()]);
        assert_eq!(result.themecolor, "themecolor");
        assert_eq!(result.partnername, demo_partner_str());
        assert_eq!(result.ausgeschlossene_kategorien, "ausgeschlossen");
        assert_eq!(result.palette.len(), 2);
        assert_eq!(result.palette[0].farbe, "farbe1");
        assert_eq!(result.palette[0].kategorie, "kategorie1");
        assert_eq!(result.palette[0].nummer, 100);
        assert_eq!(result.palette[1].farbe, "farbe2");
        assert_eq!(result.palette[1].kategorie, "kategorie2");
        assert_eq!(result.palette[1].nummer, 101);
    }
}
