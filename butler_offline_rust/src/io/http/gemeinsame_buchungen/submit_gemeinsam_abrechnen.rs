use crate::budgetbutler::database::abrechnen::abrechnen::importer::import_abrechnung;
use crate::budgetbutler::pages::gemeinsame_buchungen::abrechnen::{
    submit_rechne_ab, GemeinsameBuchungenAbrechnenSubmitContext,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, no_page_middleware};
use crate::budgetbutler::view::routes::GEMEINSAME_BUCHUNGEN_ABRECHNEN;
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::reader::read_database;
use crate::io::disk::writer::{create_database_backup, write_database};
use crate::io::html::views::gemeinsame_buchungen::present_abrechnung::{render_present_abrechnung_template, PresentAbrechnungContextResult};
use crate::io::time::{now, today};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::prozent::Prozent;
use crate::model::state::config::Config;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, HttpResponse, Responder};
use serde::Deserialize;
use crate::budgetbutler::view::optimistic_locking::{check_optimistic_locking_error, OptimisticLockingResult};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::io::http::redirect::http_redirect;

#[post("abrechnen/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    config: Data<Config>,
    form: Form<FormData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_id, database.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }
    create_database_backup(
        &database,
        &config.backup_configuration,
        today(),
        now(),
        "1_before_abrechnen",
    );
    let context = GemeinsameBuchungenAbrechnenSubmitContext {
        today: today(),
        database: &database,
        user_configuration: config.user_configuration.clone(),
        set_mindate: Datum::from_iso_string(&form.set_mindate),
        set_maxdate: Datum::from_iso_string(&form.set_maxdate),
        self_soll: Betrag::from_iso_string(&form.set_self_ausgabe),
        ergebnis: form.set_ergebnis.clone(),
        set_titel: form.set_titel.clone(),
        verhaeltnis: Prozent::from_str_representation(&form.set_verhaeltnis),
        set_self_kategorie: Kategorie::new(form.set_self_kategorie.clone()),
        set_partner_kategorie: Kategorie::new(form.set_other_kategorie.clone()),
    };
    let abrechnungs_ergebnis = submit_rechne_ab(context);

    let now_as_str = now();
    speichere_abrechnung(
        abrechnungs_ergebnis.eigene_abrechnung.lines.clone(),
        config.user_configuration.self_name.clone(),
        config.abrechnungs_configuration.clone(),
        today(),
        now_as_str.clone(),
    );
    speichere_abrechnung(
        abrechnungs_ergebnis.partner_abrechnung.lines.clone(),
        config.user_configuration.partner_name.clone(),
        config.abrechnungs_configuration.clone(),
        today(),
        now_as_str,
    );

    let neue_gemeinsame_buchungen = database.gemeinsame_buchungen.change().delete_all(
        abrechnungs_ergebnis
            .selected_buchungen
            .iter()
            .map(|x| x.index)
            .collect(),
    );

    let new_database_after_deletion =
        database.change_gemeinsame_buchungen(neue_gemeinsame_buchungen);
    let new_database_after_import = import_abrechnung(
        &new_database_after_deletion,
        &abrechnungs_ergebnis.eigene_abrechnung,
    );
    write_database(&new_database_after_import, &config.database_configuration);
    *database = read_database(&config.database_configuration, database.db_version.clone());
    create_database_backup(
        &database,
        &config.backup_configuration,
        today(),
        now(),
        "2_after_abrechnen",
    );

    HttpResponse::Ok().body(handle_render_display_view(
        "Übersicht generierter Abrechnungen",
        GEMEINSAME_BUCHUNGEN_ABRECHNEN,
        PresentAbrechnungContextResult {
            database_name: config.database_configuration.name.clone(),
            partner_name: config.user_configuration.partner_name.clone(),
            partner_abrechnungstext: abrechnungs_ergebnis.partner_abrechnung.lines,
            self_abrechnungstext: abrechnungs_ergebnis.eigene_abrechnung.lines,
        },
        no_page_middleware,
        render_present_abrechnung_template,
    ))
}

fn get_by_filter<T>(filter: Option<String>, filter_value: Option<T>) -> Option<T> {
    if let Some(filter) = filter {
        if filter == "on".to_string() {
            return filter_value;
        }
    }
    None
}

#[derive(Deserialize)]
pub struct FormData {
    pub set_mindate: String,
    pub set_maxdate: String,
    pub set_self_ausgabe: String,
    pub set_ergebnis: String,
    pub set_titel: String,

    pub set_self_kategorie: String,
    pub set_other_kategorie: String,
    pub set_verhaeltnis: String,
    pub database_id: String,
}
