use crate::io::disk::configuration::reader::{exists_config, load_configuration};
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::env::{get_env, ENV_APP_PORT, ENV_APP_PROTOCOL, ENV_APP_ROOT};
use crate::model::initial_config::config::generate_initial_config;
use crate::model::initial_config::path::create_path_if_needed;
use crate::model::local::{DEFAULT_APP_NAME, DEFAULT_APP_PORT, DEFAULT_PROTOCOL};
use crate::model::state::config::Configuration;
use std::path::PathBuf;

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

pub fn load_config(user_data_location: &PathBuf) -> Configuration {
    load_configuration(user_data_location)
}

pub fn init_if_needed(user_data_location: &PathBuf) {
    create_path_if_needed(user_data_location);
    if !exists_config(user_data_location) {
        update_configuration(user_data_location, generate_initial_config());
    }
}
