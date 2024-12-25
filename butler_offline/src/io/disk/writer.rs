use crate::budgetbutler::database::sorter::sort_database;
use crate::io::disk::database::dauerauftrag::dauerauftraege_writer::write_dauerauftraege;
use crate::io::disk::database::depotauszuege::depotauszuege_writer::write_depotauszuege;
use crate::io::disk::database::depotwerte::depotwerte_writer::write_depotwerte;
use crate::io::disk::database::einzelbuchungen::einzelbuchungen_writer::write_einzelbuchungen;
use crate::io::disk::database::gemeinsame_buchungen::gemeinsame_buchungen_writer::write_gemeinsame_buchungen;
use crate::io::disk::database::order::orders_writer::write_orders;
use crate::io::disk::database::order_dauerauftraege::order_dauerauftraege_writer::write_order_dauerauftraege;
use crate::io::disk::database::sparbuchungen::sparbuchungen_writer::write_sparbuchungen;
use crate::io::disk::database::sparkontos::sparkontos_writer::write_sparkontos;
use crate::io::disk::diskrepresentation::file::{
    File, SortedFile, DAUERAUFTRAEGE_HEADER, DAUERAUFTRAEGE_START_SIGNAL,
    DAUERAUFTRAG_ORDER_HEADER, DAUERAUFTRAG_ORDER_START_SIGNAL, DEPOTAUSZUEGE_HEADER,
    DEPOTAUSZUEGE_START_SIGNAL, DEPOTWERTE_HEADER, DEPOTWERTE_START_SIGNAL, EINZELBUCHUNGEN_HEADER,
    GEMEINSAME_BUCHUGEN_HEADER, GEMEINSAME_BUCHUGEN_START_SIGNAL, ORDER_HEADER, ORDER_START_SIGNAL,
    SPARBUCHUNGEN_HEADER, SPARBUCHUNGEN_START_SIGNAL, SPARKONTOS_HEADER, SPARKONTOS_START_SIGNAL,
};
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::primitives::datum::Datum;
use crate::model::state::config::{
    app_root, get_database_location, BackupConfiguration, DatabaseConfiguration,
};
use crate::model::state::persistent_application_state::Database;
use std::fs;
use std::io::Write;
use std::path::Path;

fn map_database_to_file(database: &Database) -> SortedFile {
    let sorted_database = sort_database(database);
    SortedFile {
        einzelbuchungen: write_einzelbuchungen(&sorted_database),
        dauerauftraege: write_dauerauftraege(&sorted_database),
        gemeinsame_buchungen: write_gemeinsame_buchungen(&sorted_database),
        sparbuchungen: write_sparbuchungen(&sorted_database),
        sparkontos: write_sparkontos(&sorted_database),
        depotwerte: write_depotwerte(&sorted_database),
        order: write_orders(&sorted_database),
        order_dauerauftrag: write_order_dauerauftraege(&sorted_database),
        depotauszuege: write_depotauszuege(&sorted_database),
    }
}

pub fn map_sorted_to_file(sorted_file: SortedFile) -> File {
    let mut result: Vec<Line> = vec![];
    result.push(Line::new(EINZELBUCHUNGEN_HEADER));
    result.extend(sorted_file.einzelbuchungen);
    result.push(Line::empty_line());

    result.push(Line::new(DAUERAUFTRAEGE_START_SIGNAL));
    result.push(Line::new(DAUERAUFTRAEGE_HEADER));
    result.extend(sorted_file.dauerauftraege);
    result.push(Line::empty_line());

    result.push(Line::new(GEMEINSAME_BUCHUGEN_START_SIGNAL));
    result.push(Line::new(GEMEINSAME_BUCHUGEN_HEADER));
    result.extend(sorted_file.gemeinsame_buchungen);
    result.push(Line::empty_line());

    result.push(Line::new(SPARBUCHUNGEN_START_SIGNAL));
    result.push(Line::new(SPARBUCHUNGEN_HEADER));
    result.extend(sorted_file.sparbuchungen);
    result.push(Line::empty_line());

    result.push(Line::new(SPARKONTOS_START_SIGNAL));
    result.push(Line::new(SPARKONTOS_HEADER));
    result.extend(sorted_file.sparkontos);
    result.push(Line::empty_line());

    result.push(Line::new(DEPOTWERTE_START_SIGNAL));
    result.push(Line::new(DEPOTWERTE_HEADER));
    result.extend(sorted_file.depotwerte);
    result.push(Line::empty_line());

    result.push(Line::new(ORDER_START_SIGNAL));
    result.push(Line::new(ORDER_HEADER));
    result.extend(sorted_file.order);
    result.push(Line::empty_line());

    result.push(Line::new(DAUERAUFTRAG_ORDER_START_SIGNAL));
    result.push(Line::new(DAUERAUFTRAG_ORDER_HEADER));
    result.extend(sorted_file.order_dauerauftrag);
    result.push(Line::empty_line());

    result.push(Line::new(DEPOTAUSZUEGE_START_SIGNAL));
    result.push(Line::new(DEPOTAUSZUEGE_HEADER));
    result.extend(sorted_file.depotauszuege);
    result.push(Line::empty_line());

    File { lines: result }
}

pub fn write_database(database: &Database, config: &DatabaseConfiguration) {
    let sorted_file = map_database_to_file(database);
    let file = map_sorted_to_file(sorted_file);

    let file_as_string = file
        .lines
        .iter()
        .map(|l| l.line.as_str())
        .collect::<Vec<&str>>()
        .join("\n");

    fs::write(get_database_location(config).as_os_str(), file_as_string).unwrap();
}

pub fn create_database_backup(
    database: &Database,
    backup_configuration: &BackupConfiguration,
    today: Datum,
    now: String,
    reason: &str,
) {
    let filename = format!("Backup_{}_{}_{}.csv", today.to_iso_string(), now, reason);
    let path = app_root()
        .join(Path::new(backup_configuration.location.as_str()))
        .join(filename);
    println!("Creating backup at: {:?}", path);
    let sorted_file = map_database_to_file(database);
    let db_file = map_sorted_to_file(sorted_file);

    let mut file = fs::File::create(path).unwrap();
    for line in db_file.lines {
        file.write_all(&line.line.as_bytes()).unwrap();
        file.write_all("\n".as_bytes()).unwrap();
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::io::disk::diskrepresentation::file::File;
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::io::disk::reader::read_data;
    use crate::io::disk::writer::{map_database_to_file, map_sorted_to_file};
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::state::persistent_application_state::builder::demo_database_version;

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
2024-01-01,DerName,123.12,Ausschüttung,DasKonto
2024-01-02,DerName2,123.13,Zinsen,DasKonto2

Sparkontos
Kontoname,Kontotyp
DepotName,Depot
SparkontoName,Sparkonto

Depotwerte
Name,ISIN,Typ
Name1,ISIN1,ETF
Name2,ISIN2,Crypto

Order
Datum,Name,Konto,Depotwert,Wert,Typ
2020-01-01,MeinName,MeinKonto,MeinDepotwert,4.00,Kauf
2020-01-02,MeinName2,MeinKonto2,MeinDepotwert2,5.00,Verkauf

Dauerauftr_Ordr
Startdatum,Endedatum,Rhythmus,Name,Konto,Depotwert,Wert,Typ
2021-12-22,2023-12-24,monatlich,Name1,MeinKonto,MeinDepotwert,4.00,Kauf
2021-12-24,2025-12-24,halbjährlich,Name2,MeinKonto2,MeinDepotwert2,5.00,Verkauf

Depotauszuege
Datum,Depotwert,Konto,Wert
2024-01-01,MeinDepotwert,MeinKonto,4.00
2024-01-02,MeinDepotwert2,MeinKonto2,5.00
";

    #[test]
    fn test_read_and_write() {
        let file = File::from_str(BEISPIEL_DATENBANK);
        let data = read_data(file);
        let database = create_database(data, any_datum(), demo_database_version());

        let sorted_file = map_database_to_file(&database);
        let result_file = map_sorted_to_file(sorted_file);

        assert_eq!(as_string(&result_file.lines), BEISPIEL_DATENBANK);
    }
}
