use crate::io::cli::dtos::CliArgsDto;
use crate::model::configuration::CliArgs;

pub fn map_to_io_cli(dto: CliArgsDto) -> CliArgs {
    CliArgs {
        user_data_location: dto.user_data_location,
        static_path: dto.static_path,
    }
}
