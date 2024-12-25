use crate::budgetbutler::chart::make_it_percent;
use crate::budgetbutler::pages::sparen::uebersicht_kontos::UebersichtKontosViewResult;
use crate::budgetbutler::view::farbe::RandomFarbenSelektor;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::farbe::Farbe;

pub fn make_uebersicht_kontos_pie(
    uebersicht_kontos: &UebersichtKontosViewResult,
    konfigurierte_farben: Vec<Farbe>,
) -> PieChart {
    let farben_selektor = RandomFarbenSelektor::new(konfigurierte_farben);

    make_it_percent(PieChart {
        labels: uebersicht_kontos
            .konten
            .iter()
            .map(|konto| konto.konto.value.name.name.clone())
            .collect(),
        data: uebersicht_kontos
            .konten
            .iter()
            .map(|konto| konto.kontostand.clone())
            .collect(),
        colors: farben_selektor.get_farben_liste(uebersicht_kontos.konten.len()),
    })
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_kontos::{
        KontoMitKontostand, UebersichtKontosViewResult,
    };
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{p_zero, vier, zwei};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::farbe::{gray, green};
    use crate::model::state::persistent_application_state::builder::demo_database_version;

    #[test]
    pub fn test_make_uebersicht_kontos_pie() {
        let uebersicht_kontos = UebersichtKontosViewResult {
            konten: vec![KontoMitKontostand {
                konto: indiziert(demo_konto()),
                kontostand: zwei(),
                aufbuchungen: p_zero(),
                differenz: p_zero(),
            }],
            gesamt: vier(),
            aufbuchungen: p_zero(),
            differenz: p_zero(),
            database_version: demo_database_version(),
        };

        let result = super::make_uebersicht_kontos_pie(&uebersicht_kontos, vec![green(), gray()]);

        assert_eq!(result.labels, vec![demo_konto().name.name]);
        assert_eq!(
            result.data,
            vec![Betrag::from_cent(Vorzeichen::Positiv, 10000)]
        );
        assert_eq!(result.colors, vec![green()]);
    }
}
