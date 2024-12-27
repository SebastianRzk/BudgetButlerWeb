use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::{
    redirect_to_keine_aktion_gefunden, redirect_to_optimistic_locking_error,
};
use crate::budgetbutler::view::request_handler::Redirect;
use crate::io::disk::updater::update_database;
use crate::io::disk::writer::create_database_backup;
use crate::io::http::redirect::http_redirect;
use crate::io::http::shared::action_export_gemeinsame_buchungen::export_gemeinsame_buchungen_request;
use crate::io::http::shared::action_import_einzelbuchungen::import_einzelbuchungen_request;
use crate::io::http::shared::action_import_gemeinsame_buchungen::import_gemeinsame_buchungen_request;
use crate::io::http::shared::action_upload_kategorien::upload_kategorien;
use crate::io::time::{now, today};
use crate::model::remote::login::{Cookie, LoginCredentials};
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::{
    OnlineRedirectActionType, OnlineRedirectState,
};
use crate::model::state::persistent_application_state::{ApplicationState, Database};
use actix_web::web::{Data, Query};
use actix_web::{get, HttpResponse, Responder};
use serde::Deserialize;

#[get("/butler-online-callback")]
pub async fn logged_in_callback(
    query: Query<RedirectAuthenticatedQuery>,
    online_redirect_state: Data<OnlineRedirectState>,
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let configuration = config.configuration.lock().unwrap();
    let online_redirect = online_redirect_state.redirect_state.lock().unwrap();
    if online_redirect.action == None {
        return http_redirect(redirect_to_keine_aktion_gefunden());
    }

    let action = online_redirect.action.clone().unwrap();
    let optimistic_locking_result = check_optimistic_locking_error(
        &action.database_version.as_string(),
        database.db_version.clone(),
    );
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let action_result: RedirectAuthenticatedResult;

    let credentials = LoginCredentials {
        username: query.user.to_string(),
        session_cookie: Cookie::from_session_str(query.session.clone()),
    };

    match action.typ {
        OnlineRedirectActionType::ImportEinzelbuchungen => {
            action_result = import_einzelbuchungen_request(
                &configuration,
                credentials,
                configuration.user_configuration.self_name.clone(),
                &database,
            )
            .await;
        }
        OnlineRedirectActionType::UploadKategorien => {
            action_result = upload_kategorien(&configuration, credentials, &database).await;
        }
        OnlineRedirectActionType::ImportGemeinsameBuchungen => {
            action_result = import_gemeinsame_buchungen_request(
                &configuration,
                credentials,
                configuration.user_configuration.self_name.clone(),
                &database,
            )
            .await;
        }
        OnlineRedirectActionType::UploadGemeinsameBuchungen => {
            action_result =
                export_gemeinsame_buchungen_request(&configuration, credentials, &database).await;
        }
    }
    if let Some(next_state) = action_result.database_to_save {
        println!("saving database");

        create_database_backup(
            &database,
            &configuration.backup_configuration,
            today(),
            now(),
            "1_before_import",
        );
        *database = update_database(&configuration.database_configuration, next_state);
        create_database_backup(
            &database,
            &configuration.backup_configuration,
            today(),
            now(),
            "2_after_import",
        );
        drop(database);
    }

    match action_result.page_render_type {
        RedirectAuthenticatedRenderPageType::RenderPage(page) => HttpResponse::Ok().body(page),
        RedirectAuthenticatedRenderPageType::Redirect(url) => http_redirect(url),
    }
}

#[derive(Deserialize)]
pub struct RedirectAuthenticatedQuery {
    pub user: String,
    pub session: String,
}

pub struct RedirectAuthenticatedResult {
    pub database_to_save: Option<Database>,
    pub page_render_type: RedirectAuthenticatedRenderPageType,
}

pub enum RedirectAuthenticatedRenderPageType {
    RenderPage(String),
    Redirect(Redirect),
}
