use actix_web::web::Data;
use actix_web::{App, HttpServer};
use std::sync::Mutex;

mod budgetbutler;
pub mod io;
pub mod model;

use crate::io::disk::configuration::reader::{exists_config, load_configuration};
use crate::io::disk::configuration::updater::update_configuration;
use crate::io::disk::reader::{exists_database, read_database};
use crate::io::disk::writer::write_database;
use crate::io::http::core::error_keine_aktion_gefunden::error_keine_aktion_gefunden;
use crate::io::http::core::error_optimistic_locking::error_optimistic_locking;
use crate::io::http::einzelbuchungen::{
    add_kategorie, modify_dauerauftrag, modify_einnahme, uebersicht_jahr, uebersicht_monat,
};
use crate::io::http::gemeinsame_buchungen::{
    gemeinsam_abrechnen, gemeinsame_buchungen_uebersicht, modify_gemeinsame_ausgabe,
    submit_gemeinsam_abrechnen, uebersicht_abrechnungen,
};
use crate::io::http::sparen::{modify_kontos, uebersicht_kontos, modify_sparbuchungen};
use crate::io::http::shared::import_remote::import_einzelbuchungen_request;
use crate::io::http::shared::redirect_authenticated::logged_in_callback;
use crate::io::http::shared::{export_import, import_mapping};
use crate::model::initial_config::config::generate_initial_config;
use crate::model::initial_config::database::generate_initial_database;
use crate::model::initial_config::path::create_initial_path_if_needed;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{AdditionalKategorie, DauerauftraegeChanges, EinzelbuchungenChanges, GemeinsameBuchungenChanges, KontoChanges, OnlineRedirectActionWrapper, OnlineRedirectState, RootPath, SparbuchungenChanges};
use io::http::core::{configuration, dashboard};
use io::http::einzelbuchungen::{
    dauerauftraege_uebersicht, einzelbuchungen_uebersicht, modify_ausgabe,
};
use model::state::persistent_state::database_version::create_initial_database_version;
use crate::io::http::shared::export_gemeinsame_buchungen::export_gemeinsame_buchungen_request;
use crate::io::http::shared::export_kategorien::export_kategorien_request;
use crate::io::http::shared::import_gemeinsame_remote::import_gemeinsam_request;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let initial_path = "demo".to_string();
    let config;

    create_initial_path_if_needed(&initial_path);
    if exists_config(&initial_path) {
        config = load_configuration(&initial_path);
    } else {
        config = update_configuration(&initial_path, generate_initial_config(&initial_path));
    }

    let database;
    if exists_database(&config.database_configuration) {
        database = read_database(
            &config.database_configuration,
            create_initial_database_version(config.database_configuration.name.clone()),
        );
    } else {
        database = generate_initial_database();
        write_database(&database, &config.database_configuration);
    }

    let state = model::state::persistent_application_state::ApplicationState {
        database: Mutex::new(database),
    };

    let app_state = Data::new(state);
    let einzelbuchungen_changes = Data::new(EinzelbuchungenChanges {
        changes: Mutex::new(Vec::new()),
    });
    let dauerauftraege_changes = Data::new(DauerauftraegeChanges {
        changes: Mutex::new(Vec::new()),
    });
    let gemeinsame_buchungen_changes = Data::new(GemeinsameBuchungenChanges {
        changes: Mutex::new(Vec::new()),
    });

    let konto_changes = Data::new(KontoChanges {
        changes: Mutex::new(Vec::new()),
    });

    let sparbuchungen_changes= Data::new(SparbuchungenChanges {
        changes: Mutex::new(Vec::new()),
    });


    let additional_kategorie_state = Data::new(AdditionalKategorie {
        kategorie: Mutex::new(None),
    });

    let config_state = Data::new(ConfigurationData {
        configuration: Mutex::new(config),
    });

    let online_redirect_state = Data::new(OnlineRedirectState {
        redirect_state: Mutex::new(OnlineRedirectActionWrapper { action: None }),
    });

    let root_path = Data::new(RootPath { path: initial_path });

    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .app_data(einzelbuchungen_changes.clone())
            .app_data(dauerauftraege_changes.clone())
            .app_data(gemeinsame_buchungen_changes.clone())
            .app_data(config_state.clone())
            .app_data(additional_kategorie_state.clone())
            .app_data(root_path.clone())
            .app_data(online_redirect_state.clone())
            .app_data(konto_changes.clone())
            .app_data(sparbuchungen_changes.clone())
            .service(dashboard::view)
            .service(einzelbuchungen_uebersicht::get_view)
            .service(einzelbuchungen_uebersicht::post_view)
            .service(dauerauftraege_uebersicht::get_view)
            .service(modify_ausgabe::get_view)
            .service(modify_ausgabe::post_view)
            .service(modify_ausgabe::post_submit)
            .service(modify_ausgabe::delete)
            .service(modify_einnahme::get_view)
            .service(modify_einnahme::post_view)
            .service(modify_einnahme::post_submit)
            .service(modify_dauerauftrag::get_view)
            .service(modify_dauerauftrag::post_view)
            .service(modify_dauerauftrag::post_submit)
            .service(modify_dauerauftrag::delete)
            .service(modify_dauerauftrag::load_split)
            .service(modify_dauerauftrag::post_split_submit)
            .service(uebersicht_monat::get_view)
            .service(uebersicht_monat::post_view)
            .service(uebersicht_jahr::get_view)
            .service(uebersicht_jahr::post_view)
            .service(add_kategorie::add_kategorie)
            .service(gemeinsame_buchungen_uebersicht::get_view)
            .service(modify_gemeinsame_ausgabe::delete)
            .service(modify_gemeinsame_ausgabe::post_submit)
            .service(modify_gemeinsame_ausgabe::get_view)
            .service(modify_gemeinsame_ausgabe::post_view)
            .service(gemeinsam_abrechnen::get_view)
            .service(gemeinsam_abrechnen::post_view)
            .service(submit_gemeinsam_abrechnen::post_view)
            .service(export_import::get_view)
            .service(export_import::submit_import_manuell)
            .service(import_mapping::submit_import_mapping)
            .service(uebersicht_abrechnungen::get_view)
            .service(io::http::statics::static_files)
            .service(io::http::statics::static_fonts)
            .service(io::http::theme::get_css_theme)
            .service(io::http::core::submit_database_name::submit)
            .service(io::http::core::submit_partner_name::submit)
            .service(io::http::core::submit_theme_color::submit)
            .service(io::http::core::submit_create_backup::submit)
            .service(io::http::core::submit_ausgeschlossene_kategorien::submit)
            .service(io::http::core::submit_change_farben::submit)
            .service(io::http::core::submit_rename_kategorie::submit)
            .service(modify_kontos::get_view)
            .service(modify_kontos::post_view)
            .service(modify_kontos::post_submit)
            .service(modify_kontos::delete)
            .service(configuration::get_view)
            .service(error_optimistic_locking)
            .service(error_keine_aktion_gefunden)
            .service(logged_in_callback)
            .service(import_einzelbuchungen_request)
            .service(export_kategorien_request)
            .service(import_gemeinsam_request)
            .service(export_gemeinsame_buchungen_request)
            .service(uebersicht_kontos::get_view)
            .service(modify_sparbuchungen::get_view)
            .service(modify_sparbuchungen::post_view)
            .service(modify_sparbuchungen::post_submit)
            .service(modify_sparbuchungen::delete)
    })
    .bind(("127.0.0.1", 5000))?
    .run()
    .await
}
