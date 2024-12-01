use crate::budgetbutler::database::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::dauerauftrag::Dauerauftrag;
use crate::model::einzelbuchung::Einzelbuchung;
use crate::model::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use std::sync::Mutex;
use rand::random;

pub struct ApplicationState {
    pub database: Mutex<Database>,
}

pub struct Database {
    pub db_version: DatabaseVersion,
    pub einzelbuchungen: Einzelbuchungen,
    pub dauerauftraege: Dauerauftraege,
    pub gemeinsame_buchungen: GemeinsameBuchungen,
}

pub struct DataOnDisk {
    pub einzelbuchungen: Vec<Einzelbuchung>,
    pub dauerauftraege: Vec<Dauerauftrag>,
    pub gemeinsame_buchungen: Vec<GemeinsameBuchung>,
}

#[derive(Clone)]
pub struct DatabaseVersion {
    pub name: String,
    pub version: u32,
    pub session_random: u32,
}

pub fn create_initial_database_version(name: String) -> DatabaseVersion {
    DatabaseVersion {
        name,
        version: 0,
        session_random: random(),
    }
}

impl DatabaseVersion {
    pub fn as_string(&self) -> String {
        format!("{}-{}-{}", self.name, self.version, self.session_random)
    }
    pub fn increment(&self) -> DatabaseVersion {
        DatabaseVersion {
            name: self.name.clone(),
            version: self.version + 1,
            session_random: self.session_random,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Einzelbuchungen {
    pub einzelbuchungen: Vec<Indiziert<Einzelbuchung>>,
}

impl Einzelbuchungen {
    pub fn select(&self) -> Selector<Indiziert<Einzelbuchung>> {
        Selector::new(self.einzelbuchungen.clone())
    }

    pub fn get(&self, index: u32) -> Indiziert<Einzelbuchung> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Einzelbuchung, Einzelbuchungen> {
        ChangeSelector {
            content: self.einzelbuchungen.clone(),
            output: None,
        }
    }

    pub fn sort(&self) -> Einzelbuchungen {
        let mut neue_buchungen = self.einzelbuchungen.clone();
        neue_buchungen.sort();

        Einzelbuchungen {
            einzelbuchungen: neue_buchungen,
        }
    }
}

impl Creates<Einzelbuchung, Einzelbuchungen> for Einzelbuchungen {
    fn create(item: Vec<Indiziert<Einzelbuchung>>) -> Einzelbuchungen {
        Einzelbuchungen {
            einzelbuchungen: item,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Dauerauftraege {
    pub dauerauftraege: Vec<Indiziert<Dauerauftrag>>,
}

impl Creates<Dauerauftrag, Dauerauftraege> for Dauerauftraege {
    fn create(item: Vec<Indiziert<Dauerauftrag>>) -> Dauerauftraege {
        Dauerauftraege {
            dauerauftraege: item,
        }
    }
}

impl Dauerauftraege {
    pub fn select(&self) -> Selector<Indiziert<Dauerauftrag>> {
        Selector::new(self.dauerauftraege.clone())
    }

    pub fn sort(&self) -> Dauerauftraege {
        let mut neue_buchungen = self.dauerauftraege.clone();
        neue_buchungen.sort();

        Dauerauftraege {
            dauerauftraege: neue_buchungen,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Dauerauftrag> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Dauerauftrag, Dauerauftraege> {
        ChangeSelector {
            content: self.dauerauftraege.clone(),
            output: None,
        }
    }
}

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct GemeinsameBuchungen {
    pub gemeinsame_buchungen: Vec<Indiziert<GemeinsameBuchung>>,
}

impl Creates<GemeinsameBuchung, GemeinsameBuchungen> for GemeinsameBuchungen {
    fn create(item: Vec<Indiziert<GemeinsameBuchung>>) -> GemeinsameBuchungen {
        GemeinsameBuchungen {
            gemeinsame_buchungen: item,
        }
    }
}

impl GemeinsameBuchungen {
    pub fn sort(&self) -> GemeinsameBuchungen {
        let mut neue_buchungen = self.gemeinsame_buchungen.clone();
        neue_buchungen.sort();

        GemeinsameBuchungen {
            gemeinsame_buchungen: neue_buchungen,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<GemeinsameBuchung> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn select(&self) -> Selector<Indiziert<GemeinsameBuchung>> {
        Selector::new(self.gemeinsame_buchungen.clone())
    }

    pub fn change(&self) -> ChangeSelector<GemeinsameBuchung, GemeinsameBuchungen> {
        ChangeSelector {
            content: self.gemeinsame_buchungen.clone(),
            output: None,
        }
    }
}

impl Database {
    pub fn change_einzelbuchungen(&self, einzelbuchungen: Einzelbuchungen) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen,
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
        }
    }
    pub fn change_dauerauftraege(&self, dauerauftraege: Dauerauftraege) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege,
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
        }
    }
    pub fn change_gemeinsame_buchungen(
        &self,
        gemeinsame_buchungen: GemeinsameBuchungen,
    ) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen,
        }
    }
}

#[cfg(test)]
pub mod builder {
    use super::{Dauerauftraege, Einzelbuchungen, GemeinsameBuchungen};
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::model::dauerauftrag::Dauerauftrag;
    use crate::model::einzelbuchung::Einzelbuchung;
    use crate::model::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::indiziert::Indiziert;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_application_state::{DataOnDisk, DatabaseVersion};

    pub fn generate_empty_database() -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
            },
            Datum::first(),
            empty_database_version(),
        )
    }

    pub fn generate_database_with_einzelbuchungen(
        einzelbuchungen: Vec<Einzelbuchung>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen,
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
            },
            Datum::first(),
            empty_database_version(),
        )
    }

    pub fn generate_database_with_dauerauftraege(
        dauerauftraege: Vec<Dauerauftrag>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege,
                gemeinsame_buchungen: vec![],
            },
            Datum::first(),
            empty_database_version(),
        )
    }

    pub fn generate_database_with_gemeinsamen_buchungen(
        gemeinsame_buchungen: Vec<GemeinsameBuchung>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen,
            },
            Datum::first(),
            empty_database_version(),
        )
    }
    pub fn generate_database_with_einzel_und_gemeinsamen_buchungen(
        einzelbuchungen: Vec<Einzelbuchung>,
        gemeinsame_buchungen: Vec<GemeinsameBuchung>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen,
                dauerauftraege: vec![],
                gemeinsame_buchungen,
            },
            Datum::first(),
            empty_database_version(),
        )
    }

    pub fn data_on_disk_with_einzelbuchungen(einzelbuchungen: Vec<Einzelbuchung>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen,
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
        }
    }

    pub fn data_on_disk_with_dauerauftraege(dauerauftraege: Vec<Dauerauftrag>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege,
            gemeinsame_buchungen: vec![],
        }
    }

    pub fn data_on_disk_with_gemeinsame_buchungen(
        gemeinsame_buchungen: Vec<GemeinsameBuchung>,
    ) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen,
        }
    }

    pub fn empty_database_version() -> DatabaseVersion {
        DatabaseVersion {
            name: "empty".to_string(),
            version: 0,
            session_random: 0,
        }
    }

    pub fn einzelbuchungen(einzelbuchung: Einzelbuchung) -> Einzelbuchungen {
        Einzelbuchungen {
            einzelbuchungen: vec![Indiziert {
                value: einzelbuchung,
                dynamisch: false,
                index: 0,
            }],
        }
    }

    pub fn leere_einzelbuchungen() -> Einzelbuchungen {
        Einzelbuchungen {
            einzelbuchungen: vec![],
        }
    }

    pub fn leere_dauerauftraege() -> Dauerauftraege {
        Dauerauftraege {
            dauerauftraege: vec![],
        }
    }

    pub fn leere_gemeinsame_buchungen() -> GemeinsameBuchungen {
        GemeinsameBuchungen {
            gemeinsame_buchungen: vec![],
        }
    }

    pub fn dauerauftrage(dauerauftrag: Dauerauftrag) -> Dauerauftraege {
        Dauerauftraege {
            dauerauftraege: vec![Indiziert {
                value: dauerauftrag,
                dynamisch: false,
                index: 0,
            }],
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::einzelbuchung::builder::any_einzelbuchung;
    use crate::model::state::persistent_application_state::builder::einzelbuchungen;

    #[test]
    fn test_as_string() {
        let version = super::DatabaseVersion {
            name: "Test".to_string(),
            version: 1,
            session_random: 2,
        };

        assert_eq!(version.as_string(), "Test-1-2");
    }

    #[test]
    fn test_einzelbuchungen_get() {
        let einzelbuchungen = einzelbuchungen(any_einzelbuchung());
        let result = einzelbuchungen.get(0);
        assert_eq!(result.value, any_einzelbuchung());
    }

    #[test]
    fn test_version_increment() {
        let version = super::DatabaseVersion {
            name: "Test".to_string(),
            version: 1,
            session_random: 2,
        };
        assert_eq!(version.as_string(), "Test-1-2");

        let result = version.increment();

        assert_eq!(result.as_string(), "Test-2-2");
    }
}
