pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/error_depotauszug_bereits_erfasst.html")]
struct ErrorDepotauszugBereitsErfasstTemplate {}

pub fn render_error_depotauszug_bereits_erfasst_template(_context: Option<String>) -> String {
    ErrorDepotauszugBereitsErfasstTemplate {}.render().unwrap()
}
