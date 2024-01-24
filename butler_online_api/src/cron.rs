extern crate diesel;
use diesel::{MysqlConnection, r2d2};
use crate::database::initialize_db_pool;
use crate::wiederkehrend::gemeinsame_buchung;
use crate::wiederkehrend::buchung;

mod schema;
mod einzelbuchungen;
mod gemeinsame_buchungen;
mod kategorien;
mod partner;
mod health;
mod openidconnect_configuration;
mod gemeinsame_dauerauftraege;
mod result_dto;
mod user;
mod dauerauftraege;
mod core;
mod database;
mod wiederkehrend;

type DbPool = r2d2::Pool<r2d2::ConnectionManager<MysqlConnection>>;

fn main() {
    dotenvy::dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let pool = initialize_db_pool();

    let mut connection = pool.get().unwrap();

    buchung::verarbeite_dauerauftraege(&mut connection);
    gemeinsame_buchung::verarbeite_gemeinsame_dauerauftraege(&mut connection);
}

