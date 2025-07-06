use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::budgetbutler::database::abrechnen::persoenliche_buchungen_abrechnen::importer::pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind;
use crate::budgetbutler::pages::shared::import::{handle_import_abrechnung, ImportAbrechnungContext};
use crate::budgetbutler::view::menu::resolve_active_group_from_url;
use crate::budgetbutler::view::request_handler::{handle_modification_manual, handle_render_display_view, no_page_middleware, ActivePage, ManualRenderResult};
use crate::budgetbutler::view::routes::{CORE_IMPORT, UNKNOWN};
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::writer::create_database_backup;
use crate::io::html::views::core::zurueck_zu::{render_success_message_template, SuccessZurueckZuViewResult};
use crate::io::html::views::index::{render_index_template, PageTitle};
use crate::io::html::views::shared::export_import::{
    render_import_template, ExportImportViewResult,
};
use crate::io::html::views::shared::import_mapping::{render_import_mapping_template, ImportMappingViewResult};
use crate::io::time::{now, today};
use crate::model::state::config::{Configuration, ConfigurationData};
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;
use std::sync::MutexGuard;

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
    let database_name = configuration_guard.database_configuration.name.clone();
    let active_page = ActivePage::construct_from_url(CORE_IMPORT);
    let view_result = no_page_middleware(context);
    let render_view = render_import_template(view_result);
    HttpResponse::Ok().body(handle_render_display_view(
        PageTitle::new("Gemeinsame Buchungen Abrechnen"),
        active_page,
        database_name,
        render_view,
    ))
}

#[post("import/submit/")]
pub async fn submit_import_manuell(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    user_application_directory: Data<UserApplicationDirectory>,
    form: Form<ImportManualFormData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let configuration = config.configuration.lock().unwrap();

    let abrechnungs_file = Line::from_multiline_str(form.import.clone());
    let abrechnung = Abrechnung::new(abrechnungs_file.clone());

    let pruefe_kategorien =
        pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind(&database, &abrechnung);
    if !pruefe_kategorien.kategorien_nicht_in_datenbank.is_empty() {
        let view_result = ImportMappingViewResult {
            database_version: database.db_version.clone(),
            abrechnung,
            alle_kategorien: database.einzelbuchungen.get_kategorien(),
            unpassende_kategorien: pruefe_kategorien.kategorien_nicht_in_datenbank,
        };
        let database_name = configuration.database_configuration.name.clone();
        let active_page = ActivePage::construct_from_url(CORE_IMPORT);
        let view_result1 = no_page_middleware(view_result);
        let render_view = render_import_mapping_template(view_result1);
        return HttpResponse::Ok().body(handle_render_display_view(
            PageTitle::new("Kategorien zuordnen"),
            active_page,
            database_name,
            render_view,
        ));
    }

    let original_database_version = database.db_version.clone();
    let context = ImportAbrechnungContext {
        database: &database,
        abrechnung,
        heute: today(),
    };

    let result = handle_import_abrechnung(context);

    let render_result = handle_modification_manual(
        form.database_id.clone(),
        original_database_version,
        &configuration.database_configuration,
        result.database,
        &user_application_directory,
    );

    if let Ok(next_state) = render_result.valid_next_state {
        create_database_backup(
            &database,
            &configuration.backup_configuration,
            &user_application_directory,
            today(),
            now(),
            "1_before_import",
        );

        *database = next_state;

        create_database_backup(
            &database,
            &configuration.backup_configuration,
            &user_application_directory,
            today(),
            now(),
            "2_after_import",
        );
        speichere_abrechnung(
            &user_application_directory,
            result.aktualisierte_abrechnung.clone(),
            configuration.user_configuration.self_name.clone(),
            configuration.abrechnungs_configuration.clone(),
            today(),
            now(),
        );
        return erfolgreich_importiert(
            &configuration,
            result.diff_einzelbuchungen,
            result.diff_gemeinsame_buchungen,
        );
    }
    render_as_locking_error(&configuration, render_result)
}

pub fn render_as_locking_error(
    configuration: &Configuration,
    render_result: ManualRenderResult,
) -> HttpResponse {
    let active_page = ActivePage::construct_from_url(UNKNOWN);
    HttpResponse::Ok().body(render_index_template(
        resolve_active_group_from_url(&active_page),
        active_page,
        PageTitle::new("Error"),
        render_result.valid_next_state.err().unwrap(),
        None,
        configuration.database_configuration.name.clone(),
    ))
}

pub fn erfolgreich_importiert(
    configuration: &MutexGuard<Configuration>,
    diff_einzelbuchungen: usize,
    diff_gemeinsame_buchungen: usize,
) -> HttpResponse {
    let active_page = ActivePage::construct_from_url(CORE_IMPORT);
    HttpResponse::Ok().body(render_index_template(
        resolve_active_group_from_url(&active_page),
        active_page,
        PageTitle::new("Export / Import"),
        render_success_message_template(SuccessZurueckZuViewResult {
            text: format!(
                "Erfolgreich {diff_einzelbuchungen} Einzelbuchungen und {diff_gemeinsame_buchungen} Gemeinsame Buchungen importiert. Zurück zu Export / Import"
            ),
            link: CORE_IMPORT.to_string(),
        }),
        None,
        configuration.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct ImportManualFormData {
    database_id: String,
    import: String,
}
