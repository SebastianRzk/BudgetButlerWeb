use crate::model::state::persistent_application_state::Database;

pub fn sort_database(unsorted_database: &Database) -> Database {
    let sorted_einzelbuchungen = unsorted_database.einzelbuchungen.clone().sort();
    let sorted_dauerauftraege = unsorted_database.dauerauftraege.clone().sort();
    let sorted_gemeinsame_buchungen = unsorted_database.gemeinsame_buchungen.clone().sort();
    let sorted_sparkontos = unsorted_database.sparkontos.clone().sort();
    let sorted_sparbuchungen = unsorted_database.sparbuchungen.clone().sort();
    let sorted_depotwerte = unsorted_database.depotwerte.clone().sort();
    let sorted_order = unsorted_database.order.clone().sort();
    let sorted_order_dauerauftraege = unsorted_database.order_dauerauftraege.clone().sort();
    let sorted_depotauszuege = unsorted_database.depotauszuege.clone().sort();

    Database {
        db_version: unsorted_database.db_version.clone(),
        einzelbuchungen: sorted_einzelbuchungen,
        dauerauftraege: sorted_dauerauftraege,
        gemeinsame_buchungen: sorted_gemeinsame_buchungen,
        sparkontos: sorted_sparkontos,
        sparbuchungen: sorted_sparbuchungen,
        depotwerte: sorted_depotwerte,
        order: sorted_order,
        order_dauerauftraege: sorted_order_dauerauftraege,
        depotauszuege: sorted_depotauszuege,
    }
}

pub fn sort_database_mut(unsorted_database: Database) -> Database {
    let sorted_einzelbuchungen = unsorted_database.einzelbuchungen.sort();
    let sorted_dauerauftraege = unsorted_database.dauerauftraege.sort();
    let sorted_gemeinsame_buchungen = unsorted_database.gemeinsame_buchungen.sort();
    let sorted_sparkontos = unsorted_database.sparkontos.sort();
    let sorted_sparbuchungen = unsorted_database.sparbuchungen.sort();
    let sorted_depotwerte = unsorted_database.depotwerte.sort();
    let sorted_order = unsorted_database.order.sort();
    let sorted_order_dauerauftraege = unsorted_database.order_dauerauftraege.sort();
    let sorted_depotauszuege = unsorted_database.depotauszuege.sort();

    Database {
        db_version: unsorted_database.db_version,
        einzelbuchungen: sorted_einzelbuchungen,
        dauerauftraege: sorted_dauerauftraege,
        gemeinsame_buchungen: sorted_gemeinsame_buchungen,
        sparkontos: sorted_sparkontos,
        sparbuchungen: sorted_sparbuchungen,
        depotwerte: sorted_depotwerte,
        order: sorted_order,
        order_dauerauftraege: sorted_order_dauerauftraege,
        depotauszuege: sorted_depotauszuege,
    }
}
