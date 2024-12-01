use crate::budgetbutler::pages::shared::import::{handle_import_abrechnung, ImportAbrechnungContext};
use crate::budgetbutler::view::request_handler::{handle_modification_manual, handle_render_display_view, no_page_middleware, SuccessMessage};
use crate::budgetbutler::view::routes::CORE_IMPORT;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::html::views::shared::export_import::{render_import_template, ExportImportViewResult};
use crate::model::state::config::Config;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::writer::create_database_backup;
use crate::io::time::{now, today};

#[get("import/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    config: Data<Config>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let context = ExportImportViewResult {
        database_version: database.db_version.clone(),
        online_default_server: config.server_configuration.clone(),
    };
    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchungen Abrechnen",
        CORE_IMPORT,
        context,
        no_page_middleware,
        render_import_template,
    ))
}

#[post("import/submit/")]
pub async fn submit_import_manuell(
    data: Data<ApplicationState>,
    config: Data<Config>,
    form: Form<ImportManualFormData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    create_database_backup(
        &database,
        &config.backup_configuration,
        today(),
        now(),
        "1_before_import",
    );


    let abrechnugns_file = Line::from_multiline_str(form.import.clone());
    let original_database_version = database.db_version.clone();
    let context = ImportAbrechnungContext {
        database: &database,
        abrechnungs_file: abrechnugns_file,
        heute: today(),
    };

    let result = handle_import_abrechnung(context);
    let view_result = ExportImportViewResult {
        database_version: result.database.db_version.clone(),
        online_default_server: config.server_configuration.clone(),
    };
    speichere_abrechnung(
        result.aktualisierte_abrechnung.clone(),
        config.user_configuration.self_name.clone(),
        config.abrechnungs_configuration.clone(),
        today(),
        now(),
    );


    let render_result = handle_modification_manual(
        form.database_id.clone(),
        original_database_version,
        CORE_IMPORT,
        "Gemeinsame Buchungen Importieren",
        view_result,
        render_import_template,
        &config.database_configuration,
        result.database,
        SuccessMessage {
            message: format!("Erfolgreich {} Einzelbuchungen und {} Gemeinsame Buchungen importiert", result.diff_einzelbuchungen, result.diff_gemeinsame_buchungen),
        },
    );

    if let Some(next_state) = render_result.valid_next_state {
        *database = next_state;
        create_database_backup(
            &database,
            &config.backup_configuration,
            today(),
            now(),
            "2_after_import",
        );
    }

    HttpResponse::Ok().body(render_result.full_rendered_page)
}

#[derive(Deserialize)]
struct ImportManualFormData {
    database_id: String,
    import: String,
}