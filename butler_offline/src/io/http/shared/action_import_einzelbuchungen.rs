use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::{Abrechnung, Titel};
use crate::budgetbutler::database::abrechnen::persoenliche_buchungen_abrechnen::abrechnung_text_generator::{generiere_text, EinfuehrungsText, HeaderInsertModus, Metadaten, Ziel};
use crate::budgetbutler::database::abrechnen::persoenliche_buchungen_abrechnen::einzel_buchungen_text_generator::einzelbuchungen_as_import_text;
use crate::budgetbutler::database::abrechnen::persoenliche_buchungen_abrechnen::importer::{import_abrechnung, pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind};
use crate::budgetbutler::view::request_handler::{handle_render_display_view, handle_render_success_display_message, no_page_middleware, ActivePage, DisplaySuccessMessage};
use crate::budgetbutler::view::routes::CORE_IMPORT;
use crate::io::disk::abrechnung::speichere_abrechnung::speichere_abrechnung;
use crate::io::disk::diskrepresentation::line::as_string;
use crate::io::html::views::index::PageTitle;
use crate::io::html::views::shared::import_mapping::{render_import_mapping_template, ImportMappingViewResult};
use crate::io::http::shared::redirect_authenticated::{RedirectAuthenticatedRenderPageType, RedirectAuthenticatedResult};
use crate::io::online::begleiterapp::delete_einzelbuchungen::delete_einzelbuchungen;
use crate::io::online::begleiterapp::get_einzelbuchungen::request_einzelbuchungen;
use crate::io::time::{now, today};
use crate::model::primitives::person::Person;
use crate::model::remote::login::LoginCredentials;
use crate::model::state::config::{AbrechnungsConfiguration, Configuration};
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::persistent_application_state::Database;

pub async fn import_einzelbuchungen_request(
    config: &Configuration,
    login: LoginCredentials,
    eigener_name: Person,
    database: &Database,
    user_application_directory: &UserApplicationDirectory,
) -> RedirectAuthenticatedResult {
    let einzelbuchungen =
        request_einzelbuchungen(&config.server_configuration, login.clone()).await;
    match einzelbuchungen {
        Ok(einzelbuchungen) => {
            println!("{einzelbuchungen:?}");
            let abrechnung = Abrechnung {
                lines: generiere_text(
                    EinfuehrungsText { lines: vec![] },
                    einzelbuchungen_as_import_text(&einzelbuchungen),
                    Metadaten {
                        titel: Titel {
                            titel: "Import von Einzelbuchungen aus der App".to_string(),
                        },
                        ziel: Ziel::ImportBuchungenAusApp,
                        abrechnungsdatum: today(),
                        abrechnende_person: eigener_name.clone(),
                        ausfuehrungsdatum: today(),
                    },
                    HeaderInsertModus::Insert,
                ),
            };
            let abrechnung_str = as_string(&abrechnung.lines);

            speichere_abrechnung(
                user_application_directory,
                abrechnung.lines.clone(),
                eigener_name.clone(),
                AbrechnungsConfiguration {
                    location: config.backup_configuration.import_backup_location.clone(),
                },
                today(),
                now(),
            );
            delete_einzelbuchungen(&config.server_configuration, login)
                .await
                .unwrap();

            println!("Abrechnung zu Import:\n{abrechnung_str}");

            let pruefe_kategorien =
                pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind(database, &abrechnung);
            return if !pruefe_kategorien.kategorien_nicht_in_datenbank.is_empty() {
                let view_result = ImportMappingViewResult {
                    database_version: database.db_version.clone(),
                    abrechnung,
                    alle_kategorien: database.einzelbuchungen.get_kategorien(),
                    unpassende_kategorien: pruefe_kategorien.kategorien_nicht_in_datenbank,
                };
                let database_name = config.database_configuration.name.clone();
                let active_page = ActivePage::construct_from_url(CORE_IMPORT);
                let view_result1 = no_page_middleware(view_result);
                let render_view = render_import_mapping_template(view_result1);
                RedirectAuthenticatedResult {
                    database_to_save: None,
                    page_render_type: RedirectAuthenticatedRenderPageType::RenderPage(
                        handle_render_display_view(
                            PageTitle::new("Kategorien zuordnen"),
                            active_page,
                            database_name,
                            render_view,
                        ),
                    ),
                }
            } else {
                println!("Keine Kategorien zum zuordnen");
                speichere_abrechnung(
                    user_application_directory,
                    abrechnung.lines.clone(),
                    eigener_name,
                    config.abrechnungs_configuration.clone(),
                    today(),
                    now(),
                );

                let database = import_abrechnung(database, &abrechnung);
                let database_name = config.database_configuration.name.clone();
                let context = DisplaySuccessMessage {
                    message: format!(
                        "Erfolgreich {} Einzelbuchungen importiert",
                        einzelbuchungen.len()
                    ),
                    link_name: "Zurück zu Import / Export".to_string(),
                    link_url: CORE_IMPORT.to_string(),
                };
                RedirectAuthenticatedResult {
                    database_to_save: Some(database),
                    page_render_type: RedirectAuthenticatedRenderPageType::RenderPage(
                        handle_render_success_display_message(
                            "Import von Einzelbuchungen",
                            ActivePage::construct_from_url(CORE_IMPORT),
                            database_name,
                            context,
                        ),
                    ),
                }
            };
        }
        Err(_) => {
            println!("Error");
        }
    };

    RedirectAuthenticatedResult {
        database_to_save: None,
        page_render_type: RedirectAuthenticatedRenderPageType::RenderPage(
            format!("Sone {:?}", "asd").to_string(),
        ),
    }
}
