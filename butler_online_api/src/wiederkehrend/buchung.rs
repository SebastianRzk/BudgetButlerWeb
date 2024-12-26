use crate::dauerauftraege::model::Dauerauftrag;
use crate::einzelbuchungen::model::NeueEinzelbuchung;
use crate::{dauerauftraege, einzelbuchungen};
use chrono::Local;
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

pub fn verarbeite_dauerauftrag(
    mut connection: &mut PooledConnection<ConnectionManager<MysqlConnection>>,
    dauerauftrag: &Dauerauftrag,
) -> i32 {
    let mut naechste_buchung = crate::wiederkehrend::util::calculate_naechste_buchung(
        dauerauftrag.start_datum,
        dauerauftrag.letzte_ausfuehrung,
        dauerauftrag.rhythmus.clone(),
    );
    let today = crate::wiederkehrend::util::to_date(Local::now().date_naive());
    let mut anzahl_verarbeiteter_buchungen = 0;
    while naechste_buchung.clone() <= today.clone()
        && naechste_buchung.clone() < dauerauftrag.ende_datum.clone()
    {
        anzahl_verarbeiteter_buchungen += 1;
        let neue_buchung = NeueEinzelbuchung {
            datum: naechste_buchung.clone(),
            user: dauerauftrag.user.clone(),
            name: dauerauftrag.name.clone(),
            wert: dauerauftrag.wert.clone(),
            kategorie: dauerauftrag.kategorie.clone(),
        };
        einzelbuchungen::output_db::insert_new_einzelbuchung(&mut connection, neue_buchung)
            .unwrap();
        dauerauftraege::output_db::update_letzte_ausfuehrung(
            &mut connection,
            dauerauftrag.id.clone(),
            naechste_buchung.clone(),
        )
        .unwrap();

        naechste_buchung = crate::wiederkehrend::util::compute_next_date(
            naechste_buchung,
            dauerauftrag.rhythmus.clone(),
        );
    }
    return anzahl_verarbeiteter_buchungen;
}
