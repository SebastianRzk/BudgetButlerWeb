use crate::dauerauftraege;
use crate::wiederkehrend::buchung::verarbeite_dauerauftrag;
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::MysqlConnection;
use std::time::SystemTime;

pub fn verarbeite_dauerauftraege(
    mut connection: &mut PooledConnection<ConnectionManager<MysqlConnection>>,
) {
    let start = SystemTime::now();
    let mut anzahl_verarbeiteter_buchungen = 0;
    let auftraege =
        dauerauftraege::output_db_cron::find_all_dauerauftraege_without_user(&mut connection)
            .unwrap();
    for dauerauftrag in auftraege.iter() {
        anzahl_verarbeiteter_buchungen += verarbeite_dauerauftrag(&mut connection, dauerauftrag);
    }
    eprintln!(
        "{:?} Buchungen von {:?} Dauerauftraegen in {:?} verarbeitet",
        anzahl_verarbeiteter_buchungen,
        auftraege.len(),
        start.elapsed()
    );
}
