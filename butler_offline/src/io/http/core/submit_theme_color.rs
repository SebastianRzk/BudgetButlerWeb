use crate::budgetbutler::pages::core::action_change_theme_color::{
    action_change_theme_color, ChangeThemeColorContext,
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
use serde::Deserialize;

#[post("configuration/submit/themecolor")]
pub async fn submit(
    configuration: Data<ConfigurationData>,
    root_path: Data<RootPath>,
    form: Form<SubmitThemeColorFormData>,
) -> HttpResponse {
    let mut config = configuration.configuration.lock().unwrap();

    let result = action_change_theme_color(ChangeThemeColorContext {
        neue_farbe: Farbe {
            as_string: form.themecolor.clone(),
        },
        config: &config,
    });

    let refreshed_config = update_configuration(&root_path.path, result.new_config);
    *config = refreshed_config;

    drop(config);

    http_redirect(Redirect::to(CORE_CONFIGURATION))
}

#[derive(Deserialize)]
struct SubmitThemeColorFormData {
    themecolor: String,
}
