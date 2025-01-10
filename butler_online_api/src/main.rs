extern crate diesel;

use crate::einzelbuchungen::input_http::add_einzelbuchung;
use crate::einzelbuchungen::input_http::delete_einzelbuchung;
use crate::einzelbuchungen::input_http::delete_einzelbuchungen;
use crate::einzelbuchungen::input_http::get_einzelbuchungen;
use actix_identity::IdentityMiddleware;
use actix_session::{config::PersistentSession, storage::CookieSessionStore, SessionMiddleware};
use actix_web::cookie::Key;
use actix_web::web::Data;
use actix_web::{error, middleware, web, App, HttpServer};
use std::collections::HashMap;
use std::sync::RwLock;

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

use crate::dauerauftraege::input_http::add_dauerauftrag;
use crate::dauerauftraege::input_http::delete_dauerauftrag;
use crate::dauerauftraege::input_http::get_dauerauftraege;

use crate::gemeinsame_dauerauftraege::input_http::add_gemeinsamer_dauerauftrag;
use crate::gemeinsame_dauerauftraege::input_http::delete_gemeinsamer_dauerauftrag;
use crate::gemeinsame_dauerauftraege::input_http::get_gemeinsame_dauerauftraege;

use crate::health::input_http::health_status;
use crate::openidconnect_configuration::compute_allowed_redirects;
use crate::user::input_http::user_info;

mod core;
mod database;
mod database_migrations;
mod dauerauftraege;
mod einzelbuchungen;
mod gemeinsame_buchungen;
mod gemeinsame_dauerauftraege;
mod health;
mod kategorien;
mod openidconnect_configuration;
mod partner;
mod result_dto;
mod schema;
mod user;
mod wiederkehrend;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    dotenvy::dotenv().ok();
    env_logger::init_from_env(env_logger::Env::new().default_filter_or("info"));

    let pool = database::initialize_db_pool();

    let secret_key = Key::generate();
    let client: openid::DiscoveredClient = openidconnect_configuration::generate_discovery_client()
        .await
        .map_err(error::ErrorInternalServerError)
        .expect("Can not create openid client");

    let sessions = web::Data::new(RwLock::new(user::model::Sessions {
        map: HashMap::new(),
    }));
    let discovery_client = web::Data::new(client);

    log::info!("Running database migrations");
    let mut connection = pool.get().expect("Can not get connection from pool");
    database_migrations::run_migrations(&mut connection).expect("Can not run database migrations");
    log::info!("Database migations finished");

    log::info!("starting HTTP server at http://0.0.0.0:8080");
    let db_pool = web::Data::new(pool);

    let allowed_redirects = Data::new(compute_allowed_redirects());

    HttpServer::new(move || {
        App::new()
            .wrap(IdentityMiddleware::default())
            .wrap(
                SessionMiddleware::builder(CookieSessionStore::default(), secret_key.clone())
                    .cookie_secure(false)
                    .session_lifecycle(
                        PersistentSession::default().session_ttl(time::Duration::hours(2)),
                    )
                    .build(),
            )
            .wrap(middleware::Logger::default())
            .app_data(discovery_client.clone())
            .app_data(sessions.clone())
            .app_data(db_pool.clone())
            .app_data(allowed_redirects.clone())
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
                    .service(delete_kategorien)
                    .service(add_dauerauftrag)
                    .service(get_dauerauftraege)
                    .service(delete_dauerauftrag)
                    .service(add_gemeinsamer_dauerauftrag)
                    .service(get_gemeinsame_dauerauftraege)
                    .service(delete_gemeinsamer_dauerauftrag),
            )
            .service(health_status)
    })
    .bind(("0.0.0.0", 8080))?
    .run()
    .await
}
