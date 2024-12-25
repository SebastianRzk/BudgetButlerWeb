use crate::budgetbutler::database::reader::calc_dauerauftrag::{
    calc_dauerauftrag, calc_order_dauerauftrag,
};
use crate::budgetbutler::database::reader::dynamic_indexer::index_dynamic;
use crate::budgetbutler::database::sorter::sort_database_mut;
use crate::io::disk::database::types::ElementRequirement;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::sparbuchung::SparbuchungTyp;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::{Kategorie, SPAREN_KATEGORIE};
use crate::model::state::persistent_application_state::{DataOnDisk, Database};
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

struct IndexedValues<T: ElementRequirement> {
    new_index: u32,
    values: Vec<Indiziert<T>>,
}

pub fn create_database(
    data_on_disk: DataOnDisk,
    heute: Datum,
    current_db_version: DatabaseVersion,
) -> Database {
    let indizierte_einzelbuchungen = index_values(data_on_disk.einzelbuchungen, 1);

    let indizierte_dauerauftraege = index_values(
        data_on_disk.dauerauftraege,
        indizierte_einzelbuchungen.new_index,
    );

    let indizierte_gemeinsame_buchungen = index_values(
        data_on_disk.gemeinsame_buchungen,
        indizierte_dauerauftraege.new_index,
    );

    let indizierte_sparkontos = index_values(
        data_on_disk.sparkontos,
        indizierte_gemeinsame_buchungen.new_index,
    );

    let indizierte_sparbuchungen =
        index_values(data_on_disk.sparbuchungen, indizierte_sparkontos.new_index);

    let indizierte_depotwerte =
        index_values(data_on_disk.depotwerte, indizierte_sparbuchungen.new_index);

    let indizierte_order = index_values(data_on_disk.order, indizierte_depotwerte.new_index);

    let indizierte_order_dauerauftraege = index_values(
        data_on_disk.order_dauerauftraege,
        indizierte_order.new_index,
    );

    let indizierte_depotauszuege = index_values(
        data_on_disk.depotauszuege,
        indizierte_order_dauerauftraege.new_index,
    );

    let initialized_db = calc_internal_state(
        Database {
            einzelbuchungen: Einzelbuchungen {
                einzelbuchungen: indizierte_einzelbuchungen.values,
            },
            dauerauftraege: Dauerauftraege {
                dauerauftraege: indizierte_dauerauftraege.values,
            },
            sparkontos: Sparkontos {
                sparkontos: indizierte_sparkontos.values,
            },
            gemeinsame_buchungen: GemeinsameBuchungen {
                gemeinsame_buchungen: indizierte_gemeinsame_buchungen.values,
            },
            sparbuchungen: Sparbuchungen {
                sparbuchungen: indizierte_sparbuchungen.values,
            },
            depotwerte: Depotwerte {
                depotwerte: indizierte_depotwerte.values,
            },
            order: Orders {
                orders: indizierte_order.values,
            },
            order_dauerauftraege: OrderDauerauftraege {
                order_dauerauftraege: indizierte_order_dauerauftraege.values,
            },
            depotauszuege: Depotauszuege {
                depotauszuege: indizierte_depotauszuege.values,
            },
            db_version: DatabaseVersion {
                name: current_db_version.name,
                version: current_db_version.version + 1,
                session_random: current_db_version.session_random,
            },
        },
        heute,
        indizierte_depotauszuege.new_index,
    );

    sort_database_mut(initialized_db)
}

fn index_values<T: ElementRequirement>(values: Vec<T>, first_free_index: u32) -> IndexedValues<T> {
    let mut current_index = first_free_index;
    let mut indexed_values = Vec::<Indiziert<T>>::new();
    for value in values {
        indexed_values.push(Indiziert {
            index: current_index,
            dynamisch: false,
            value,
        });
        current_index += 1;
    }
    IndexedValues {
        new_index: current_index,
        values: indexed_values,
    }
}

fn calc_internal_state(database: Database, heute: Datum, next_free_index: u32) -> Database {
    let mut current_index: u32 = next_free_index;
    let mut einzelbuchungen = database.einzelbuchungen.einzelbuchungen;
    let dauerauftraege = database.dauerauftraege;
    let mut order = database.order.orders;

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

    for sparbuchung in &database.sparbuchungen.sparbuchungen {
        current_index += 1;

        let betrag: Betrag;

        match sparbuchung.value.typ {
            SparbuchungTyp::ManuelleEinzahlung | SparbuchungTyp::SonstigeKosten => {
                betrag = sparbuchung.value.wert.negativ();
            }

            SparbuchungTyp::ManuelleAuszahlung | SparbuchungTyp::Ausschuettung => {
                betrag = sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::Zinsen => {
                betrag = Betrag::zero();
            }
        }

        if betrag == Betrag::zero() {
            continue;
        }

        einzelbuchungen.push(Indiziert {
            index: current_index,
            dynamisch: true,
            value: Einzelbuchung {
                datum: sparbuchung.value.datum.clone(),
                name: sparbuchung.value.name.clone(),
                kategorie: Kategorie::new(SPAREN_KATEGORIE.to_string()),
                betrag,
            },
        });
    }

    for order_dauerauftrag in &database.order_dauerauftraege.order_dauerauftraege {
        let dynamische_buchungen =
            calc_order_dauerauftrag(&order_dauerauftrag.value, heute.clone());
        let mut dynamic_index = index_dynamic(dynamische_buchungen, current_index);
        current_index = dynamic_index.new_index;
        order.append(&mut dynamic_index.values);
    }

    for order in &order {
        current_index += 1;
        einzelbuchungen.push(Indiziert {
            index: current_index,
            dynamisch: true,
            value: Einzelbuchung {
                datum: order.value.datum.clone(),
                name: order.value.name.clone(),
                kategorie: Kategorie::new(SPAREN_KATEGORIE.to_string()),
                betrag: order
                    .value
                    .wert
                    .get_betrag_fuer_geleistete_investition()
                    .invertiere_vorzeichen(),
            },
        });
    }

    Database {
        einzelbuchungen: Einzelbuchungen { einzelbuchungen },
        dauerauftraege,
        gemeinsame_buchungen: database.gemeinsame_buchungen,
        sparbuchungen: database.sparbuchungen,
        sparkontos: database.sparkontos,
        db_version: database.db_version,
        depotwerte: database.depotwerte,
        order: Orders { orders: order },
        order_dauerauftraege: database.order_dauerauftraege,
        depotauszuege: database.depotauszuege,
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::model::database::dauerauftrag::Dauerauftrag;
    use crate::model::database::depotauszug::builder::demo_depotauszug_aus_str;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::database::order::builder::any_order;
    use crate::model::database::order::Order;
    use crate::model::database::order_dauerauftrag::builder::order_dauerauftrag_with_range;
    use crate::model::database::sparbuchung::builder::{
        any_sparbuchung, sparbuchung_with_betrag_und_typ,
    };
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::datum::builder::{any_datum, datum};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::{demo_kategorie, sparen_kategorie};
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::demo_person;
    use crate::model::primitives::rhythmus::Rhythmus;
    use crate::model::state::persistent_application_state::builder::{
        data_on_disk_with_dauerauftraege, data_on_disk_with_depotauszug,
        data_on_disk_with_depotwerte, data_on_disk_with_einzelbuchungen,
        data_on_disk_with_gemeinsame_buchungen, data_on_disk_with_order,
        data_on_disk_with_order_dauerauftrag, data_on_disk_with_sparbuchungen,
        data_on_disk_with_sparkontos, demo_database_version,
    };
    use crate::model::state::persistent_application_state::DataOnDisk;
    use crate::model::state::persistent_state::database_version::DatabaseVersion;

    #[test]
    fn test_create_database_with_einzelbuchung() {
        let einzelbuchungen = vec![Einzelbuchung {
            datum: Datum::new(1, 1, 2024),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: betrag(Vorzeichen::Negativ, 123, 12),
        }];

        let data_on_disk = data_on_disk_with_einzelbuchungen(einzelbuchungen);

        let database = create_database(data_on_disk, Datum::first(), demo_database_version());

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

        let database = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(database.dauerauftraege.select().count(), 1);

        let dauerauftrag = &database.dauerauftraege.get(1);
        assert_eq!(dauerauftrag.index, 1);
        assert_eq!(dauerauftrag.value.start_datum, Datum::new(1, 1, 2024));
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

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

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
            kategorie: demo_kategorie(),
            person: demo_person(),
            name: demo_name(),
        };
        let data_on_disk = data_on_disk_with_gemeinsame_buchungen(vec![gemeinsame_buchung.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(einzelbuchung.dynamisch, true);
        assert_eq!(einzelbuchung.value.datum, gemeinsame_buchung.datum);
        assert_eq!(einzelbuchung.value.betrag, zwei());
        assert_eq!(einzelbuchung.value.kategorie, gemeinsame_buchung.kategorie);
        assert_eq!(einzelbuchung.value.name, gemeinsame_buchung.name);
    }

    #[test]
    fn test_should_init_sparkontos() {
        let sparkonto = Sparkonto {
            name: demo_name(),
            kontotyp: Kontotyp::Sparkonto,
        };
        let data_on_disk = data_on_disk_with_sparkontos(vec![sparkonto.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.sparkontos.select().count(), 1);
        let selected_sparkonto = result.sparkontos.get(1);
        assert_eq!(selected_sparkonto.dynamisch, false);
        assert_eq!(selected_sparkonto.value.name, sparkonto.name);
        assert_eq!(selected_sparkonto.value.kontotyp, sparkonto.kontotyp);
    }

    #[test]
    fn test_should_init_sparbuchungen() {
        let sparbuchung = any_sparbuchung();
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.sparbuchungen.select().count(), 1);
        let selected_sparbuchung = result.sparbuchungen.get(1);
        assert_eq!(selected_sparbuchung.dynamisch, false);
        assert_eq!(selected_sparbuchung.value, sparbuchung);
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

    #[test]
    fn test_should_calc_sparbuchungen_to_einzelbuchungen_with_einzahlung_should_import_as_ausgabe()
    {
        let sparbuchung =
            sparbuchung_with_betrag_und_typ(u_zwei(), SparbuchungTyp::ManuelleEinzahlung);
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        compute_and_assert_ausgabe(sparbuchung, data_on_disk);
    }

    fn compute_and_assert_ausgabe(sparbuchung: Sparbuchung, data_on_disk: DataOnDisk) {
        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let selected_einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(selected_einzelbuchung.dynamisch, true);
        assert_eq!(selected_einzelbuchung.value.datum, sparbuchung.datum);
        assert_eq!(selected_einzelbuchung.value.name, sparbuchung.name);
        assert_eq!(selected_einzelbuchung.value.kategorie, sparen_kategorie());
        assert_eq!(selected_einzelbuchung.value.betrag, minus_zwei());
    }

    #[test]
    fn test_should_calc_sparbuchungen_to_einzelbuchungen_with_auszahlung_should_import_as_einnahme()
    {
        let sparbuchung =
            sparbuchung_with_betrag_und_typ(u_zwei(), SparbuchungTyp::ManuelleAuszahlung);
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let selected_einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(selected_einzelbuchung.dynamisch, true);
        assert_eq!(selected_einzelbuchung.value.datum, sparbuchung.datum);
        assert_eq!(selected_einzelbuchung.value.name, sparbuchung.name);
        assert_eq!(selected_einzelbuchung.value.kategorie, sparen_kategorie());
        assert_eq!(selected_einzelbuchung.value.betrag, zwei());
    }

    #[test]
    fn test_should_calc_sparbuchungen_to_einzelbuchungen_with_ausschuettung_should_import_as_einnahme(
    ) {
        let sparbuchung = sparbuchung_with_betrag_und_typ(u_zwei(), SparbuchungTyp::Ausschuettung);
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        compute_and_assert_einnahme(sparbuchung, data_on_disk);
    }

    #[test]
    fn test_should_calc_sparbuchungen_to_einzelbuchungen_with_zinsen_should_do_nothing() {
        let sparbuchung = sparbuchung_with_betrag_und_typ(u_zwei(), SparbuchungTyp::Zinsen);
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 0);
    }

    #[test]
    fn test_should_calc_sparbuchungen_to_einzelbuchungen_with_sonstige_kosten_should_import_as_ausgabe(
    ) {
        let sparbuchung = sparbuchung_with_betrag_und_typ(u_zwei(), SparbuchungTyp::SonstigeKosten);
        let data_on_disk = data_on_disk_with_sparbuchungen(vec![sparbuchung.clone()]);

        compute_and_assert_ausgabe(sparbuchung, data_on_disk);
    }

    fn compute_and_assert_einnahme(sparbuchung: Sparbuchung, data_on_disk: DataOnDisk) {
        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let selected_einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(selected_einzelbuchung.dynamisch, true);
        assert_eq!(selected_einzelbuchung.value.datum, sparbuchung.datum);
        assert_eq!(selected_einzelbuchung.value.name, sparbuchung.name);
        assert_eq!(selected_einzelbuchung.value.kategorie, sparen_kategorie());
        assert_eq!(selected_einzelbuchung.value.betrag, zwei());
    }

    #[test]
    fn test_should_init_depotwerte() {
        let depotwert = any_depotwert();
        let data_on_disk = data_on_disk_with_depotwerte(vec![depotwert.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.depotwerte.select().count(), 1);
        let selected_depotwert = result.depotwerte.get(1);
        assert_eq!(selected_depotwert.dynamisch, false);
        assert_eq!(selected_depotwert.value, depotwert);
    }

    #[test]
    fn test_should_init_order() {
        let order = any_order();
        let data_on_disk = data_on_disk_with_order(vec![order.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.order.select().count(), 1);
        let selected_order = result.order.get(1);
        assert_eq!(selected_order.dynamisch, false);
        assert_eq!(selected_order.value, order);
    }

    #[test]
    fn test_init_order_should_create_einzelbuchung() {
        let order = any_order();
        let data_on_disk = data_on_disk_with_order(vec![order.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let selected_einzelbuchung = result.einzelbuchungen.get(3);
        assert_eq!(selected_einzelbuchung.dynamisch, true);
        assert_eq!(
            selected_einzelbuchung.value,
            Einzelbuchung {
                datum: order.datum,
                name: order.name,
                kategorie: sparen_kategorie(),
                betrag: order
                    .wert
                    .get_betrag_fuer_geleistete_investition()
                    .invertiere_vorzeichen(),
            }
        );
    }

    #[test]
    fn test_should_init_order_dauerauftraege() {
        let order_dauerauftrag = any_order();
        let data_on_disk = data_on_disk_with_order(vec![order_dauerauftrag.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.order.select().count(), 1);
        let selected_order = result.order.get(1);
        assert_eq!(selected_order.dynamisch, false);
        assert_eq!(selected_order.value, order_dauerauftrag);
    }

    #[test]
    fn test_init_order_dauerauftraege_should_create_einzelbuchung() {
        let order_dauerauftrag = order_dauerauftrag_with_range(
            datum("2024-01-01"),
            datum("2024-01-02"),
            Rhythmus::Monatlich,
        );
        let data_on_disk = data_on_disk_with_order_dauerauftrag(vec![order_dauerauftrag.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.order.select().count(), 1);
        eprintln!("{:?}", result.order);
        let selected_order = result.order.get(3);
        assert_eq!(selected_order.dynamisch, true);
        assert_eq!(
            selected_order.value,
            Order {
                datum: datum("2024-01-01"),
                name: order_dauerauftrag.name.clone(),
                konto: order_dauerauftrag.konto,
                depotwert: order_dauerauftrag.depotwert,
                wert: order_dauerauftrag.wert.clone(),
            }
        );

        assert_eq!(result.einzelbuchungen.select().count(), 1);
        let selected_einzelbuchung = result.einzelbuchungen.get(5);
        assert_eq!(selected_einzelbuchung.dynamisch, true);
        assert_eq!(
            selected_einzelbuchung.value,
            Einzelbuchung {
                datum: datum("2024-01-01"),
                name: order_dauerauftrag.name,
                kategorie: sparen_kategorie(),
                betrag: order_dauerauftrag
                    .wert
                    .get_betrag_fuer_geleistete_investition()
                    .invertiere_vorzeichen(),
            }
        );
    }

    #[test]
    fn test_should_init_depotauszuege() {
        let depotauszug = demo_depotauszug_aus_str();
        let data_on_disk = data_on_disk_with_depotauszug(vec![depotauszug.clone()]);

        let result = create_database(data_on_disk, Datum::last(), demo_database_version());

        assert_eq!(result.depotauszuege.select().count(), 1);
        let selected_order = result.depotauszuege.get(1);
        assert_eq!(selected_order.dynamisch, false);
        assert_eq!(selected_order.value, depotauszug);
    }
}
