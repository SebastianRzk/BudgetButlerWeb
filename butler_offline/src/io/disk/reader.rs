use crate::budgetbutler::database::reader::reader::create_database;
use crate::io::disk::database::dauerauftrag::dauerauftraege_reader::read_dauerauftraege;
use crate::io::disk::database::depotauszuege::depotauszuege_reader::read_depotauszuege;
use crate::io::disk::database::depotwerte::depotwerte_reader::read_depotwerte;
use crate::io::disk::database::einzelbuchungen::einzelbuchungen_reader::read_einzelbuchungen;
use crate::io::disk::database::gemeinsame_buchungen::gemeinsame_buchungen_reader::read_gemeinsame_buchungen;
use crate::io::disk::database::order::orders_reader::read_orders;
use crate::io::disk::database::order_dauerauftraege::order_dauerauftraege_reader::read_order_dauerauftraege;
use crate::io::disk::database::sparbuchungen::sparbuchungen_reader::read_sparbuchungen;
use crate::io::disk::database::sparkontos::sparkontos_reader::read_sparkontos;
use crate::io::disk::diskrepresentation::file::File;
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::diskrepresentation::sorter::sort_file;
use crate::io::time::today;
use crate::model::state::config::{get_database_location, DatabaseConfiguration};
use crate::model::state::persistent_application_state::{DataOnDisk, Database};
use crate::model::state::persistent_state::database_version::DatabaseVersion;
use std;
use std::fs;
use std::path::PathBuf;

fn read_file(path: PathBuf) -> File {
    println!(
        "loading file {}",
        std::path::absolute(&path).unwrap().to_str().unwrap()
    );
    let file_as_string = fs::read_to_string::<PathBuf>(path).unwrap();
    let lines = file_as_string
        .lines()
        .map(|l| Line {
            line: l.to_string(),
        })
        .collect();
    File { lines }
}

pub fn read_data(file: File) -> DataOnDisk {
    let sorted_file = sort_file(file);
    DataOnDisk {
        einzelbuchungen: read_einzelbuchungen(&sorted_file),
        dauerauftraege: read_dauerauftraege(&sorted_file),
        gemeinsame_buchungen: read_gemeinsame_buchungen(&sorted_file),
        sparkontos: read_sparkontos(&sorted_file),
        sparbuchungen: read_sparbuchungen(&sorted_file),
        depotwerte: read_depotwerte(&sorted_file),
        order: read_orders(&sorted_file),
        order_dauerauftraege: read_order_dauerauftraege(&sorted_file),
        depotauszuege: read_depotauszuege(&sorted_file),
    }
}

pub fn exists_database(config: &DatabaseConfiguration) -> bool {
    let full_path = get_database_location(config);
    println!("Checking if database exists at {:?}", full_path);
    full_path.exists()
}

pub fn read_database(
    config: &DatabaseConfiguration,
    current_database_version: DatabaseVersion,
) -> Database {
    let db_location = get_database_location(config);
    println!("Reading database from {:?}", db_location);
    let file = read_file(db_location);
    let data = read_data(file);
    create_database(data, today(), current_database_version)
}

#[cfg(test)]
mod tests {
    use crate::io::disk::diskrepresentation::file::File;
    use crate::io::disk::reader::read_data;
    use crate::model::database::depotwert::builder::depotwert_referenz;
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::database::order::OrderTyp::Kauf;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::primitives::person::builder::person;
    use crate::model::primitives::rhythmus::Rhythmus;

    const BEISPIEL_DATENBANK: &str = "\
Datum,Kategorie,Name,Wert
2023-01-01,NeueKategorie,Normal,-123.12
2024-01-02,NeueKategorie,\"Mit , Komma\",-123.00

Dauerauftraege
Startdatum,Endedatum,Kategorie,Name,Rhythmus,Wert
2021-12-22,2023-12-24,Kategorie1,Name1,monatlich,-1233.00
2021-12-24,2025-12-24,Kategorie2,Name2 als ausgabe,halbjährlich,-1233.00

Gemeinsame Buchungen
Datum,Kategorie,Name,Wert,Person
2024-11-01,MeineBuchung,Name,-234.00,Test_User
2024-11-21,PartnerBuchung,asd,-1234.00,kein_Partnername_gesetzt

Sparbuchungen
Datum,Name,Wert,Typ,Konto
2024-01-01,DerName,123.12,Zinsen,DasKonto
2024-01-02,DerName2,123.13,Ausschüttung,DasKonto2

Sparkontos
Kontoname,Kontotyp
SparkontoName,Sparkonto
DepotName,Depot

Depotwerte
Name,ISIN,Typ
Name1,ISIN1,ETF
Name2,ISIN2,Crypto

Order
Datum,Name,Konto,Depotwert,Wert,Typ
2020-01-01,MeinName,MeinKonto,MeinDepotwert,4.00,Kauf
2020-01-02,MeinName2,MeinKonto2,MeinDepotwert2,5.00,Kauf

Dauerauftr_Ordr
Startdatum,Endedatum,Rhythmus,Name,Konto,Depotwert,Wert,Typ
2020-01-01,2021-01-02,monatlich,MeinName,MeinKonto,MeinDepotwert,4.00,Kauf
2020-01-02,2021-01-03,monatlich,MeinName2,MeinKonto2,MeinDepotwert2,5.00,Kauf

Depotauszuege
Datum,Depotwert,Konto,Wert
2020-01-01,DE000A0D9PT0,MeinKonto,1000.00
2020-01-02,DE000A0D9PT1,MeinKonto2,1000.00
";

    #[test]
    fn test_read_data() {
        let file = File::from_str(BEISPIEL_DATENBANK);
        let data = read_data(file);

        let erste_einzelbuchung = &data.einzelbuchungen[0];
        assert_eq!(erste_einzelbuchung.datum, Datum::new(1, 1, 2023));
        assert_eq!(erste_einzelbuchung.name, name("Normal"));
        assert_eq!(erste_einzelbuchung.kategorie, kategorie("NeueKategorie"));
        assert_eq!(
            erste_einzelbuchung.betrag,
            Betrag::new(Vorzeichen::Negativ, 123, 12)
        );

        let zweite_einzelbuchung = &data.einzelbuchungen[1];
        assert_eq!(zweite_einzelbuchung.datum, Datum::new(2, 1, 2024));
        assert_eq!(zweite_einzelbuchung.name, name("Mit , Komma"));
        assert_eq!(zweite_einzelbuchung.kategorie, kategorie("NeueKategorie"));
        assert_eq!(
            zweite_einzelbuchung.betrag,
            Betrag::new(Vorzeichen::Negativ, 123, 0)
        );

        let erster_dauerauftrag = &data.dauerauftraege[0];
        assert_eq!(erster_dauerauftrag.start_datum, Datum::new(22, 12, 2021));
        assert_eq!(erster_dauerauftrag.ende_datum, Datum::new(24, 12, 2023));
        assert_eq!(erster_dauerauftrag.name, name("Name1"));
        assert_eq!(erster_dauerauftrag.kategorie, kategorie("Kategorie1"));
        assert_eq!(
            erster_dauerauftrag.betrag,
            Betrag::new(Vorzeichen::Negativ, 1233, 0)
        );

        let zweiter_dauerauftrag = &data.dauerauftraege[1];
        assert_eq!(zweiter_dauerauftrag.start_datum, Datum::new(24, 12, 2021));
        assert_eq!(zweiter_dauerauftrag.ende_datum, Datum::new(24, 12, 2025));
        assert_eq!(zweiter_dauerauftrag.name, name("Name2 als ausgabe"));
        assert_eq!(zweiter_dauerauftrag.kategorie, kategorie("Kategorie2"));
        assert_eq!(
            zweiter_dauerauftrag.betrag,
            Betrag::new(Vorzeichen::Negativ, 1233, 0)
        );

        let erste_gemeinsame_buchung = &data.gemeinsame_buchungen[0];
        assert_eq!(erste_gemeinsame_buchung.datum, Datum::new(1, 11, 2024));
        assert_eq!(erste_gemeinsame_buchung.name, name("Name"));
        assert_eq!(
            erste_gemeinsame_buchung.kategorie,
            kategorie("MeineBuchung")
        );
        assert_eq!(
            erste_gemeinsame_buchung.betrag,
            Betrag::new(Vorzeichen::Negativ, 234, 0)
        );
        assert_eq!(erste_gemeinsame_buchung.person, person("Test_User"));

        let zweite_gemeinsame_buchung = &data.gemeinsame_buchungen[1];
        assert_eq!(zweite_gemeinsame_buchung.datum, Datum::new(21, 11, 2024));
        assert_eq!(zweite_gemeinsame_buchung.name, name("asd"));
        assert_eq!(
            zweite_gemeinsame_buchung.kategorie,
            kategorie("PartnerBuchung")
        );
        assert_eq!(
            zweite_gemeinsame_buchung.betrag,
            Betrag::new(Vorzeichen::Negativ, 1234, 0)
        );
        assert_eq!(
            zweite_gemeinsame_buchung.person,
            person("kein_Partnername_gesetzt")
        );

        let erstes_sparkonto = &data.sparkontos[0];
        assert_eq!(erstes_sparkonto.name, name("SparkontoName"));
        assert_eq!(erstes_sparkonto.kontotyp, Kontotyp::Sparkonto);

        let zweites_sparkonto = &data.sparkontos[1];
        assert_eq!(zweites_sparkonto.name, name("DepotName"));
        assert_eq!(zweites_sparkonto.kontotyp, Kontotyp::Depot);

        let erste_sparbuchung = &data.sparbuchungen[0];
        assert_eq!(erste_sparbuchung.datum, Datum::new(1, 1, 2024));
        assert_eq!(erste_sparbuchung.name, name("DerName"));
        assert_eq!(erste_sparbuchung.wert, BetragOhneVorzeichen::new(123, 12));
        assert_eq!(erste_sparbuchung.typ, SparbuchungTyp::Zinsen);
        assert_eq!(erste_sparbuchung.konto, konto_referenz("DasKonto"));

        let zweite_sparbuchung = &data.sparbuchungen[1];
        assert_eq!(zweite_sparbuchung.datum, Datum::new(2, 1, 2024));
        assert_eq!(zweite_sparbuchung.name, name("DerName2"));
        assert_eq!(zweite_sparbuchung.wert, BetragOhneVorzeichen::new(123, 13));
        assert_eq!(zweite_sparbuchung.typ, SparbuchungTyp::Ausschuettung);
        assert_eq!(zweite_sparbuchung.konto, konto_referenz("DasKonto2"));

        let erster_depotwert = &data.depotwerte[0];
        assert_eq!(erster_depotwert.name, name("Name1"));
        assert_eq!(erster_depotwert.isin, isin("ISIN1"));
        assert_eq!(erster_depotwert.typ, DepotwertTyp::ETF);

        let zweiter_depotwert = &data.depotwerte[1];
        assert_eq!(zweiter_depotwert.name, name("Name2"));
        assert_eq!(zweiter_depotwert.isin, isin("ISIN2"));
        assert_eq!(zweiter_depotwert.typ, DepotwertTyp::Crypto);

        let erste_order = &data.order[0];
        assert_eq!(erste_order.datum, Datum::new(1, 1, 2020));
        assert_eq!(erste_order.name, name("MeinName"));
        assert_eq!(erste_order.konto, konto_referenz("MeinKonto"));
        assert_eq!(erste_order.depotwert, depotwert_referenz("MeinDepotwert"));
        assert_eq!(
            erste_order.wert,
            OrderBetrag::new(BetragOhneVorzeichen::new(4, 0), Kauf)
        );

        let zweite_order = &data.order[1];
        assert_eq!(zweite_order.datum, Datum::new(2, 1, 2020));
        assert_eq!(zweite_order.name, name("MeinName2"));
        assert_eq!(zweite_order.konto, konto_referenz("MeinKonto2"));
        assert_eq!(zweite_order.depotwert, depotwert_referenz("MeinDepotwert2"));
        assert_eq!(
            zweite_order.wert,
            OrderBetrag::new(BetragOhneVorzeichen::new(5, 0), Kauf)
        );

        let erste_order_dauerauftrag = &data.order_dauerauftraege[0];
        assert_eq!(erste_order_dauerauftrag.start_datum, Datum::new(1, 1, 2020));
        assert_eq!(erste_order_dauerauftrag.ende_datum, Datum::new(2, 1, 2021));
        assert_eq!(erste_order_dauerauftrag.rhythmus, Rhythmus::Monatlich);
        assert_eq!(erste_order_dauerauftrag.name, name("MeinName"));
        assert_eq!(erste_order_dauerauftrag.konto, konto_referenz("MeinKonto"));
        assert_eq!(
            erste_order_dauerauftrag.depotwert,
            depotwert_referenz("MeinDepotwert")
        );
        assert_eq!(
            erste_order_dauerauftrag.wert,
            OrderBetrag::new(BetragOhneVorzeichen::new(4, 0), Kauf)
        );

        let zweite_order_dauerauftrag = &data.order_dauerauftraege[1];
        assert_eq!(
            zweite_order_dauerauftrag.start_datum,
            Datum::new(2, 1, 2020)
        );
        assert_eq!(zweite_order_dauerauftrag.ende_datum, Datum::new(3, 1, 2021));
        assert_eq!(zweite_order_dauerauftrag.rhythmus, Rhythmus::Monatlich);
        assert_eq!(zweite_order_dauerauftrag.name, name("MeinName2"));
        assert_eq!(
            zweite_order_dauerauftrag.konto,
            konto_referenz("MeinKonto2")
        );
        assert_eq!(
            zweite_order_dauerauftrag.depotwert,
            depotwert_referenz("MeinDepotwert2")
        );
        assert_eq!(
            zweite_order_dauerauftrag.wert,
            OrderBetrag::new(BetragOhneVorzeichen::new(5, 0), Kauf)
        );

        let erster_depotauszug = &data.depotauszuege[0];
        assert_eq!(erster_depotauszug.datum, Datum::new(1, 1, 2020));
        assert_eq!(
            erster_depotauszug.depotwert,
            depotwert_referenz("DE000A0D9PT0")
        );
        assert_eq!(erster_depotauszug.konto, konto_referenz("MeinKonto"));
        assert_eq!(
            erster_depotauszug.wert,
            Betrag::new(Vorzeichen::Positiv, 1000, 0)
        );

        let zweiter_depotauszug = &data.depotauszuege[1];
        assert_eq!(zweiter_depotauszug.datum, Datum::new(2, 1, 2020));
        assert_eq!(
            zweiter_depotauszug.depotwert,
            depotwert_referenz("DE000A0D9PT1")
        );
        assert_eq!(zweiter_depotauszug.konto, konto_referenz("MeinKonto2"));
        assert_eq!(
            zweiter_depotauszug.wert,
            Betrag::new(Vorzeichen::Positiv, 1000, 0)
        );
    }
}
