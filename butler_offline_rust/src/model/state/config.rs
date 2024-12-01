use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::person::Person;
use crate::model::remote::server::ServerConfiguration;

pub struct Config {
    pub database_configuration: DatabaseConfiguration,
    pub design_configuration: DesignConfiguration,
    pub user_configuration: UserConfiguration,
    pub abrechnungs_configuration: AbrechnungsConfiguration,
    pub backup_configuration: BackupConfiguration,
    pub server_configuration: ServerConfiguration,
}

pub struct DatabaseConfiguration {
    pub name: String,
    pub location: String,
}

pub struct DesignConfiguration {
    pub configurierte_farben: Vec<Farbe>,
    pub design_farbe: Farbe
}

#[derive(Clone)]
pub struct UserConfiguration {
    pub self_name: Person,
    pub partner_name: Person,
}

#[derive(Clone)]
pub struct AbrechnungsConfiguration {
    pub location: String,
}


#[derive(Clone)]
pub struct BackupConfiguration {
    pub location: String,
}

impl BackupConfiguration {

    pub fn to_database_configuration(&self, database_name: String) -> DatabaseConfiguration {
        DatabaseConfiguration {
            name: database_name,
            location: self.location.clone(),
        }
    }

}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::person::builder::{demo_partner, demo_self};
    use crate::model::state::config::UserConfiguration;

    pub fn demo_user_configuration() -> UserConfiguration {
        UserConfiguration {
            self_name: demo_self(),
            partner_name: demo_partner(),
        }
    }
}


#[cfg(test)]
pub mod tests {

    #[test]
    fn test_backup_configuration_to_database_configuration(){
        let backup_configuration = super::BackupConfiguration {
            location: "demo/backups".to_string(),
        };

        let database_configuration = backup_configuration.to_database_configuration("testname".to_string());

        assert_eq!(database_configuration.name, "testname");
        assert_eq!(database_configuration.location, "demo/backups");
    }
}