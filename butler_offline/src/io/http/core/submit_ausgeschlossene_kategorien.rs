use crate::budgetbutler::pages::core::action_change_ausgeschlossene_kategorien::{
    action_change_ausgeschlossene_kategorien, ChangeAusgeschlosseneKategorienContext,
};
use crate::budgetbutler::view::request_handler::Redirect;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::http::redirect::http_redirect;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::RootPath;
use actix_web::web::{Data, Form};
use actix_web::{post, HttpResponse};
use serde::Deserialize;

#[post("configuration/submit/ausgeschlossenekategorien")]
pub async fn submit(
    configuration: Data<ConfigurationData>,
    root_path: Data<RootPath>,
    form: Form<SubmitAusgeschlosseneKategorienFormData>,
) -> HttpResponse {
    let mut config = configuration.configuration.lock().unwrap();

    let result = action_change_ausgeschlossene_kategorien(ChangeAusgeschlosseneKategorienContext {
        neue_ausgeschlossene_kategorien: parse_ausgeschlossene_kategorien(
            form.ausgeschlossene_kategorien.clone(),
        ),
        config: &config,
    });

    let refreshed_config = update_configuration(&root_path.path, result.new_config);
    *config = refreshed_config;

    drop(config);

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}

fn parse_ausgeschlossene_kategorien(string: String) -> Vec<Kategorie> {
    let mut kategorien = Vec::new();
    if string.is_empty() {
        return kategorien;
    }

    if !string.contains(",") {
        kategorien.push(Kategorie::new(string));
        return kategorien;
    }

    for kategorie in string.split(",") {
        kategorien.push(Kategorie::new(kategorie.to_string()));
    }
    kategorien
}

#[derive(Deserialize)]
struct SubmitAusgeschlosseneKategorienFormData {
    ausgeschlossene_kategorien: String,
}

#[cfg(test)]
mod tests {
    use crate::io::http::core::submit_ausgeschlossene_kategorien::parse_ausgeschlossene_kategorien;
    use crate::model::primitives::kategorie::kategorie;

    #[test]
    fn test_parse_ausgeschlossene_kategorien() {
        let string = "Kategorie1,Kategorie2,Kategorie3".to_string();
        let kategorien = parse_ausgeschlossene_kategorien(string);
        assert_eq!(kategorien.len(), 3);
        assert_eq!(kategorien[0], kategorie("Kategorie1"));
        assert_eq!(kategorien[1], kategorie("Kategorie2"));
        assert_eq!(kategorien[2], kategorie("Kategorie3"));
    }
}
