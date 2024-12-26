use crate::budgetbutler::chart::make_it_percent;
use crate::budgetbutler::database::sparen::depotwert_beschreibungen::calc_depotwert_beschreibung;
use crate::budgetbutler::view::farbe::RandomFarbenSelektor;
use crate::model::database::order::OrderTyp;
use crate::model::database::order_dauerauftrag::OrderDauerauftrag;
use crate::model::indiziert::Indiziert;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::persistent_application_state::Database;

pub fn make_aktuelle_dauerauftraege_pie(
    dauerauftraege: &Vec<Indiziert<OrderDauerauftrag>>,
    database: &Database,
    konfigurierte_farben: Vec<Farbe>,
) -> PieChart {
    let farben_selektor = RandomFarbenSelektor::new(konfigurierte_farben);
    let aufbuchungs_dauerauftraege = dauerauftraege
        .iter()
        .filter(|konto| konto.value.wert.get_typ() == OrderTyp::Kauf)
        .collect::<Vec<_>>();

    make_it_percent(PieChart {
        labels: aufbuchungs_dauerauftraege
            .iter()
            .map(|konto| {
                calc_depotwert_beschreibung(&konto.value.depotwert.isin, database).description
            })
            .collect(),
        data: aufbuchungs_dauerauftraege
            .iter()
            .map(|konto| konto.value.wert.get_realer_wert().positiv().clone())
            .collect(),
        colors: farben_selektor.get_farben_liste(aufbuchungs_dauerauftraege.len()),
    })
}

#[cfg(test)]
mod tests {
    use crate::model::database::order::OrderTyp;
    use crate::model::database::order_dauerauftrag::builder::order_dauerauftrag_with_wert;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::farbe::{gray, green};
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_application_state::builder::generate_empty_database;

    #[test]
    fn test_make_uebersicht_kontos_pie_ohne_dauerauftrage_() {
        let dauerauftraege = vec![];

        let result = super::make_aktuelle_dauerauftraege_pie(
            &dauerauftraege,
            &generate_empty_database(),
            vec![green(), gray()],
        );

        assert_eq!(result.labels.len(), 0);
        assert_eq!(result.data.len(), 0);
        assert_eq!(result.colors.len(), 0);
    }
    #[test]
    fn test_make_uebersicht_kontos_pie_ohne_dauerauftrage_einzahlung() {
        let dauerauftraege = vec![
            indiziert(order_dauerauftrag_with_wert(OrderBetrag::new(
                u_zwei(),
                OrderTyp::Dividende,
            ))),
            indiziert(order_dauerauftrag_with_wert(OrderBetrag::new(
                u_zwei(),
                OrderTyp::Verkauf,
            ))),
            indiziert(order_dauerauftrag_with_wert(OrderBetrag::new(
                u_zwei(),
                OrderTyp::SonstigeKosten,
            ))),
            indiziert(order_dauerauftrag_with_wert(OrderBetrag::new(
                u_zwei(),
                OrderTyp::Steuer,
            ))),
        ];

        let result = super::make_aktuelle_dauerauftraege_pie(
            &dauerauftraege,
            &generate_empty_database(),
            vec![green(), gray()],
        );

        assert_eq!(result.labels.len(), 0);
        assert_eq!(result.data.len(), 0);
        assert_eq!(result.colors.len(), 0);
    }

    #[test]
    fn test_make_uebersicht_kontos_pie() {
        let dauerauftraege = vec![indiziert(order_dauerauftrag_with_wert(OrderBetrag::new(
            u_zwei(),
            OrderTyp::Kauf,
        )))];

        let result = super::make_aktuelle_dauerauftraege_pie(
            &dauerauftraege,
            &generate_empty_database(),
            vec![green(), gray()],
        );

        assert_eq!(result.labels, vec!["Unbekannt (TestISIN)".to_string()]);
        assert_eq!(result.data, vec![Betrag::new(Vorzeichen::Positiv, 100, 00)]);
        assert_eq!(result.colors, vec![green()]);
    }
}
