use crate::model::database::dauerauftrag::Dauerauftrag;
use crate::model::database::depotauszug::Depotauszug;
use crate::model::database::depotwert::Depotwert;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::database::order::Order;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::database::sparbuchung::Sparbuchung;
use crate::model::database::sparkonto::Sparkonto;
use crate::model::state::persistent_state::database_version::DatabaseVersion;
use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;
use crate::model::state::persistent_state::depotauszuege::Depotauszuege;
use crate::model::state::persistent_state::depotwerte::Depotwerte;
use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;
use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;
use crate::model::state::persistent_state::order::Orders;
use crate::model::state::persistent_state::order_dauerauftraege::OrderDauerauftraege;
use crate::model::state::persistent_state::sparbuchungen::Sparbuchungen;
use crate::model::state::persistent_state::sparkontos::Sparkontos;
use std::sync::Mutex;

pub struct ApplicationState {
    pub database: Mutex<Database>,
}

pub struct Database {
    pub db_version: DatabaseVersion,
    pub einzelbuchungen: Einzelbuchungen,
    pub dauerauftraege: Dauerauftraege,
    pub gemeinsame_buchungen: GemeinsameBuchungen,
    pub sparkontos: Sparkontos,
    pub sparbuchungen: Sparbuchungen,
    pub depotwerte: Depotwerte,
    pub order: Orders,
    pub order_dauerauftraege: OrderDauerauftraege,
    pub depotauszuege: Depotauszuege,
}

pub struct DataOnDisk {
    pub einzelbuchungen: Vec<Einzelbuchung>,
    pub dauerauftraege: Vec<Dauerauftrag>,
    pub gemeinsame_buchungen: Vec<GemeinsameBuchung>,
    pub sparkontos: Vec<Sparkonto>,
    pub sparbuchungen: Vec<Sparbuchung>,
    pub depotwerte: Vec<Depotwert>,
    pub order: Vec<Order>,
    pub order_dauerauftraege: Vec<OrderDauerauftrag>,
    pub depotauszuege: Vec<Depotauszug>,
}

impl Database {
    pub fn change_einzelbuchungen(&self, einzelbuchungen: Einzelbuchungen) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen,
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }
    pub fn change_dauerauftraege(&self, dauerauftraege: Dauerauftraege) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege,
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
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
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }
    pub fn change_sparkontos(&self, sparkontos: Sparkontos) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos,
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }

    pub fn change_depotwerte(&self, depotwerte: Depotwerte) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte,
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }

    pub fn change_order(&self, order: Orders) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order,
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }

    pub fn change_order_dauerauftraege(
        &self,
        order_dauerauftraege: OrderDauerauftraege,
    ) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege,
            depotauszuege: self.depotauszuege.clone(),
        }
    }

    pub fn change_depotauszuege(&self, depotauszuege: Depotauszuege) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen: self.sparbuchungen.clone(),
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege,
        }
    }

    pub fn change_sparbuchungen(&self, sparbuchungen: Sparbuchungen) -> Database {
        Database {
            db_version: self.db_version.increment(),
            einzelbuchungen: self.einzelbuchungen.clone(),
            dauerauftraege: self.dauerauftraege.clone(),
            gemeinsame_buchungen: self.gemeinsame_buchungen.clone(),
            sparkontos: self.sparkontos.clone(),
            sparbuchungen,
            depotwerte: self.depotwerte.clone(),
            order: self.order.clone(),
            order_dauerauftraege: self.order_dauerauftraege.clone(),
            depotauszuege: self.depotauszuege.clone(),
        }
    }
}

#[cfg(test)]
pub mod builder {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::model::database::dauerauftrag::Dauerauftrag;
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::Depotwert;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::database::order::Order;
    use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
    use crate::model::database::sparbuchung::Sparbuchung;
    use crate::model::database::sparkonto::Sparkonto;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_application_state::DataOnDisk;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;
    use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;
    use crate::model::state::persistent_state::depotauszuege::Depotauszuege;
    use crate::model::state::persistent_state::depotwerte::Depotwerte;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;
    use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;
    use crate::model::state::persistent_state::order::Orders;
    use crate::model::state::persistent_state::order_dauerauftraege::OrderDauerauftraege;
    use crate::model::state::persistent_state::sparbuchungen::Sparbuchungen;
    use crate::model::state::persistent_state::sparkontos::Sparkontos;

    pub fn generate_empty_database() -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
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
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
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
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_sparkontos(sparkontos: Vec<Sparkonto>) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos,
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_sparkontos_und_sparbuchungen(
        sparkontos: Vec<Sparkonto>,
        sparbuchungen: Vec<Sparbuchung>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos,
                sparbuchungen,
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_sparbuchungen(
        sparbuchungen: Vec<Sparbuchung>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen,
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_depotwerte(depotwerte: Vec<Depotwert>) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte,
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
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
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_orders(order: Vec<Order>) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order,
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_order_dauerauftraege(
        order_dauerauftraege: Vec<OrderDauerauftrag>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege,
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn generate_database_with_depotauszuege(
        depotauszuege: Vec<Depotauszug>,
    ) -> super::Database {
        create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege,
            },
            Datum::first(),
            demo_database_version(),
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
                sparkontos: vec![],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![],
                order_dauerauftraege: vec![],
                depotauszuege: vec![],
            },
            Datum::first(),
            demo_database_version(),
        )
    }

    pub fn data_on_disk_with_einzelbuchungen(einzelbuchungen: Vec<Einzelbuchung>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen,
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_dauerauftraege(dauerauftraege: Vec<Dauerauftrag>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege,
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_gemeinsame_buchungen(
        gemeinsame_buchungen: Vec<GemeinsameBuchung>,
    ) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen,
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_sparkontos(sparkontos: Vec<Sparkonto>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos,
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_sparbuchungen(sparbuchungen: Vec<Sparbuchung>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen,
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_depotwerte(depotwerte: Vec<Depotwert>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte,
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_order(order: Vec<Order>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order,
            order_dauerauftraege: vec![],
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_order_dauerauftrag(
        order_dauerauftrag: Vec<OrderDauerauftrag>,
    ) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: order_dauerauftrag,
            depotauszuege: vec![],
        }
    }

    pub fn data_on_disk_with_depotauszug(depotauszuege: Vec<Depotauszug>) -> DataOnDisk {
        DataOnDisk {
            einzelbuchungen: vec![],
            dauerauftraege: vec![],
            gemeinsame_buchungen: vec![],
            sparkontos: vec![],
            sparbuchungen: vec![],
            depotwerte: vec![],
            order: vec![],
            order_dauerauftraege: vec![],
            depotauszuege,
        }
    }

    pub fn demo_database_version() -> DatabaseVersion {
        DatabaseVersion {
            name: "empty".to_string(),
            version: 0,
            session_random: 0,
        }
    }

    pub fn demo_database_version_str() -> String {
        "empty-0-0".to_string()
    }

    pub fn einzelbuchungen(einzelbuchung: Einzelbuchung) -> Einzelbuchungen {
        Einzelbuchungen {
            einzelbuchungen: vec![indiziert(einzelbuchung)],
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

    pub fn leere_sparkontos() -> Sparkontos {
        Sparkontos { sparkontos: vec![] }
    }

    pub fn leere_sparbuchungen() -> Sparbuchungen {
        Sparbuchungen {
            sparbuchungen: vec![],
        }
    }

    pub fn leere_depotwerte() -> Depotwerte {
        Depotwerte { depotwerte: vec![] }
    }

    pub fn leere_order() -> Orders {
        Orders { orders: vec![] }
    }

    pub fn leere_order_dauerauftraege() -> OrderDauerauftraege {
        OrderDauerauftraege {
            order_dauerauftraege: vec![],
        }
    }

    pub fn leere_depotauszuege() -> Depotauszuege {
        Depotauszuege {
            depotauszuege: vec![],
        }
    }

    pub fn dauerauftrage(dauerauftrag: Dauerauftrag) -> Dauerauftraege {
        Dauerauftraege {
            dauerauftraege: vec![indiziert(dauerauftrag)],
        }
    }

    pub fn sparkontos(sparkonto: Sparkonto) -> Sparkontos {
        Sparkontos {
            sparkontos: vec![indiziert(sparkonto)],
        }
    }

    pub fn depotwerte(depotwert: Depotwert) -> Depotwerte {
        Depotwerte {
            depotwerte: vec![indiziert(depotwert)],
        }
    }

    pub fn depotauszuege(depotauszug: Depotauszug) -> Depotauszuege {
        Depotauszuege {
            depotauszuege: vec![indiziert(depotauszug)],
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::dauerauftrag::builder::dauerauftrag_mit_kategorie;
    use crate::model::database::einzelbuchung::builder::{
        demo_einzelbuchung, einzelbuchung_with_kategorie,
    };
    use crate::model::database::gemeinsame_buchung::builder::{
        gemeinsame_buchung_mit_kategorie, gemeinsame_buchung_mit_person,
    };
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::person::builder::person;
    use crate::model::state::persistent_application_state::builder::einzelbuchungen;
    use crate::model::state::persistent_state::dauerauftraege::Dauerauftraege;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;
    use crate::model::state::persistent_state::gemeinsame_buchungen::GemeinsameBuchungen;

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
        let einzelbuchungen = einzelbuchungen(demo_einzelbuchung());
        let result = einzelbuchungen.get(0);
        assert_eq!(result.value, demo_einzelbuchung());
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

    #[test]
    fn test_einzelbuchungen_get_kategorien() {
        let einzelbuchungen = einzelbuchungen(demo_einzelbuchung());
        let result = einzelbuchungen.get_kategorien();
        assert_eq!(result.len(), 1);
        assert_eq!(result[0], demo_kategorie());
    }

    #[test]
    fn test_gemeinsame_buchungen_rename_person() {
        let gemeinsame_buchungen = GemeinsameBuchungen {
            gemeinsame_buchungen: vec![
                indiziert(gemeinsame_buchung_mit_person("to rename")),
                indiziert(gemeinsame_buchung_mit_person("not to rename")),
            ],
        };

        let result = gemeinsame_buchungen
            .change()
            .rename_person(person("to rename"), person("renamed"));

        assert_eq!(
            result.gemeinsame_buchungen[0].value.person,
            person("renamed")
        );
        assert_eq!(
            result.gemeinsame_buchungen[1].value.person,
            person("not to rename")
        );
    }

    #[test]
    fn test_gemeinsame_buchungen_change_kategorie() {
        let gemeinsame_buchungen = GemeinsameBuchungen {
            gemeinsame_buchungen: vec![
                indiziert(gemeinsame_buchung_mit_kategorie("to rename")),
                indiziert(gemeinsame_buchung_mit_kategorie("not to rename")),
            ],
        };

        let result = gemeinsame_buchungen
            .change()
            .rename_kategorie(kategorie("to rename"), kategorie("renamed"));

        assert_eq!(
            result.gemeinsame_buchungen[0].value.kategorie,
            kategorie("renamed")
        );
        assert_eq!(
            result.gemeinsame_buchungen[1].value.kategorie,
            kategorie("not to rename")
        );
    }

    #[test]
    fn test_dauerauftrag_change_kategorie() {
        let dauerauftraege = Dauerauftraege {
            dauerauftraege: vec![
                indiziert(dauerauftrag_mit_kategorie("to rename")),
                indiziert(dauerauftrag_mit_kategorie("not to rename")),
            ],
        };

        let result = dauerauftraege
            .change()
            .rename_kategorie(kategorie("to rename"), kategorie("renamed"));

        assert_eq!(
            result.dauerauftraege[0].value.kategorie,
            kategorie("renamed")
        );
        assert_eq!(
            result.dauerauftraege[1].value.kategorie,
            kategorie("not to rename")
        );
    }

    #[test]
    fn test_einzelbuchungen_change_kategorie() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![
                indiziert(einzelbuchung_with_kategorie("to rename")),
                indiziert(einzelbuchung_with_kategorie("not to rename")),
            ],
        };

        let result = einzelbuchungen
            .change()
            .rename_kategorie(kategorie("to rename"), kategorie("renamed"));

        assert_eq!(
            result.einzelbuchungen[0].value.kategorie,
            kategorie("renamed")
        );
        assert_eq!(
            result.einzelbuchungen[1].value.kategorie,
            kategorie("not to rename")
        );
    }
}
