use crate::model::state::config::Configuration;
use std::fs::{remove_file, File};
use std::path::Path;

pub fn write_configuration(configuration_path: &str, configuration: Configuration) {
    let full_path = Path::new(configuration_path).join("configuration.json");
    println!("Writing configuration to {:?}", full_path);

    let file: File;
    if full_path.exists() {
        remove_file(&full_path).unwrap();
    }
    file = File::create(&full_path).unwrap();

    serde_json::to_writer(file, &configuration).unwrap()
}
