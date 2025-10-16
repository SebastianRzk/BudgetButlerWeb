use crate::budgetbutler::database::init::init_database_if_needed;
use crate::io::disk::configuration::reader::{exists_config, load_configuration};
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::disk::shares::save_shares;
use crate::io::env::{get_env, ENV_APP_PORT, ENV_APP_PROTOCOL, ENV_APP_ROOT};
use crate::model::initial_config::config::generate_initial_config;
use crate::model::initial_config::path::create_path_if_needed;
use crate::model::local::{DEFAULT_APP_NAME, DEFAULT_APP_PORT, DEFAULT_PROTOCOL};
use crate::model::shares::shares_state::ShareState;
use crate::model::state::config::Configuration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use std::path::Path;

pub fn get_protocol() -> String {
    get_env(ENV_APP_PROTOCOL).unwrap_or(DEFAULT_PROTOCOL.to_string())
}

pub fn get_port() -> u16 {
    get_env(ENV_APP_PORT)
        .map(|x| {
            x.parse()
                .expect("Could not parse port. Port should be a number")
        })
        .unwrap_or(DEFAULT_APP_PORT)
}

pub fn get_domain() -> String {
    get_env(ENV_APP_ROOT).unwrap_or(DEFAULT_APP_NAME.to_string())
}

pub fn load_config(user_data_location: &Path) -> Configuration {
    load_configuration(user_data_location)
}

pub fn init_user_data_location_if_needed(user_data_location: &UserApplicationDirectory) {
    create_path_if_needed(&user_data_location.path);
    if !exists_config(&user_data_location.path) {
        let initial_config = generate_initial_config();
        update_configuration(&user_data_location.path, &initial_config);
        save_shares(user_data_location, &ShareState::default());
        init_database_if_needed(&initial_config, user_data_location);
    }
}
