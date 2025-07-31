use crate::io::cargo::get_current_application_version;
use crate::io::disk::reader::exists_database;
use crate::io::disk::version::save_user_data_version;
use crate::io::disk::writer::write_database;
use crate::model::initial_config::database::generate_initial_database;
use crate::model::initial_config::path::create_path_if_needed;
use crate::model::state::config::Configuration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;

pub fn init_database_if_needed(
    config: &Configuration,
    user_application_directory: &UserApplicationDirectory,
) {
    if !exists_database(user_application_directory, &config.database_configuration) {
        create_path_if_needed(&user_application_directory.path.join("abrechnungen"));
        create_path_if_needed(&user_application_directory.path.join("backups").join("import_backup"));
        write_database(
            user_application_directory,
            &generate_initial_database(),
            &config.database_configuration,
        );
        save_user_data_version(user_application_directory, &get_current_application_version());
    }
}
