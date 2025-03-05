use crate::io::disk::configuration::reader::load_configuration;
use crate::io::disk::configuration::writer::write_configuration;
use crate::model::state::config::Configuration;
use std::path::Path;

pub fn update_configuration(
    configuration_path: &Path,
    configuration: Configuration,
) -> Configuration {
    write_configuration(configuration_path, configuration);
    load_configuration(configuration_path)
}
