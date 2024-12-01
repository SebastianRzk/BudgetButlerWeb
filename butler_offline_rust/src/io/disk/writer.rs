use crate::io::disk::dauerauftrag::dauerauftraege_writer::write_dauerauftraege;
use crate::io::disk::diskrepresentation::file::{File, SortedFile, DAUERAUFTRAEGE_HEADER, DAUERAUFTRAEGE_START_SIGNAL, DAUERAUFTRAG_ORDER_HEADER, DAUERAUFTRAG_ORDER_START_SIGNAL, DEPOTAUSZUEGE_HEADER, DEPOTAUSZUEGE_START_SIGNAL, DEPOTWERTE_HEADER, DEPOTWERTE_START_SIGNAL, EINZELBUCHUNGEN_HEADER, GEMEINSAME_BUCHUGEN_HEADER, GEMEINSAME_BUCHUGEN_START_SIGNAL, ORDER_HEADER, ORDER_START_SIGNAL, SPARBUCHUNGEN_HEADER, SPARBUCHUNGEN_START_SIGNAL, SPARKONTOS_HEADER, SPARKONTOS_START_SIGNAL};
use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::einzelbuchungen::einzelbuchungen_writer::write_einzelbuchungen;
use crate::model::state::config::{BackupConfiguration, DatabaseConfiguration};
use crate::model::state::persistent_application_state::Database;
use std::fs;
use std::io::Write;
use std::path::Path;
use crate::budgetbutler::database::sorter::sort_database;
use crate::io::disk::gemeinsame_buchungen::gemeinsame_buchungen_writer::write_gemeinsame_buchungen;
use crate::model::primitives::datum::Datum;

fn map_database_to_file(database: &Database) -> SortedFile {
    let sorted_database = sort_database(database);
    SortedFile {
        einzelbuchungen: write_einzelbuchungen(&sorted_database),
        dauerauftraege: write_dauerauftraege(&sorted_database),
        gemeinsame_buchungen: write_gemeinsame_buchungen(&sorted_database),
        sparbuchungen: vec![],
        sparkontos: vec![],
        depotwerte: vec![],
        order: vec![],
        dauerauftrag_order: vec![],
        depotauszuege: vec![],
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
    result.extend(sorted_file.dauerauftrag_order);
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

    let file_as_string = file.lines.iter().map(|l| l.line.as_str()).collect::<Vec<&str>>().join("\n");

    fs::write(config.location.as_str(), file_as_string).unwrap();
}


pub fn create_database_backup(database: &Database, backup_configuration: &BackupConfiguration, today: Datum, now: String, reason: &str){
    let filename = format!("Backup_{}_{}_{}.csv", today.to_iso_string(), now, reason);
    let path = Path::new(backup_configuration.location.as_str()).join(filename);
    println!("Creating backup at: {:?}", path);
    let sorted_file = map_database_to_file(database);
    let db_file = map_sorted_to_file(sorted_file);

    let mut file = fs::File::create(path).unwrap();
    for line in db_file.lines {
        file.write_all(&line.line.as_bytes()).unwrap();
        file.write_all("\n".as_bytes()).unwrap();
    }
}
