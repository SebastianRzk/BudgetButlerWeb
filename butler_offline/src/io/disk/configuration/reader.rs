use crate::model::state::config::Configuration;
use std::path::PathBuf;

pub fn exists_config(configuration_path: &PathBuf) -> bool {
    let full_path = configuration_path.join("configuration.json");
    full_path.exists()
}

pub fn load_configuration(configuration_path: &PathBuf) -> Configuration {
    let full_path = configuration_path.join("configuration.json");
    println!("Loading configuration from: {:?}", full_path);
    let file = std::fs::File::open(full_path).unwrap();
    serde_json::from_reader(file).unwrap()
}
