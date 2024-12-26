use crate::budgetbutler::pages::core::action_rename_kategorie::{
    action_rename_kategorie, RenameKategorieContext,
};
use crate::budgetbutler::view::request_handler::{
    handle_modification_without_change, VersionedContext,
};
use crate::io::http::redirect::http_redirect;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, HttpResponse};
use serde::Deserialize;

#[post("configuration/submit/renamekategorie/")]
pub async fn submit(
    data: Data<ApplicationState>,
    configuration_data: Data<ConfigurationData>,
    form: Form<SubmitRenameKategorieFormData>,
) -> HttpResponse {
    let mut database = data.database.lock().unwrap();
    let conf = configuration_data.configuration.lock().unwrap();

    let new_state = handle_modification_without_change(
        VersionedContext {
            requested_db_version: form.database_id.clone(),
            current_db_version: database.db_version.clone(),
            context: RenameKategorieContext {
                database: &database,
                alte_kategorie: Kategorie::new(form.alte_kategorie.clone()),
                neue_kategorie: Kategorie::new(form.neue_kategorie.clone()),
            },
        },
        action_rename_kategorie,
        &conf.database_configuration,
    );

    *database = new_state.changed_database;
    drop(database);

    http_redirect(new_state.target)
}

#[derive(Deserialize)]
struct SubmitRenameKategorieFormData {
    alte_kategorie: String,
    neue_kategorie: String,
    database_id: String,
}
