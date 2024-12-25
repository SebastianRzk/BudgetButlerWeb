use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::person::Person;
use crate::model::remote::server::ServerConfiguration;
use crate::model::state::config::{
    AbrechnungsConfiguration, BackupConfiguration, Configuration, DatabaseConfiguration,
    DesignConfiguration, ErfassungsConfiguration, UserConfiguration,
};
use std::path::PathBuf;

pub fn generate_initial_config(root_path: &PathBuf) -> Configuration {
    let initial_user_name_str = "Test_User";
    Configuration {
        database_configuration: DatabaseConfiguration {
            name: initial_user_name_str.to_string(),
            location: root_path.to_str().unwrap().to_string(),
        },
        abrechnungs_configuration: AbrechnungsConfiguration {
            location: "data/abrechnungen".to_string(),
        },
        backup_configuration: BackupConfiguration {
            location: "data/backups".to_string(),
            import_backup_location: "data/backups/import_backup".to_string(),
        },
        design_configuration: DesignConfiguration {
            design_farbe: Farbe {
                as_string: "#1c71d8".to_string(),
            },
            configurierte_farben: vec![
                Farbe {
                    as_string: "#1a5fb4".to_string(),
                },
                Farbe {
                    as_string: "#26a269".to_string(),
                },
                Farbe {
                    as_string: "#e5a50a".to_string(),
                },
                Farbe {
                    as_string: "#c64600".to_string(),
                },
                Farbe {
                    as_string: "#a51d2d".to_string(),
                },
                Farbe {
                    as_string: "#613583".to_string(),
                },
                Farbe {
                    as_string: "#63452c".to_string(),
                },
                Farbe {
                    as_string: "#9a9996".to_string(),
                },
                Farbe {
                    as_string: "#99c1f1".to_string(),
                },
                Farbe {
                    as_string: "#8ff0a4".to_string(),
                },
                Farbe {
                    as_string: "#f9f06b".to_string(),
                },
                Farbe {
                    as_string: "#ffbe6f".to_string(),
                },
                Farbe {
                    as_string: "#f66151".to_string(),
                },
                Farbe {
                    as_string: "#dc8add".to_string(),
                },
                Farbe {
                    as_string: "#cdab8f".to_string(),
                },
                Farbe {
                    as_string: "ffffff".to_string(),
                },
                Farbe {
                    as_string: "77767b".to_string(),
                },
            ],
        },
        server_configuration: ServerConfiguration {
            server_url: "http://localhost:8081".to_string(),
        },
        user_configuration: UserConfiguration {
            self_name: Person::new(initial_user_name_str.to_string()),
            partner_name: Person::new("kein_Partnername_gesetzt".to_string()),
        },
        erfassungs_configuration: ErfassungsConfiguration {
            ausgeschlossene_kategorien: vec![],
        },
    }
}
