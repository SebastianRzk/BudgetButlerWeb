use crate::model::state::persistent_application_state::Database;

pub fn sort_database(unsorted_database: &Database)-> Database {
    let sorted_einzelbuchungen = unsorted_database.einzelbuchungen.clone().sort();
    let sorted_dauerauftraege = unsorted_database.dauerauftraege.clone().sort();
    let sorted_gemeinsame_buchungen = unsorted_database.gemeinsame_buchungen.clone().sort();

    Database {
        db_version: unsorted_database.db_version.clone(),
        einzelbuchungen: sorted_einzelbuchungen,
        dauerauftraege: sorted_dauerauftraege,
        gemeinsame_buchungen: sorted_gemeinsame_buchungen,
    }
}

pub fn sort_database_mut(unsorted_database: Database)-> Database {
    let sorted_einzelbuchungen = unsorted_database.einzelbuchungen.sort();
    let sorted_dauerauftraege = unsorted_database.dauerauftraege.sort();
    let sorted_gemeinsame_buchungen = unsorted_database.gemeinsame_buchungen.sort();

    Database {
        db_version: unsorted_database.db_version,
        einzelbuchungen: sorted_einzelbuchungen,
        dauerauftraege: sorted_dauerauftraege,
        gemeinsame_buchungen: sorted_gemeinsame_buchungen,
    }
}
