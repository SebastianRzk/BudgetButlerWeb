use crate::dauerauftraege;
use crate::dauerauftraege::model::Dauerauftrag;
use crate::einzelbuchungen::model::NeueEinzelbuchung;
use crate::einzelbuchungen::output_db;
use chrono::Local;
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::MysqlConnection;

pub fn verarbeite_dauerauftrag(
    connection: &mut PooledConnection<ConnectionManager<MysqlConnection>>,
    dauerauftrag: &Dauerauftrag,
) -> i32 {
    let mut naechste_buchung = crate::wiederkehrend::util::calculate_naechste_buchung(
        dauerauftrag.start_datum,
        dauerauftrag.letzte_ausfuehrung,
        dauerauftrag.rhythmus.clone(),
    );
    let today = crate::wiederkehrend::util::to_date(Local::now().date_naive());
    let mut anzahl_verarbeiteter_buchungen = 0;
    while naechste_buchung <= today
        && naechste_buchung < dauerauftrag.ende_datum
    {
        anzahl_verarbeiteter_buchungen += 1;
        let neue_buchung = NeueEinzelbuchung {
            datum: naechste_buchung,
            user: dauerauftrag.user.clone(),
            name: dauerauftrag.name.clone(),
            wert: dauerauftrag.wert.clone(),
            kategorie: dauerauftrag.kategorie.clone(),
        };
        output_db::repository::insert_new_einzelbuchung(connection, neue_buchung).unwrap();
        dauerauftraege::output_db::update_letzte_ausfuehrung(
            connection,
            dauerauftrag.id.clone(),
            naechste_buchung,
        )
        .unwrap();

        naechste_buchung = crate::wiederkehrend::util::compute_next_date(
            naechste_buchung,
            dauerauftrag.rhythmus.clone(),
        );
    }
    anzahl_verarbeiteter_buchungen
}
