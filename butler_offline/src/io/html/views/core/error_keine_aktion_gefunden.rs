pub use askama::Template;

#[derive(Template)]
#[template(path = "error_keine_aktion_gefunden.html")]
pub struct ErrorOptimisticLockingTemplate {}

pub fn render_error_keine_aktion_gefunden_template(_context: Option<String>) -> String {
    ErrorOptimisticLockingTemplate {}.render().unwrap()
}
