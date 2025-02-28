use crate::gemeinsame_buchungen::model::NeueGemeinsameBuchung;
use crate::gemeinsame_dauerauftraege::model::GemeinsamerDauerauftrag;
use crate::{gemeinsame_buchungen, gemeinsame_dauerauftraege};
use chrono::Local;
use diesel::r2d2::{ConnectionManager, PooledConnection};
use diesel::MysqlConnection;

pub fn verarbeite_gemeinsame_buchung_dauerauftrag(
    mut connection: &mut PooledConnection<ConnectionManager<MysqlConnection>>,
    dauerauftrag: &GemeinsamerDauerauftrag,
) -> i32 {
    let mut anzahl_verarbeiteter_buchungen = 0;
    let mut naechste_buchung = crate::wiederkehrend::util::calculate_naechste_buchung(
        dauerauftrag.start_datum,
        dauerauftrag.letzte_ausfuehrung,
        dauerauftrag.rhythmus.clone(),
    );
    let today = crate::wiederkehrend::util::to_date(Local::now().date_naive());
    while naechste_buchung.clone() <= today.clone()
        && naechste_buchung.clone() < dauerauftrag.ende_datum.clone()
    {
        anzahl_verarbeiteter_buchungen += 1;
        let neue_buchung = NeueGemeinsameBuchung {
            datum: naechste_buchung.clone(),
            user: dauerauftrag.user.clone(),
            name: dauerauftrag.name.clone(),
            wert: dauerauftrag.wert.clone(),
            kategorie: dauerauftrag.kategorie.clone(),
            zielperson: dauerauftrag.zielperson.clone(),
        };
        gemeinsame_buchungen::output_db::insert_new_gemeinsame_buchung(
            &mut connection,
            neue_buchung,
        )
        .unwrap();
        gemeinsame_dauerauftraege::output_db::aktualisiere_letzte_ausfuehrung(
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
    anzahl_verarbeiteter_buchungen
}
