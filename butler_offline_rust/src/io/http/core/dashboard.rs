use crate::budgetbutler::pages::core::dashboard::{handle_view, DashboardContext};
use crate::budgetbutler::view::request_handler::handle_render_display_view;
use crate::io::html::views::core::dashboard::render_dashboard_template;
use crate::io::time::today;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::Data;
use actix_web::{get, HttpResponse, Responder};

#[get("/")]
pub async fn view(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let config = configuration_data.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Dashboard",
        "/",
        DashboardContext {
            database: &database_guard,
            today: today(),
        },
        handle_view,
        render_dashboard_template,
        config.database_configuration.name.clone(),
    ))
}
