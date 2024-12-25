use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub fn check_optimistic_locking_error(
    requested_version: &String,
    current_version: DatabaseVersion,
) -> OptimisticLockingResult {
    if requested_version != &current_version.as_string() {
        return OptimisticLockingResult::Error;
    }
    OptimisticLockingResult::Ok
}

#[derive(Debug, PartialEq, Eq)]
pub enum OptimisticLockingResult {
    Error,
    Ok,
}
