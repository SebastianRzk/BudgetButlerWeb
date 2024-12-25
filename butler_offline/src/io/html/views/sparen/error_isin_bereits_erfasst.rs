pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/error_depotwert_mit_isin_bereits_erfasst.html")]
pub struct ErrorISINBereitsErfasstTemplate {}

pub fn render_error_isin_bereits_erfasst_template(_context: Option<String>) -> String {
    ErrorISINBereitsErfasstTemplate {}.render().unwrap()
}
