use crate::model::state::persistent_application_state::Database;
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

pub fn generate_initial_database() -> Database {
    Database {
        db_version: DatabaseVersion {
            name: "initial".to_string(),
            version: 0,
            session_random: 0,
        },
        dauerauftraege: Dauerauftraege {
            dauerauftraege: vec![],
        },
        gemeinsame_buchungen: GemeinsameBuchungen {
            gemeinsame_buchungen: vec![],
        },
        einzelbuchungen: Einzelbuchungen {
            einzelbuchungen: vec![],
        },
        sparkontos: Sparkontos { sparkontos: vec![] },
        sparbuchungen: Sparbuchungen {
            sparbuchungen: vec![],
        },
        depotwerte: Depotwerte { depotwerte: vec![] },
        order: Orders { orders: vec![] },
        order_dauerauftraege: OrderDauerauftraege {
            order_dauerauftraege: vec![],
        },
        depotauszuege: Depotauszuege {
            depotauszuege: vec![],
        },
    }
}
