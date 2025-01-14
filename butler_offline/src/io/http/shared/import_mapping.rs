use crate::budgetbutler::database::abrechnen::abrechnen::importer::aktualisiere_kategorien;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::budgetbutler::pages::shared::import::{handle_import_abrechnung, ImportAbrechnungContext};
use crate::budgetbutler::view::request_handler::handle_modification_manual;
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::writer::create_database_backup;
use crate::io::html::views::shared::import_mapping::ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT;
use crate::io::http::shared::export_import::{erfolgreich_importiert, render_as_locking_error};
use crate::io::time::{now, today};
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::config::ConfigurationData;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{post, Responder};
use std::collections::HashMap;
use std::string::ToString;

#[post("import/mapping")]
pub async fn submit_import_mapping(
    data: Data<ApplicationState>,
    config: Data<ConfigurationData>,
    form: Form<HashMap<String, String>>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let configuration = config.configuration.lock().unwrap();
    let abrechnung_str = form.get("abrechnung").unwrap().to_string();
    let database_id = form.get("database_id").unwrap().to_string();
    let mut mappings: HashMap<Kategorie, Kategorie> = HashMap::new();

    for moegliches_mapping in form.keys() {
        let value = form.get(moegliches_mapping).unwrap();
        if moegliches_mapping.ends_with("_mapping") && value != ALS_NEUE_KATEGORIE_IMPORTIEREN_TEXT
        {
            let kategorie = moegliches_mapping.replace("_mapping", "");
            let mapping = form.get(moegliches_mapping).unwrap().to_string();
            mappings.insert(Kategorie::new(kategorie), Kategorie::new(mapping));
        }
    }

    let aktualisierte_abrechung = aktualisiere_kategorien(
        Abrechnung::new(Line::from_multiline_str(abrechnung_str)),
        mappings,
    );

    let original_database_version = database.db_version.clone();
    let context = ImportAbrechnungContext {
        database: &database,
        abrechnung: aktualisierte_abrechung,
        heute: today(),
    };

    let result = handle_import_abrechnung(context);

    let render_result = handle_modification_manual(
        database_id.clone(),
        original_database_version,
        &configuration.database_configuration,
        result.database,
    );

    if let Ok(next_state) = render_result.valid_next_state {
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
        return erfolgreich_importiert(
            &configuration,
            result.diff_einzelbuchungen,
            result.diff_gemeinsame_buchungen,
        );
    }
    render_as_locking_error(&configuration, render_result)
}
