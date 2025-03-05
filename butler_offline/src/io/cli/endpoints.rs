use crate::io::cli::dtos::CliArgsDto;
use crate::io::cli::mapper::map_to_io_cli;
use crate::model::configuration::CliArgs;
use clap::Parser;

pub fn get_cli_args() -> CliArgs {
    map_to_io_cli(CliArgsDto::parse())
}
