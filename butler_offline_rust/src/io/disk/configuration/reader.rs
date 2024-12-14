use std::path::Path;
use crate::model::state::config::Configuration;


pub fn exists_config(configuration_path: &String) -> bool {
    let full_path = Path::new(configuration_path).join("configuration.json");
    full_path.exists()
}

pub fn load_configuration(configuration_path: &String) -> Configuration {
    let full_path = Path::new(configuration_path).join("configuration.json");
    println!("Loading configuration from: {:?}", full_path);
    let file = std::fs::File::open(full_path).unwrap();
    serde_json::from_reader(file).unwrap()
}