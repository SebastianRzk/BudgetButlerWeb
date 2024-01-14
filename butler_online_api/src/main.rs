extern crate diesel;

use actix_identity::IdentityMiddleware;
use actix_session::{config::PersistentSession, storage::CookieSessionStore, SessionMiddleware};
use actix_web::cookie::Key;
use actix_web::{error, middleware, web, App, HttpServer};
use diesel::{prelude::*, r2d2};
use std::collections::HashMap;
use std::sync::RwLock;

use crate::einzelbuchungen::input_http::add_einzelbuchung;
use crate::einzelbuchungen::input_http::delete_einzelbuchung;
use crate::einzelbuchungen::input_http::delete_einzelbuchungen;
use crate::einzelbuchungen::input_http::get_einzelbuchungen;

use crate::gemeinsame_buchungen::input_http::add_gemeinsame_buchung;
use crate::gemeinsame_buchungen::input_http::add_gemeinsame_buchungen;
use crate::gemeinsame_buchungen::input_http::delete_gemeinsame_buchung;
use crate::gemeinsame_buchungen::input_http::delete_gemeinsame_buchungen;
use crate::gemeinsame_buchungen::input_http::get_gemeinsame_buchungen;

use crate::partner::input_http::delete_partnerstatus;
use crate::partner::input_http::get_partnerstatus;
use crate::partner::input_http::set_partnerstatus;

use crate::kategorien::input_http::add_kategorie;
use crate::kategorien::input_http::add_kategorien;
use crate::kategorien::input_http::delete_kategorie;
use crate::kategorien::input_http::delete_kategorien;
use crate::kategorien::input_http::get_kategorien;

use crate::health::input_http::health_status;

use crate::user::input_http::user_info;

mod schema;

mod einzelbuchungen;

mod gemeinsame_buchungen;
mod kategorien;

mod partner;

mod health;
mod openidconnect_configuration;

mod result_dto;
mod user;

mod database_migrations;

type DbPool = r2d2::Pool<r2d2::ConnectionManager<MysqlConnection>>;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let pool = initialize_db_pool();

    let secret_key = Key::generate();
    let client: openid::DiscoveredClient = openidconnect_configuration::generate_discovery_client()
        .await
        .map_err(error::ErrorInternalServerError)
        .unwrap();

    let sessions = web::Data::new(RwLock::new(openidconnect_configuration::Sessions {
        map: HashMap::new(),
    }));

    log::info!("Running database migrations");
    let mut connection = pool.get().unwrap();
    database_migrations::run_migrations(&mut connection).unwrap();
    log::info!("Database migations finished");

    log::info!("starting HTTP server at http://localhost:8080");

    HttpServer::new(move || {
        App::new()
            .wrap(IdentityMiddleware::default())
            .app_data(web::Data::new(pool.clone()))
            .wrap(
                SessionMiddleware::builder(CookieSessionStore::default(), secret_key.clone())
                    .cookie_secure(false)
                    .session_lifecycle(
                        PersistentSession::default().session_ttl(cookie::time::Duration::hours(2)),
                    )
                    .build(),
            )
            .wrap(middleware::Logger::default())
            .app_data(web::Data::new(client.clone()))
            .app_data(sessions.clone())
            .app_data(web::Data::new(pool.clone()))
            .service(
                web::scope("/api")
                    .service(
                        web::scope("/login")
                            .service(openidconnect_configuration::logout)
                            .service(openidconnect_configuration::authorize)
                            .service(openidconnect_configuration::login)
                            .service(openidconnect_configuration::offline_access)
                            .service(user_info),
                    )
                    .service(get_einzelbuchungen)
                    .service(add_einzelbuchung)
                    .service(delete_einzelbuchungen)
                    .service(delete_einzelbuchung)
                    .service(add_gemeinsame_buchung)
                    .service(add_gemeinsame_buchungen)
                    .service(delete_gemeinsame_buchung)
                    .service(delete_gemeinsame_buchungen)
                    .service(get_gemeinsame_buchungen)
                    .service(set_partnerstatus)
                    .service(get_partnerstatus)
                    .service(delete_partnerstatus)
                    .service(get_kategorien)
                    .service(add_kategorien)
                    .service(add_kategorie)
                    .service(delete_kategorie)
                    .service(delete_kategorien),
            )
            .service(health_status)
    })
    .bind(("127.0.0.1", 8080))?
    .run()
    .await
}

fn initialize_db_pool() -> DbPool {
    let conn_spec = std::env::var("DATABASE_URL").expect("DATABASE_URL should be set");
    let manager = r2d2::ConnectionManager::<MysqlConnection>::new(conn_spec);
    r2d2::Pool::builder()
        .build(manager)
        .expect("database URL should be valid path to SQLite DB file")
}

