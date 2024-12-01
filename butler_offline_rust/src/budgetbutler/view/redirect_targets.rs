use crate::budgetbutler::view::request_handler::Redirect;

pub fn redirect_to_optimistic_locking_error() -> Redirect {
    Redirect {
        target: "/error-optimistic-locking".to_string(),
    }
}