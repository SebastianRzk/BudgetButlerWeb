use crate::budgetbutler::pages::sparen::action_add_edit_depotauszug::{
    submit_depotauszug, Auszug, Mode, SubmitDepotauszugContext,
};
use crate::budgetbutler::pages::sparen::action_delete_depotauszug::{
    delete_depotauszug, DeleteContext,
};
use crate::budgetbutler::pages::sparen::add_depotauszug::{
    handle_view, AddDepotauszugContext, EditDepotauszug,
};
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::{
    redirect_to_depotauszug_bereits_erfasst, redirect_to_optimistic_locking_error,
};
use crate::budgetbutler::view::request_handler::{
    handle_modification, handle_render_display_view, VersionedContext,
};
use crate::budgetbutler::view::routes::SPAREN_DEPOTAUSZUG_ADD;
use crate::io::html::views::sparen::add_depotauszug::render_add_depotauszug_template;
use crate::io::http::redirect::http_redirect;
use crate::io::time::today;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::state::config::ConfigurationData;
use crate::model::state::non_persistent_application_state::DepotauszuegeChanges;
use crate::model::state::persistent_application_state::ApplicationState;
use actix_web::web::{Data, Form};
use actix_web::{get, post, HttpResponse, Responder};
use serde::Deserialize;
use std::collections::HashMap;

#[get("add_depotauszug/")]
pub async fn get_view(
    data: Data<ApplicationState>,
    depotauszuege_changes: Data<DepotauszuegeChanges>,
    config: Data<ConfigurationData>,
) -> impl Responder {
    let database_guard = data.database.lock().unwrap();
    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Neuer Depotauszug hinzufügen",
        SPAREN_DEPOTAUSZUG_ADD,
        AddDepotauszugContext {
            database: &database_guard,
            depotwerte_changes: &depotauszuege_changes.changes.lock().unwrap(),
            edit_buchung: None,
            heute: today(),
        },
        handle_view,
        render_add_depotauszug_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[post("add_depotauszug/")]
pub async fn post_view(
    data: Data<ApplicationState>,
    depotauszuege_changes: Data<DepotauszuegeChanges>,
    form: Form<EditFormData>,
    config: Data<ConfigurationData>,
) -> HttpResponse {
    let database_guard = data.database.lock().unwrap();
    let optimistic_locking_result =
        check_optimistic_locking_error(&form.database_version, database_guard.db_version.clone());
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return http_redirect(redirect_to_optimistic_locking_error());
    }

    let configuration_guard = config.configuration.lock().unwrap();
    HttpResponse::Ok().body(handle_render_display_view(
        "Depotauszug editieren",
        SPAREN_DEPOTAUSZUG_ADD,
        AddDepotauszugContext {
            database: &database_guard,
            depotwerte_changes: &depotauszuege_changes.changes.lock().unwrap(),
            edit_buchung: Some(EditDepotauszug {
                datum: Datum::from_iso_string(&form.edit_datum.clone()),
                konto_referenz: KontoReferenz::new(Name::new(form.edit_konto_name.clone())),
            }),
            heute: today(),
        },
        handle_view,
        render_add_depotauszug_template,
        configuration_guard.database_configuration.name.clone(),
    ))
}

#[derive(Deserialize)]
struct EditFormData {
    edit_datum: String,
    edit_konto_name: String,
    database_version: String,
}

#[post("add_depotauszug/submit")]
pub async fn post_submit(
    data: Data<ApplicationState>,
    depotauszuege_changes: Data<DepotauszuegeChanges>,
    form_data: Form<HashMap<String, String>>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();
    let konto = KontoReferenz::new(Name::new(form_data.get("edit_konto_name").unwrap().clone()));
    let datum = Datum::from_iso_string(form_data.get("edit_datum").unwrap());
    let database_version = form_data.get("database_version").unwrap().clone();

    eprintln!("Form data: {:?}", form_data);
    let add = "yes".to_string();
    let mode = if form_data.get("edit").is_some() && form_data.get("edit").unwrap() == &add {
        Mode::Edit
    } else {
        Mode::Add
    };

    if mode == Mode::Add
        && database
            .depotauszuege
            .select()
            .existiert_auszug(konto.clone(), datum.clone())
    {
        return http_redirect(redirect_to_depotauszug_bereits_erfasst());
    }

    let relevante_auszuege = extract_relevante_auszuege(
        extract_new_depotwerte(&form_data),
        extract_edit_depotwerte(&form_data),
    );

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: database_version,
            current_db_version: database.db_version.clone(),
            context: SubmitDepotauszugContext {
                database: &database,
                konto,
                datum,
                mode,
                auszuege: relevante_auszuege,
            },
        },
        &depotauszuege_changes.changes,
        submit_depotauszug,
        &configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

fn extract_edit_depotwerte(mapper: &HashMap<String, String>) -> Vec<Auszug> {
    let prefix = "wert_changed_";
    extract_auszug(mapper, prefix)
}

fn extract_new_depotwerte(mapper: &HashMap<String, String>) -> Vec<Auszug> {
    let prefix = "wert_new_";
    extract_auszug(mapper, prefix)
}

fn extract_relevante_auszuege(new: Vec<Auszug>, edit: Vec<Auszug>) -> Vec<Auszug> {
    let mut result = edit.clone();

    for new_auszug in new {
        if new_auszug.wert.as_cent() != 0 {
            result.push(new_auszug);
        }
    }

    result
}

fn extract_auszug(mapper: &HashMap<String, String>, prefix: &str) -> Vec<Auszug> {
    let mut konten = Vec::new();
    for (key, value) in mapper.iter() {
        if key.starts_with(prefix) {
            let isin = key.replace(prefix, "");
            let wert = Betrag::from_user_input(value);
            konten.push(Auszug {
                depotwert_referenz: DepotwertReferenz::new(ISIN::new(isin)),
                wert,
            });
        }
    }

    konten
}

#[post("add_depotauszug/delete")]
pub async fn delete(
    data: Data<ApplicationState>,
    depotauszug_changes: Data<DepotauszuegeChanges>,
    form_data: Form<DeleteFormData>,
    configuration: Data<ConfigurationData>,
) -> impl Responder {
    let mut database = data.database.lock().unwrap();

    let new_state = handle_modification(
        VersionedContext {
            requested_db_version: form_data.database_version.clone(),
            current_db_version: database.db_version.clone(),
            context: DeleteContext {
                database: &database,
                delete_konto: KontoReferenz::new(Name::new(form_data.konto_name.clone())),
                delete_datum: Datum::from_iso_string(&form_data.datum),
            },
        },
        &depotauszug_changes.changes,
        delete_depotauszug,
        &configuration
            .configuration
            .lock()
            .unwrap()
            .database_configuration,
    );
    *database = new_state.changed_database;

    drop(database);

    http_redirect(new_state.target)
}

#[derive(Deserialize)]
struct DeleteFormData {
    konto_name: String,
    datum: String,
    database_version: String,
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::action_add_edit_depotauszug::Auszug;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::isin::ISIN;
    use std::collections::{HashMap, HashSet};

    #[test]
    fn test_extract_edit_depotwerte() {
        let mut mapper = HashMap::new();
        mapper.insert("wert_changed_DE123".to_string(), "123".to_string());
        mapper.insert("something other".to_string(), "123".to_string());

        let result = super::extract_edit_depotwerte(&mapper);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].depotwert_referenz.isin, isin("DE123"));
        assert_eq!(result[0].wert, Betrag::new(Vorzeichen::Positiv, 123, 0));
    }

    #[test]
    fn test_extract_new_depotwerte() {
        let mut mapper = HashMap::new();
        mapper.insert("wert_new_DE123".to_string(), "123".to_string());
        mapper.insert("something other".to_string(), "123".to_string());

        let result = super::extract_new_depotwerte(&mapper);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].depotwert_referenz.isin, isin("DE123"));
        assert_eq!(result[0].wert, Betrag::new(Vorzeichen::Positiv, 123, 0));
    }

    #[test]
    fn test_extract_relevante_auszuege() {
        let mut mapper = HashMap::new();
        mapper.insert("wert_new_DE123".to_string(), "123".to_string());
        mapper.insert("something other".to_string(), "123".to_string());

        let result = super::extract_relevante_auszuege(
            vec![
                Auszug {
                    depotwert_referenz: depotwert_referenz("NEU123"),
                    wert: Betrag::zero(),
                },
                Auszug {
                    depotwert_referenz: depotwert_referenz("NEU223"),
                    wert: vier(),
                },
            ],
            vec![
                Auszug {
                    depotwert_referenz: depotwert_referenz("EDIT123"),
                    wert: Betrag::zero(),
                },
                Auszug {
                    depotwert_referenz: depotwert_referenz("EDIT223"),
                    wert: zwei(),
                },
            ],
        );

        assert_eq!(result.len(), 3);
        let isins: HashSet<ISIN> = result
            .iter()
            .map(|x| x.depotwert_referenz.isin.clone())
            .collect();
        assert!(isins.contains(&isin("NEU223")));
        assert!(isins.contains(&isin("EDIT123")));
        assert!(isins.contains(&isin("EDIT223")));
    }
}
