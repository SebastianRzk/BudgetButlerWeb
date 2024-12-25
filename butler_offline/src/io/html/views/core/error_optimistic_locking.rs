pub use askama::Template;

#[derive(Template)]
#[template(path = "error_optimistic_locking.html")]
pub struct ErrorOptimisticLockingTemplate {}

pub fn render_error_optimistic_locking_template(_context: Option<String>) -> String {
    ErrorOptimisticLockingTemplate {}.render().unwrap()
}
