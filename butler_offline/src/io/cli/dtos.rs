use clap::Parser;

#[derive(Parser)]
pub struct CliArgsDto {
    #[arg(long, value_name = "graph-location")]
    pub user_data_location: Option<String>,
    #[arg(long, value_name = "static-path")]
    pub static_path: Option<String>,
}
