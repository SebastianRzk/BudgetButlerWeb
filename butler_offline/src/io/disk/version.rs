use crate::budgetbutler::migration::model::ApplicationVersion;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::user_data::VERSION_FILE_NAME;

const UNKNOWN_VERSION: &str = "0.0.0";

pub fn load_user_data_version(
    user_application_directory: &UserApplicationDirectory,
) -> ApplicationVersion {
    let version_path = user_application_directory.path.join(VERSION_FILE_NAME);
    let version_string =
        std::fs::read_to_string(version_path).unwrap_or_else(|_| UNKNOWN_VERSION.to_string());
    ApplicationVersion::new(version_string.as_str())
}

pub fn save_user_data_version(
    user_application_directory: &UserApplicationDirectory,
    version: &ApplicationVersion,
) {
    let version_path = user_application_directory.path.join(VERSION_FILE_NAME);
    std::fs::write(version_path, version.to_string()).expect("Could not write version file");
}
