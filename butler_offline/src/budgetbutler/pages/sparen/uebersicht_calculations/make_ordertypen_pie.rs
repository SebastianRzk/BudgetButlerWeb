use crate::budgetbutler::chart::make_it_percent;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::order_typen::OrderTypen;
use crate::budgetbutler::view::farbe::RandomFarbenSelektor;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::farbe::Farbe;

pub fn make_ordertypen_pie(order_typen: &OrderTypen, konfigurierte_farben: Vec<Farbe>) -> PieChart {
    let farben_selektor = RandomFarbenSelektor::new(konfigurierte_farben);

    make_it_percent(PieChart {
        labels: vec!["Dauerauftrag".to_string(), "Manueller Auftrag".to_string()],
        data: vec![
            order_typen.gesamt_dynamisch.clone(),
            order_typen.gesamt_statisch.clone(),
        ],
        colors: farben_selektor.get_farben_liste(2),
    })
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_calculations::order_typen::OrderTypen;
    use crate::model::primitives::betrag::builder::{p_zero, vier};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::farbe::{gray, green};

    #[test]
    pub fn test_make_ordertypen_pie() {
        let anlagetypen = OrderTypen {
            gesamt_statisch: p_zero(),
            gesamt_dynamisch: vier(),
        };

        let result = super::make_ordertypen_pie(&anlagetypen, vec![green(), gray()]);

        assert_eq!(
            result.labels,
            vec![
                String::from("Dauerauftrag"),
                String::from("Manueller Auftrag")
            ]
        );
        assert_eq!(
            result.data,
            vec![
                Betrag::from_cent(Vorzeichen::Positiv, 10000),
                Betrag::from_cent(Vorzeichen::Positiv, 0)
            ]
        );
        assert_eq!(result.colors, vec![green(), gray()]);
    }
}
