use crate::budgetbutler::chart::make_it_percent;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::berechne_anlagetypen::Anlagetyp;
use crate::budgetbutler::view::farbe::RandomFarbenSelektor;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::farbe::Farbe;

pub fn make_uebersicht_anlagetrypen_pie(
    uebersicht_anlagetypen: &Vec<Anlagetyp>,
    konfigurierte_farben: Vec<Farbe>,
) -> PieChart {
    let farben_selektor = RandomFarbenSelektor::new(konfigurierte_farben);

    make_it_percent(PieChart {
        labels: uebersicht_anlagetypen
            .iter()
            .map(|anlagetyp| anlagetyp.name.clone())
            .collect(),
        data: uebersicht_anlagetypen
            .iter()
            .map(|anlagetyp| anlagetyp.kontostand.clone())
            .collect(),
        colors: farben_selektor.get_farben_liste(uebersicht_anlagetypen.len()),
    })
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_calculations::berechne_anlagetypen::Anlagetyp;
    use crate::model::primitives::betrag::builder::{p_zero, vier};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::farbe::{gray, green};

    #[test]
    pub fn test_make_uebersicht_kontos_pie() {
        let anlagetypen = vec![Anlagetyp {
            kontostand: vier(),
            name: "Test".to_string(),
            gesamte_einzahlungen: p_zero(),
            differenz: p_zero(),
            farbe: green(),
        }];

        let result = super::make_uebersicht_anlagetrypen_pie(&anlagetypen, vec![green(), gray()]);

        assert_eq!(result.labels, vec![String::from("Test")]);
        assert_eq!(
            result.data,
            vec![Betrag::from_cent(Vorzeichen::Positiv, 10000)]
        );
        assert_eq!(result.colors, vec![green()]);
    }
}
