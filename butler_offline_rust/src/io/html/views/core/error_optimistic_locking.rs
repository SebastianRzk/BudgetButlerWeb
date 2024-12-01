use crate::budgetbutler::pages::core::error_optimistic_locking::ErrorOptimisticLockingViewResult;
pub use askama::Template;

#[derive(Template)]
#[template(path = "error_optimistic_locking.html")]
pub struct ErrorOptimisticLockingTemplate {
}

pub fn render_error_optimistic_locking_template(template: ErrorOptimisticLockingViewResult) -> String {
    let as_template: ErrorOptimisticLockingTemplate = map_to_template(template);
    as_template.render().unwrap()
}

fn map_to_template(view_result: ErrorOptimisticLockingViewResult) -> ErrorOptimisticLockingTemplate {
    ErrorOptimisticLockingTemplate {
    }
}
