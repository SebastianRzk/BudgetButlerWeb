use crate::model::state::config::Configuration;
use std::fs::{remove_file, File};
use std::path::Path;

pub fn write_configuration(configuration_path: &Path, configuration: &Configuration) {
    let full_path = configuration_path.join("configuration.json");
    println!("Writing configuration to {full_path:?}");

    if full_path.exists() {
        remove_file(&full_path).unwrap();
    }
    let file: File = File::create(&full_path).unwrap();

    serde_json::to_writer_pretty(file, &configuration).unwrap()
}
