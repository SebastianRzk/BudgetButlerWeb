extern crate diesel;
use crate::database::initialize_db_pool;
use crate::wiederkehrend::buchung_cron;
use crate::wiederkehrend::gemeinsame_buchung_cron;

mod core;
mod database;
mod dauerauftraege;
mod einzelbuchungen;
mod gemeinsame_buchungen;
mod gemeinsame_dauerauftraege;
mod health;
mod kategorien;
mod partner;
mod result_dto;
mod schema;
mod user;
mod wiederkehrend;

fn main() {
    dotenvy::dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let pool = initialize_db_pool();

    let mut connection = pool
        .get()
        .expect("Cannot get database connection from pool");

    buchung_cron::verarbeite_dauerauftraege(&mut connection);
    gemeinsame_buchung_cron::verarbeite_gemeinsame_dauerauftraege(&mut connection);
}
