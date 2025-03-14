use crate::model::configuration::CliArgs;
use crate::model::state::config::alternative_app_root;
use std::path::{absolute, PathBuf};

pub fn user_data_location(cli_args: &CliArgs) -> PathBuf {
    let user_data_location = cli_args
        .user_data_location
        .clone()
        .map(|x| PathBuf::new().join(x))
        .unwrap_or(alternative_app_root().join("data"));
    println!(
        "User data location: {:?}",
        absolute(user_data_location.clone())
            .unwrap()
            .to_str()
            .unwrap()
    );
    user_data_location
}

pub fn compute_static_path(cli_args: &CliArgs) -> PathBuf {
    cli_args
        .static_path
        .clone()
        .map(|x| PathBuf::new().join(x))
        .unwrap_or(alternative_app_root().join("target").join("static"))
}
