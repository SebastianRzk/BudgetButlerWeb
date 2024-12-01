use actix_web::web::Data;
use actix_web::{App, HttpServer};
use std::sync::Mutex;

pub mod model;
pub mod io;
mod budgetbutler;

use crate::io::disk::reader::read_database;
use crate::io::http::core::error_optimistic_locking::error_optimistic_locking;
use crate::io::http::einzelbuchungen::{add_kategorie, modify_dauerauftrag, modify_einnahme, uebersicht_jahr, uebersicht_monat};
use crate::io::http::gemeinsame_buchungen::{gemeinsame_buchungen_uebersicht, modify_gemeinsame_ausgabe, gemeinsam_abrechnen, submit_gemeinsam_abrechnen, uebersicht_abrechnungen};
use crate::io::http::shared::export_import;
use crate::model::state::config::{AbrechnungsConfiguration, BackupConfiguration, Config, DatabaseConfiguration, UserConfiguration};
use crate::model::state::non_persistent_application_state::{AdditionalKategorie, DauerauftraegeChanges, EinzelbuchungenChanges, GemeinsameBuchungenChanges};
use io::http::core::{dashboard, configuration};
use io::http::einzelbuchungen::{dauerauftraege_uebersicht, einzelbuchungen_uebersicht, modify_ausgabe};
use model::primitives::farbe::Farbe;
use model::state::config::DesignConfiguration;
use crate::model::primitives::person::Person;
use crate::model::remote::server::ServerConfiguration;
use crate::model::state::persistent_application_state::create_initial_database_version;

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let config = Config {
        database_configuration: DatabaseConfiguration {
            name: "testname".to_string(),
            location: "demo/Database_Test_User.csv".to_string(),
        },
        abrechnungs_configuration: AbrechnungsConfiguration {
            location: "demo/abrechnungen".to_string(),
        },
        backup_configuration: BackupConfiguration {
            location: "demo/backups".to_string(),
        },
        design_configuration: DesignConfiguration {
            design_farbe: Farbe{
                as_string: "#00acd6".to_string()
            },
            configurierte_farben: vec![
                Farbe {
                    as_string: "green".to_string()
                },
                Farbe {
                    as_string: "blue".to_string()
                },
            ],
        },
        server_configuration: ServerConfiguration {
            server_url: "http://localhost:8081".to_string(),
        },
        user_configuration: UserConfiguration {
            self_name: Person::new("Sebastian".to_string()),
            partner_name: Person::new("kein_Partnername_gesetzt".to_string()),
        }
    };

    let database = read_database(&config.database_configuration, create_initial_database_version(config.database_configuration.name.clone()));

    let state = model::state::persistent_application_state::ApplicationState {
        database: Mutex::new(database)
    };

    let app_state = Data::new(state);
    let einzelbuchungen_changes = Data::new(EinzelbuchungenChanges {
        changes: Mutex::new(Vec::new())
    });
    let dauerauftraege_changes = Data::new(DauerauftraegeChanges {
        changes: Mutex::new(Vec::new())
    });
    let gemeinsame_buchungen_changes = Data::new(GemeinsameBuchungenChanges {
        changes: Mutex::new(Vec::new())
    });

    let additional_kategorie_state = Data::new(AdditionalKategorie {
        kategorie: Mutex::new(None),
    });

    let config_state = Data::new(config);

    HttpServer::new(move || {
        App::new()
            .app_data(app_state.clone())
            .app_data(einzelbuchungen_changes.clone())
            .app_data(dauerauftraege_changes.clone())
            .app_data(gemeinsame_buchungen_changes.clone())
            .app_data(config_state.clone())
            .app_data(additional_kategorie_state.clone())
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
            .service(uebersicht_abrechnungen::get_view)
            .service(io::http::statics::static_files)
            .service(io::http::statics::static_fonts)
            .service(io::http::theme::get_css_theme)
            .service(configuration::get_view)
            .service(error_optimistic_locking)
    })
        .bind(("127.0.0.1", 8081))?
        .run()
        .await
}

