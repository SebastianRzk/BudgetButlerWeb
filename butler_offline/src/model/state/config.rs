use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::person::Person;
use crate::model::remote::server::ServerConfiguration;
use serde::{Deserialize, Serialize};
use std::env::current_dir;
use std::path::{Path, PathBuf};
use std::sync::Mutex;

pub struct ConfigurationData {
    pub configuration: Mutex<Configuration>,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct Configuration {
    pub database_configuration: DatabaseConfiguration,
    pub design_configuration: DesignConfiguration,
    pub user_configuration: UserConfiguration,
    pub abrechnungs_configuration: AbrechnungsConfiguration,
    pub backup_configuration: BackupConfiguration,
    pub server_configuration: ServerConfiguration,
    pub erfassungs_configuration: ErfassungsConfiguration,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct DatabaseConfiguration {
    pub name: String,
    pub location: String,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct DesignConfiguration {
    pub configurierte_farben: Vec<Farbe>,
    pub design_farbe: Farbe,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct UserConfiguration {
    pub self_name: Person,
    pub partner_name: Person,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct ErfassungsConfiguration {
    pub ausgeschlossene_kategorien: Vec<Kategorie>,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct AbrechnungsConfiguration {
    pub location: String,
}

#[derive(Clone, Deserialize, Serialize)]
pub struct BackupConfiguration {
    pub location: String,
    pub import_backup_location: String,
}

impl BackupConfiguration {
    pub fn to_database_configuration(&self, database_name: String) -> DatabaseConfiguration {
        DatabaseConfiguration {
            name: database_name,
            location: self.location.clone(),
        }
    }
}

pub fn get_database_location(database_configuration: &DatabaseConfiguration) -> PathBuf {
    app_root()
        .join(Path::new(&database_configuration.location))
        .join(&format!("Database_{}.csv", database_configuration.name))
}

pub fn app_root() -> PathBuf {
    current_dir().unwrap().parent().unwrap().to_path_buf()
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::farbe::builder::any_farbe;
    use crate::model::primitives::person::builder::{demo_partner, demo_self};
    use crate::model::primitives::person::Person;
    use crate::model::remote::server::ServerConfiguration;
    use crate::model::state::config::{
        AbrechnungsConfiguration, BackupConfiguration, Configuration, DatabaseConfiguration,
        DesignConfiguration, ErfassungsConfiguration, UserConfiguration,
    };

    pub fn demo_configuration() -> Configuration {
        Configuration {
            database_configuration: leere_database_configuration(),
            server_configuration: leere_server_configuration(),
            erfassungs_configuration: leere_erfassungs_configuration(),
            user_configuration: demo_user_configuration(),
            design_configuration: leere_design_configuration(),
            abrechnungs_configuration: leere_abrechnungs_configuration(),
            backup_configuration: leere_backup_configuration(),
        }
    }

    pub fn demo_user_configuration() -> UserConfiguration {
        UserConfiguration {
            self_name: demo_self(),
            partner_name: demo_partner(),
        }
    }

    pub fn leere_design_configuration() -> DesignConfiguration {
        DesignConfiguration {
            configurierte_farben: vec![],
            design_farbe: any_farbe(),
        }
    }

    pub fn leere_user_configuration() -> UserConfiguration {
        UserConfiguration {
            self_name: Person::new("".to_string()),
            partner_name: Person::new("".to_string()),
        }
    }

    pub fn leere_erfassungs_configuration() -> ErfassungsConfiguration {
        ErfassungsConfiguration {
            ausgeschlossene_kategorien: vec![],
        }
    }

    pub fn leere_abrechnungs_configuration() -> AbrechnungsConfiguration {
        AbrechnungsConfiguration {
            location: "".to_string(),
        }
    }

    pub fn leere_backup_configuration() -> BackupConfiguration {
        BackupConfiguration {
            location: "".to_string(),
            import_backup_location: "".to_string(),
        }
    }

    pub fn leere_server_configuration() -> ServerConfiguration {
        ServerConfiguration {
            server_url: "".to_string(),
        }
    }

    pub fn leere_database_configuration() -> DatabaseConfiguration {
        DatabaseConfiguration {
            name: "".to_string(),
            location: "".to_string(),
        }
    }
}

#[cfg(test)]
pub mod tests {

    #[test]
    fn test_backup_configuration_to_database_configuration() {
        let backup_configuration = super::BackupConfiguration {
            location: "demo/backups".to_string(),
            import_backup_location: "demo/backups/import_backup".to_string(),
        };

        let database_configuration =
            backup_configuration.to_database_configuration("testname".to_string());

        assert_eq!(database_configuration.name, "testname");
        assert_eq!(database_configuration.location, "demo/backups");
    }
}
