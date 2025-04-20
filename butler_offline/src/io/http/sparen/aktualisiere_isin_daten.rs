use crate::budgetbutler::pages::sparen::alternative_isin::calculate_alternative_isins;
use crate::budgetbutler::shares::shares_update::calculate_if_share_can_be_updated;
use crate::budgetbutler::shares::shares_update::SharesUpdateStatus::{
    ErrorOnUpdate, NoUpdateNeeded, UpdateAvailable,
};
use crate::budgetbutler::view::redirect_targets::{
    redirect_to_aktualisiere_isin_alternativ, redirect_to_depot_analyse_mit_message,
};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, ActivePage};
use crate::budgetbutler::view::routes::SPAREN_UEBERSICHT_ETFS;
use crate::io::disk::shares::save_shares;
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::sparen::alternative_isin::render_alternative_isin_template;
use crate::io::http::redirect::http_redirect;
use crate::io::online::shares::online_shares::{
    fetch_latest_share_data, load_alternative_isin_index, load_shares_index,
};
use crate::model::primitives::isin::ISIN;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::shares::SharesData;
use actix_web::web::{Data, Form, Path};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[post("aktualisiere_isin/{isin}")]
pub async fn aktualisiere(
    shares: Data<SharesData>,
    path: Path<String>,
    user_application_directory: Data<UserApplicationDirectory>,
) -> impl Responder {
    let isin = ISIN::new(path.into_inner());
    let shares_index = load_shares_index().await;

    let mut current_shares = shares.data.lock().unwrap();
    let share_update = calculate_if_share_can_be_updated(
        &shares_index,
        &isin,
        current_shares.get_share(&isin).map(|x| &x.datum),
    );
    let message = if share_update == UpdateAvailable {
        let new_share_request_data = fetch_latest_share_data(&isin).await;
        if let Some(new_share_data) = new_share_request_data {
            current_shares.append(&isin, new_share_data.clone());
            save_shares(&user_application_directory, &current_shares);
            drop(current_shares);
            format!(
                "Daten von ISIN {} wurden erfolgreich auf Datenbestand von Datum {} aktualisiert.",
                isin.isin,
                new_share_data.datum.to_german_string()
            )
        } else {
            format!(
                "Fehler beim Aktualisieren der ISIN {}. Letzter Datenbestand für die ISIN konnte nicht geladen werden. Datenbestand wurde nicht erneuert",
                isin.isin
            )
        }
    } else if share_update == ErrorOnUpdate {
        format!(
            "Fehler beim Aktualisieren der ISIN {}. Datenbestand wurde nicht erneuert",
            isin.isin
        )
    } else if share_update == NoUpdateNeeded {
        format!(
            "Daten von ISIN {} sind bereits aktuell. Datenbestand wurde nicht erneuert.",
            isin.isin
        )
    } else {
        return http_redirect(redirect_to_aktualisiere_isin_alternativ(&isin));
    };

    http_redirect(redirect_to_depot_analyse_mit_message(message))
}

#[get("aktualisiere_isin_alternativ/{isin}")]
pub async fn get_view_alternativ(
    path: Path<String>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let isin = ISIN::new(path.into_inner());
    let shares_index = load_alternative_isin_index().await;
    let database_name = config
        .configuration
        .lock()
        .unwrap()
        .database_configuration
        .name
        .clone();

    if let Some(shi) = shares_index {
        let view_result = calculate_alternative_isins(shi, &isin);
        let active_page = ActivePage::construct_from_url(SPAREN_UEBERSICHT_ETFS);
        let rendered_view = render_alternative_isin_template(view_result);
        HttpResponse::Ok().body(handle_render_display_view(
            PageTitle::new("Aktualisiere ISIN Alternativ"),
            active_page,
            database_name,
            rendered_view,
        ))
    } else {
        HttpResponse::Ok().body(handle_render_display_view(
            PageTitle::new("Aktualisiere ISIN Alternativ"),
            ActivePage::construct_from_url(SPAREN_UEBERSICHT_ETFS),
            database_name,
            "Fehler beim Laden der Daten".to_string(),
        ))
    }
}

#[derive(Deserialize)]
pub struct AktualisiereISINAlternativQuery {
    pub alternative_isin: String,
}

#[post("aktualisiere_isin_alternativ/{isin}")]
pub async fn update_isin_alternativ(
    path: Path<String>,
    query: Form<AktualisiereISINAlternativQuery>,
    shares: Data<SharesData>,
    user_application_directory: Data<UserApplicationDirectory>,
) -> impl Responder {
    let isin = ISIN::new(path.into_inner());
    let alternative_isin = ISIN::new(query.alternative_isin.clone());

    if alternative_isin.isin == "nichts_tun" {
        return http_redirect(redirect_to_depot_analyse_mit_message(
            "Datenbestand wurde nicht erneuert.".to_string(),
        ));
    }

    let new_share_data = fetch_latest_share_data(&alternative_isin).await;
    let message = if let Some(new_share_data) = new_share_data {
        let datum = new_share_data.datum.clone();
        let mut current_shares = shares.data.lock().unwrap();
        current_shares.append(&isin, new_share_data);
        save_shares(&user_application_directory, &current_shares);
        drop(current_shares);
        format!(
            "Daten von ISIN {} wurden erfolgreich auf Datenbestand von ISIN {} und Datum {} aktualisiert.",
            isin.isin, alternative_isin.isin, datum.to_german_string()
        )
    } else {
        format!(
            "Fehler beim Aktualisieren der ISIN {}. Letzter Datenbestand für die ISIN konnte nicht geladen werden. Datenbestand wurde nicht erneuert",
            isin.isin
        )
    };
    http_redirect(redirect_to_depot_analyse_mit_message(message))
}
