use crate::budgetbutler::pages::core::action_change_farben::{
    action_change_farben, ChangeFarbenContext,
};
use crate::budgetbutler::view::request_handler::Redirect;
use crate::budgetbutler::view::routes::CORE_CONFIGURATION;
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::http::redirect::http_redirect;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::RootPath;
use actix_web::web::{Data, Form};
use actix_web::{post, HttpResponse};
use std::collections::HashMap;

#[post("configuration/submit/farben")]
pub async fn submit(
    configuration: Data<ConfigurationData>,
    root_path: Data<RootPath>,
    form: Form<HashMap<String, String>>,
) -> HttpResponse {
    let mut config = configuration.configuration.lock().unwrap();

    let mut keys: Vec<&String> = form.keys().into_iter().collect();
    keys.sort();
    let mut neue_farben = Vec::new();

    for key in keys {
        neue_farben.push(Farbe {
            as_string: form.get(key).unwrap().clone(),
        });
    }

    let result = action_change_farben(ChangeFarbenContext {
        neue_farben,
        config: &config,
    });

    let refreshed_config = update_configuration(&root_path.path, result.new_config);
    *config = refreshed_config;

    drop(config);

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}
