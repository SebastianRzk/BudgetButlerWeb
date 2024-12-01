use crate::budgetbutler::database::reader::calc_dauerauftrag::calc_dauerauftrag;
use crate::budgetbutler::database::reader::dynamic_indexer::index_dynamic;
use crate::budgetbutler::database::sorter::sort_database_mut;
use crate::model::dauerauftrag::Dauerauftrag;
use crate::model::einzelbuchung::Einzelbuchung;
use crate::model::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::{
    DataOnDisk, Database, DatabaseVersion, Dauerauftraege, Einzelbuchungen, GemeinsameBuchungen,
};

pub fn create_database(
    data_on_disk: DataOnDisk,
    heute: Datum,
    current_db_version: DatabaseVersion,
) -> Database {
    let mut current_index: u32 = 1;

    let mut einzelbuchungen = Vec::<Indiziert<Einzelbuchung>>::new();

    for einzelbuchung_on_disk in data_on_disk.einzelbuchungen {
        einzelbuchungen.push(Indiziert {
            index: current_index,
            dynamisch: false,
            value: einzelbuchung_on_disk,
        });
        current_index += 1;
    }

    let mut dauerauftraege = Vec::<Indiziert<Dauerauftrag>>::new();

    for dauerauftrag_on_disk in data_on_disk.dauerauftraege {
        dauerauftraege.push(Indiziert {
            index: current_index,
            dynamisch: false,
            value: dauerauftrag_on_disk,
        });
        current_index += 1;
    }

    let mut gemeinsame_buchungen = Vec::<Indiziert<GemeinsameBuchung>>::new();

    for gemeinsame_buchung_on_disk in data_on_disk.gemeinsame_buchungen {
        gemeinsame_buchungen.push(Indiziert {
            index: current_index,
            dynamisch: false,
            value: gemeinsame_buchung_on_disk,
        });
        current_index += 1;
    }

    let initialized_db = calc_internal_state(
        Database {
            einzelbuchungen: Einzelbuchungen { einzelbuchungen },
            dauerauftraege: Dauerauftraege { dauerauftraege },
            gemeinsame_buchungen: GemeinsameBuchungen {
                gemeinsame_buchungen,
            },
            db_version: DatabaseVersion {
                name: current_db_version.name,
                version: current_db_version.version + 1,
                session_random: current_db_version.session_random,
            },
        },
        heute,
        current_index,
    );

    sort_database_mut(initialized_db)
}

fn calc_internal_state(database: Database, heute: Datum, next_free_index: u32) -> Database {
    let mut current_index: u32 = next_free_index;
    let mut einzelbuchungen = database.einzelbuchungen.einzelbuchungen;
    let dauerauftraege = database.dauerauftraege;

    for dauerauftrag in &dauerauftraege.dauerauftraege {
        let dynamische_buchungen = calc_dauerauftrag(&dauerauftrag.value, heute.clone());
        let mut dynamic_index = index_dynamic(dynamische_buchungen, current_index);
        current_index = dynamic_index.new_index;
        einzelbuchungen.append(&mut dynamic_index.values);
    }

    for gemeinsame_buchung in &database.gemeinsame_buchungen.gemeinsame_buchungen {
        current_index += 1;
        einzelbuchungen.push(Indiziert {
            index: current_index,
            dynamisch: true,
            value: Einzelbuchung {
                datum: gemeinsame_buchung.value.datum.clone(),
                name: gemeinsame_buchung.value.name.clone(),
                kategorie: gemeinsame_buchung.value.kategorie.clone(),
                betrag: gemeinsame_buchung.value.betrag.halbiere(),
            },
        });
    }

    Database {
        einzelbuchungen: Einzelbuchungen { einzelbuchungen },
        dauerauftraege,
        gemeinsame_buchungen: database.gemeinsame_buchungen,
        db_version: database.db_version,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::model::dauerauftrag::Dauerauftrag;
    use crate::model::einzelbuchung::Einzelbuchung;
    use crate::model::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::any_kategorie;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::any_name;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::any_person;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::{
        data_on_disk_with_dauerauftraege, data_on_disk_with_einzelbuchungen,
        data_on_disk_with_gemeinsame_buchungen, empty_database_version,
    };
    use crate::model::state::persistent_application_state::DatabaseVersion;

    #[test]
    fn test_create_database_with_einzelbuchung() {
        let einzelbuchungen = vec![Einzelbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        }];

        let data_on_disk = data_on_disk_with_einzelbuchungen(einzelbuchungen);

        let database = create_database(data_on_disk, Datum::first(), empty_database_version());

        assert_eq!(database.einzelbuchungen.select().count(), 1);

        let einzelbuchung = &database.einzelbuchungen.get(1);
        assert_eq!(einzelbuchung.index, 1);
        assert_eq!(einzelbuchung.value.datum, Datum::new(1, 1, 2024));
        assert_eq!(einzelbuchung.value.name, name("Normal"));
        assert_eq!(einzelbuchung.value.kategorie, kategorie("NeueKategorie"));
        assert_eq!(
            einzelbuchung.value.betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );
    }

    #[test]
    fn test_create_database_with_dauerauftrag() {
        let dauerauftraege = vec![Dauerauftrag {
            start_datum: Datum::new(1, 1, 2024),
            ende_datum: Datum::new(1, 1, 2025),
            name: name("Miete"),
            kategorie: kategorie("NeueKategorie"),
            rhythmus: Rhythmus::Monatlich,
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        }];

        let data_on_disk = data_on_disk_with_dauerauftraege(dauerauftraege);

        let database = create_database(data_on_disk, Datum::last(), empty_database_version());

        assert_eq!(database.dauerauftraege.select().count(), 1);

        let dauerauftrag = &database.dauerauftraege.get(1);
        assert_eq!(dauerauftrag.index, 1);
        assert_eq!(dauerauftrag.value.start_datum, Datum::new(1, 1,2024));
        assert_eq!(dauerauftrag.value.ende_datum, Datum::new(1, 1, 2025));
        assert_eq!(dauerauftrag.value.name, name("Miete"));
        assert_eq!(dauerauftrag.value.kategorie, kategorie("NeueKategorie"));
        assert_eq!(dauerauftrag.value.rhythmus, Rhythmus::Monatlich);
        assert_eq!(
            dauerauftrag.value.betrag,
            betrag(Vorzeichen::Negativ, 123, 12)
        );
    }

    #[test]
    fn test_should_init_dauerauftraege() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2024),
            ende_datum: Datum::new(1, 1, 2025),
            name: name("Miete"),
            kategorie: kategorie("NeueKategorie"),
            rhythmus: Rhythmus::Monatlich,
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        };
        let data_on_disk = data_on_disk_with_dauerauftraege(vec![dauerauftrag]);

        let result = create_database(data_on_disk, Datum::last(), empty_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 12);
        assert_eq!(result.einzelbuchungen.get(3).index, 3);
        assert_eq!(result.einzelbuchungen.get(14).index, 14);
        assert_eq!(result.dauerauftraege.select().count(), 1);
    }

    #[test]
    fn test_should_init_gemeinsame_buchungen() {
        let gemeinsame_buchung = GemeinsameBuchung {
            datum: any_datum(),
            betrag: vier(),
            kategorie: any_kategorie(),
            person: any_person(),
            name: any_name(),
        };
        let data_on_disk = data_on_disk_with_gemeinsame_buchungen(vec![gemeinsame_buchung.clone()]);

        let result = create_database(data_on_disk, Datum::last(), empty_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(einzelbuchung.dynamisch, true);
        assert_eq!(einzelbuchung.value.datum, gemeinsame_buchung.datum);
        assert_eq!(einzelbuchung.value.betrag, zwei());
        assert_eq!(einzelbuchung.value.kategorie, gemeinsame_buchung.kategorie);
        assert_eq!(einzelbuchung.value.name, gemeinsame_buchung.name);
    }

    #[test]
    fn test_should_increment_db_version() {
        let result = create_database(
            data_on_disk_with_dauerauftraege(vec![]),
            Datum::last(),
            DatabaseVersion {
                name: "MyName".to_string(),
                version: 0,
                session_random: 123,
            },
        );

        assert_eq!(result.db_version.name, "MyName");
        assert_eq!(result.db_version.version, 1);
        assert_eq!(result.db_version.session_random, 123);
    }
}
