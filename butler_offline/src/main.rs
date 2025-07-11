use actix_web::web::Data;
use actix_web::{error, web, App, HttpResponse, HttpServer};
use std::sync::Mutex;

mod budgetbutler;
pub mod io;
pub mod model;

use crate::budgetbutler::config::{get_domain, get_port, get_protocol, init_and_load_config};
use crate::budgetbutler::database::init::init_database;
use crate::budgetbutler::migration::migrator::run_migrations;
use crate::io::cargo::get_current_application_version;
use crate::io::cli::endpoints::get_cli_args;
use crate::io::disk::butler::{compute_static_path, user_data_location};
use crate::io::disk::shares::load_shares;
use crate::io::disk::version::load_user_data_version;
use crate::io::http::core::error_keine_aktion_gefunden::error_keine_aktion_gefunden;
use crate::io::http::core::error_optimistic_locking::error_optimistic_locking;
use crate::io::http::core::submit_reload_database::submit_reload_database;
use crate::io::http::einzelbuchungen::{
    add_kategorie, modify_dauerauftrag, modify_einnahme, uebersicht_jahr, uebersicht_monat,
};
use crate::io::http::gemeinsame_buchungen::{
    gemeinsam_abrechnen, gemeinsame_buchungen_uebersicht, modify_gemeinsame_ausgabe,
    submit_gemeinsam_abrechnen, uebersicht_abrechnungen,
};
use crate::io::http::shared::export_gemeinsame_buchungen::export_gemeinsame_buchungen_request;
use crate::io::http::shared::export_kategorien::export_kategorien_request;
use crate::io::http::shared::import_gemeinsame_remote::import_gemeinsam_request;
use crate::io::http::shared::import_remote::import_einzelbuchungen_request;
use crate::io::http::shared::redirect_authenticated::logged_in_callback;
use crate::io::http::shared::{export_import, import_mapping};
use crate::io::http::sparen::aktualisiere_isin_daten;
use crate::io::http::sparen::error_depotauszug_bereits_erfasst::error_depotauszug_bereits_erfasst;
use crate::io::http::sparen::error_isin_bereits_erfasst::error_isin_bereits_erfasst;
use crate::io::http::sparen::{
    modify_depotauszug, modify_depotwerte, modify_kontos, modify_order, modify_order_dauerauftrag,
    modify_sparbuchungen, order_dauerauftraege_uebersicht, order_uebersicht,
    sparbuchungen_uebersicht, uebersicht_depotauszuege, uebersicht_depotwerte, uebersicht_etfs,
    uebersicht_kontos, uebersicht_sparen,
};
use crate::model::local::{get_port_binding_domain, LocalServerName};
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    AdditionalKategorie, DauerauftraegeChanges, DepotauszuegeChanges, DepotwerteChanges,
    EinzelbuchungenChanges, GemeinsameBuchungenChanges, KontoChanges, OnlineRedirectActionWrapper,
    OnlineRedirectState, OrderChanges, OrderDauerauftragChanges, SparbuchungenChanges,
    StaticPathDirectory, UserApplicationDirectory,
};
use crate::model::state::shares::SharesData;
use io::http::core::{configuration, dashboard};
use io::http::einzelbuchungen::{
    dauerauftraege_uebersicht, einzelbuchungen_uebersicht, modify_ausgabe,
};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let cli_args = get_cli_args();

    let user_data_location = user_data_location(&cli_args);
    let static_path = compute_static_path(&cli_args);
    let user_application_directory = UserApplicationDirectory {
        path: user_data_location.clone(),
    };

    run_migrations(
        get_current_application_version(),
        load_user_data_version(&user_application_directory),
        &user_application_directory,
    );

    let app_domain = get_domain();
    let app_port: u16 = get_port();
    let app_protocol: String = get_protocol();

    let config = init_and_load_config(&user_data_location);

    let database = init_database(&user_data_location, &config, &user_application_directory);

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

    let sparbuchungen_changes = Data::new(SparbuchungenChanges {
        changes: Mutex::new(Vec::new()),
    });

    let depotwerte_changes = Data::new(DepotwerteChanges {
        changes: Mutex::new(Vec::new()),
    });

    let order_changes = Data::new(OrderChanges {
        changes: Mutex::new(Vec::new()),
    });

    let order_dauerauftrag_changes = Data::new(OrderDauerauftragChanges {
        changes: Mutex::new(Vec::new()),
    });

    let additional_kategorie_state = Data::new(AdditionalKategorie {
        kategorie: Mutex::new(None),
    });

    let depotauszuge_changes = Data::new(DepotauszuegeChanges {
        changes: Mutex::new(Vec::new()),
    });

    let config_state = Data::new(ConfigurationData {
        configuration: Mutex::new(config),
    });

    let online_redirect_state = Data::new(OnlineRedirectState {
        redirect_state: Mutex::new(OnlineRedirectActionWrapper { action: None }),
    });

    let app_location_state = Data::new(LocalServerName {
        app_domain: app_domain.clone(),
        protocol: app_protocol.clone(),
        app_port,
    });

    let shares_state = Data::new(SharesData {
        data: Mutex::new(load_shares(&user_application_directory)),
    });

    let user_application_directory = Data::new(user_application_directory);
    let static_path_directory = Data::new(StaticPathDirectory { path: static_path });

    println!("Server started at {app_protocol}://{app_domain}:{app_port}");
    HttpServer::new(move || {
        let json_cfg = web::FormConfig::default()
            .limit(40000 * 1000 * 1000)
            .error_handler(|err, _req| {
                error::InternalError::from_response(err, HttpResponse::Conflict().into()).into()
            });
        App::new()
            .app_data(app_state.clone())
            .app_data(static_path_directory.clone())
            .app_data(einzelbuchungen_changes.clone())
            .app_data(dauerauftraege_changes.clone())
            .app_data(gemeinsame_buchungen_changes.clone())
            .app_data(config_state.clone())
            .app_data(additional_kategorie_state.clone())
            .app_data(user_application_directory.clone())
            .app_data(online_redirect_state.clone())
            .app_data(konto_changes.clone())
            .app_data(sparbuchungen_changes.clone())
            .app_data(depotwerte_changes.clone())
            .app_data(order_changes.clone())
            .app_data(order_dauerauftrag_changes.clone())
            .app_data(depotauszuge_changes.clone())
            .app_data(shares_state.clone())
            .app_data(app_location_state.clone())
            .app_data(json_cfg)
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
            .service(sparbuchungen_uebersicht::get_view)
            .service(sparbuchungen_uebersicht::post_view)
            .service(modify_depotwerte::get_view)
            .service(modify_depotwerte::post_view)
            .service(modify_depotwerte::post_submit)
            .service(modify_depotwerte::delete)
            .service(error_isin_bereits_erfasst)
            .service(uebersicht_depotwerte::get_view)
            .service(modify_order::get_view)
            .service(modify_order::post_view)
            .service(modify_order::post_submit)
            .service(modify_order::delete)
            .service(order_uebersicht::get_view)
            .service(order_uebersicht::post_view)
            .service(modify_order_dauerauftrag::get_view)
            .service(modify_order_dauerauftrag::post_view)
            .service(modify_order_dauerauftrag::post_submit)
            .service(modify_order_dauerauftrag::delete)
            .service(modify_order_dauerauftrag::load_split)
            .service(modify_order_dauerauftrag::post_split_submit)
            .service(order_dauerauftraege_uebersicht::get_view)
            .service(modify_depotauszug::get_view)
            .service(modify_depotauszug::post_view)
            .service(modify_depotauszug::post_submit)
            .service(modify_depotauszug::delete)
            .service(uebersicht_depotauszuege::get_view)
            .service(uebersicht_depotauszuege::post_view)
            .service(error_depotauszug_bereits_erfasst)
            .service(uebersicht_sparen::get_view)
            .service(uebersicht_etfs::get_view)
            .service(submit_reload_database)
            .service(aktualisiere_isin_daten::aktualisiere)
            .service(aktualisiere_isin_daten::update_isin_alternativ)
            .service(aktualisiere_isin_daten::get_view_alternativ)
    })
    .bind((get_port_binding_domain(app_domain), app_port))?
    .run()
    .await
}
