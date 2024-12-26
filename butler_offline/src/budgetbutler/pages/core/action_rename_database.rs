use crate::model::primitives::person::Person;
use crate::model::state::config::{Configuration, DatabaseConfiguration, UserConfiguration};
use crate::model::state::persistent_application_state::Database;

pub struct RenameDatabaseContext<'a> {
    pub new_database_name: String,
    pub database: &'a Database,
    pub config: &'a Configuration,
}

pub struct SettingsAndDatabaseChangeViewResult {
    pub new_database: Database,
    pub new_config: Configuration,
}

pub fn action_rename_database(
    context: RenameDatabaseContext,
) -> SettingsAndDatabaseChangeViewResult {
    let aktuelle_person = context.config.user_configuration.self_name.clone();
    let neue_person = Person::new(context.new_database_name.clone());

    let neue_gemeinsame_buchungen = context
        .database
        .gemeinsame_buchungen
        .change()
        .rename_person(aktuelle_person.clone(), neue_person.clone());
    let neue_datenbank = context
        .database
        .change_gemeinsame_buchungen(neue_gemeinsame_buchungen);

    SettingsAndDatabaseChangeViewResult {
        new_database: neue_datenbank,
        new_config: Configuration {
            database_configuration: DatabaseConfiguration {
                name: context.new_database_name.clone(),
                location: context.config.database_configuration.location.clone(),
            },
            erfassungs_configuration: context.config.erfassungs_configuration.clone(),
            user_configuration: UserConfiguration {
                self_name: neue_person,
                partner_name: context.config.user_configuration.partner_name.clone(),
            },
            abrechnungs_configuration: context.config.abrechnungs_configuration.clone(),
            backup_configuration: context.config.backup_configuration.clone(),
            design_configuration: context.config.design_configuration.clone(),
            server_configuration: context.config.server_configuration.clone(),
        },
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::core::action_rename_database::{
        action_rename_database, RenameDatabaseContext,
    };
    use crate::model::database::gemeinsame_buchung::builder::gemeinsame_buchung_mit_person;
    use crate::model::primitives::person::builder::person;
    use crate::model::state::config::builder::{
        leere_abrechnungs_configuration, leere_backup_configuration, leere_design_configuration,
        leere_erfassungs_configuration, leere_server_configuration,
    };
    use crate::model::state::config::{Configuration, DatabaseConfiguration, UserConfiguration};
    use crate::model::state::persistent_application_state::builder::generate_database_with_gemeinsamen_buchungen;

    #[test]
    fn test_action_rename_database() {
        let database = generate_database_with_gemeinsamen_buchungen(vec![
            gemeinsame_buchung_mit_person("to rename"),
            gemeinsame_buchung_mit_person("not to rename"),
        ]);

        let configuration = Configuration {
            database_configuration: DatabaseConfiguration {
                name: "to rename".to_string(),
                location: "demo/".to_string(),
            },
            server_configuration: leere_server_configuration(),
            erfassungs_configuration: leere_erfassungs_configuration(),
            user_configuration: UserConfiguration {
                self_name: person("to rename"),
                partner_name: person("partner"),
            },
            design_configuration: leere_design_configuration(),
            abrechnungs_configuration: leere_abrechnungs_configuration(),
            backup_configuration: leere_backup_configuration(),
        };

        let context = RenameDatabaseContext {
            new_database_name: "renamed".to_string(),
            database: &database,
            config: &configuration,
        };

        let result = action_rename_database(context);

        assert_eq!(
            result
                .new_database
                .gemeinsame_buchungen
                .gemeinsame_buchungen[0]
                .value
                .person
                .person,
            "renamed"
        );
        assert_eq!(
            result
                .new_database
                .gemeinsame_buchungen
                .gemeinsame_buchungen[1]
                .value
                .person
                .person,
            "not to rename"
        );

        assert_eq!(result.new_config.database_configuration.name, "renamed");
        assert_eq!(result.new_config.database_configuration.location, "demo/");

        assert_eq!(
            result.new_config.user_configuration.self_name.person,
            "renamed"
        );
    }
}
