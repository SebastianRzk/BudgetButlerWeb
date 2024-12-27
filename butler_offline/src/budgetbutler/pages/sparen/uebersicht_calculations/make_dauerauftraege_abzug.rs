use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::budgetbutler::pages::sparen::uebersicht_sparen::DauerauftragAbzug;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::persistent_application_state::Database;

pub fn make_dauerauftraege_abzuge(
    dauerauftraege: Vec<Indiziert<OrderDauerauftrag>>,
    konfigurierte_farben: Vec<Farbe>,
    database: &Database,
) -> Vec<DauerauftragAbzug> {
    let mut result = vec![];

    if dauerauftraege.is_empty() {
        return result;
    }

    for dauerauftrag in dauerauftraege.iter() {
        let dauerauftrag_abzug = DauerauftragAbzug {
            name: dauerauftrag.value.name.clone(),
            depotwert_beschreibung: calc_depotwert_beschreibung(
                &dauerauftrag.value.depotwert.isin,
                database,
            )
            .description,
            wert: dauerauftrag.value.wert.clone(),
            farbe: konfigurierte_farben[result.len() % konfigurierte_farben.len()].clone(),
        };
        result.push(dauerauftrag_abzug);
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::model::database::order_dauerauftrag::builder::demo_order_dauerauftrag;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::farbe::green;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_make_dauerauftraege_abzuge_leer() {
        let dauerauftraege = vec![];
        let konfigurierte_farben = vec![];
        let database = generate_empty_database();
        let result =
            super::make_dauerauftraege_abzuge(dauerauftraege, konfigurierte_farben, &database);
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_make_dauerauftraege_abzuge() {
        let dauerauftraege = vec![indiziert(demo_order_dauerauftrag())];
        let konfigurierte_farben = vec![green()];
        let database = generate_empty_database();

        let result =
            super::make_dauerauftraege_abzuge(dauerauftraege, konfigurierte_farben, &database);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, demo_order_dauerauftrag().name);
        assert_eq!(
            result[0].depotwert_beschreibung,
            "Unbekannt (MeinDepotwert)"
        );
        assert_eq!(result[0].wert, demo_order_dauerauftrag().wert);
        assert_eq!(result[0].farbe, green());
    }
}
