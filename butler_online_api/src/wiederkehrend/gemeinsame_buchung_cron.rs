use crate::gemeinsame_dauerauftraege;
use crate::wiederkehrend::gemeinsame_buchung::verarbeite_gemeinsame_buchung_dauerauftrag;
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::MysqlConnection;
use std::time::SystemTime;

pub fn verarbeite_gemeinsame_dauerauftraege(
    mut connection: &mut PooledConnection<ConnectionManager<MysqlConnection>>,
) {
    let start = SystemTime::now();
    let mut anzahl_verarbeiteter_buchungen = 0;
    let auftraege = gemeinsame_dauerauftraege::output_db_cron::finde_alle_gemeinsame_dauerauftraege_without_user(&mut connection).unwrap();
    for dauerauftrag in auftraege.iter() {
        anzahl_verarbeiteter_buchungen +=
            verarbeite_gemeinsame_buchung_dauerauftrag(&mut connection, dauerauftrag);
    }
    eprintln!(
        "{:?} Buchungen von {:?} gemeinsamen Dauerauftraegen in {:?} verarbeitet",
        anzahl_verarbeiteter_buchungen,
        auftraege.len(),
        start.elapsed()
    );
}
