use crate::budgetbutler::database::abrechnen::abrechnen::importer::pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::budgetbutler::pages::shared::import::{
    handle_import_abrechnung, ImportAbrechnungContext,
};
use crate::budgetbutler::view::request_handler::{
    handle_modification_manual, handle_render_display_view, no_page_middleware, SuccessMessage,
};
use crate::budgetbutler::view::routes::CORE_IMPORT;
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::writer::create_database_backup;
use crate::io::html::views::shared::export_import::{
    render_import_template, ExportImportViewResult,
};
use crate::io::html::views::shared::import_mapping::{render_import_mapping_template, ImportMappingViewResult};
use crate::io::time::{now, today};
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;

#[get("import/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    let context = ExportImportViewResult {
        database_version: database.db_version.clone(),
        online_default_server: configuration_guard.server_configuration.clone(),
    };
    HttpResponse::Ok().body(handle_render_display_view(
        "Gemeinsame Buchungen Abrechnen",
        CORE_IMPORT,
        context,
        no_page_middleware,
        render_import_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("import/submit/")]
pub async fn submit_import_manuell(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    form: Form<ImportManualFormData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let configuration = config.configuration.lock().unwrap();

    let abrechnungs_file = Line::from_multiline_str(form.import.clone());
    let abrechnung = Abrechnung::new(abrechnungs_file.clone());

    let pruefe_kategorien =
        pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind(&database, &abrechnung);
    if pruefe_kategorien.kategorien_nicht_in_datenbank.len() > 0 {
        let view_result = ImportMappingViewResult {
            database_version: database.db_version.clone(),
            abrechnung,
            alle_kategorien: database.einzelbuchungen.get_kategorien(),
            unpassende_kategorien: pruefe_kategorien.kategorien_nicht_in_datenbank,
        };
        return HttpResponse::Ok().body(handle_render_display_view(
            "Kategorien zuordnen",
            CORE_IMPORT,
            view_result,
            no_page_middleware,
            render_import_mapping_template,
            configuration.database_configuration.name.clone(),
        ));
    }

    let original_database_version = database.db_version.clone();
    let context = ImportAbrechnungContext {
        database: &database,
        abrechnung,
        heute: today(),
    };

    let result = handle_import_abrechnung(context);
    let view_result = ExportImportViewResult {
        database_version: result.database.db_version.clone(),
        online_default_server: configuration.server_configuration.clone(),
    };

    let render_result = handle_modification_manual(
        form.database_id.clone(),
        original_database_version,
        CORE_IMPORT,
        "Gemeinsame Buchungen Importieren",
        view_result,
        render_import_template,
        &configuration.database_configuration,
        result.database,
        SuccessMessage {
            message: format!(
                "Erfolgreich {} Einzelbuchungen und {} Gemeinsame Buchungen importiert",
                result.diff_einzelbuchungen, result.diff_gemeinsame_buchungen
            ),
        },
    );

    if let Some(next_state) = render_result.valid_next_state {
        create_database_backup(
            &database,
            &configuration.backup_configuration,
            today(),
            now(),
            "1_before_import",
        );

        *database = next_state;

        create_database_backup(
            &database,
            &configuration.backup_configuration,
            today(),
            now(),
            "2_after_import",
        );
        speichere_abrechnung(
            result.aktualisierte_abrechnung.clone(),
            configuration.user_configuration.self_name.clone(),
            configuration.abrechnungs_configuration.clone(),
            today(),
            now(),
        );
    }

    HttpResponse::Ok().body(render_result.full_rendered_page)
}

#[derive(Deserialize)]
struct ImportManualFormData {
    database_id: String,
    import: String,
}