use crate::budgetbutler::pages::core::dashboard::{handle_view, DashboardContext};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::io::html::views::core::dashboard::render_dashboard_template;
use crate::io::html::views::index::PageTitle;
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
    let context = DashboardContext {
        database: &database_guard,
        today: today(),
    };
    let database_name = config.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url("/");
    let view_result = handle_view(context);
    let render_view = render_dashboard_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Dashboard"),
        active_page,
        database_name,
        render_view,
    ))
}
