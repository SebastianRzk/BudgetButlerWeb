use crate::io::disk::reader::{exists_database, read_database};
use crate::io::disk::writer::write_database;
use crate::model::initial_config::database::generate_initial_database;
use crate::model::initial_config::path::create_path_if_needed;
use crate::model::state::config::Configuration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::create_initial_database_version;
use std::path::Path;

pub fn init_database(
    user_data_location: &Path,
    config: &Configuration,
    user_application_directory: &UserApplicationDirectory,
) -> Database {
    if exists_database(user_application_directory, &config.database_configuration) {
        read_database(
            user_application_directory,
            &config.database_configuration,
            create_initial_database_version(config.database_configuration.name.clone()),
        )
    } else {
        let d = generate_initial_database();
        create_path_if_needed(&user_data_location.join("abrechnungen"));
        create_path_if_needed(&user_data_location.join("backups").join("import_backup"));
        write_database(
            user_application_directory,
            &d,
            &config.database_configuration,
        );
        d
    }
}
