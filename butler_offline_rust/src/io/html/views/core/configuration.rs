use crate::budgetbutler::pages::core::configuration::ConfigurationViewResult;
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

    palette: Vec<FarbenZuordnungTemplate>
}

pub struct FarbenZuordnungTemplate {
    pub checked: bool,
    pub nummer: u32,
    pub farbe: String,
    pub kategorie: String,
}

pub fn render_configuration_template(context: ConfigurationViewResult) -> String {
    let as_template: ConfigurationTemplate = map_to_template(context);
    as_template.render().unwrap()
}

fn map_to_template(view_result: ConfigurationViewResult) -> ConfigurationTemplate {
    let kategorien_liste_as_str: Vec<String> = view_result.ausgeschlossene_kategorien.iter().map(|x| x.kategorie.clone()).collect();
    ConfigurationTemplate {
        palette: vec![],
        database_id: view_result.database_id.as_string(),
        themecolor: view_result.themecolor.as_string,
        database_name: view_result.database_name.to_string(),
        kategorien: view_result.kategorien.iter().map(|x| x.to_string()).collect(),
        partnername: view_result.partner.person,
        ausgeschlossene_kategorien: kategorien_liste_as_str.join(","),
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn test_map_to_template() {
        todo!()
    }
}