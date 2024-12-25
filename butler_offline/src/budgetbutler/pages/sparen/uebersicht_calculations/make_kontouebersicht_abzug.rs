use crate::budgetbutler::pages::sparen::uebersicht_kontos::UebersichtKontosViewResult;
use crate::budgetbutler::pages::sparen::uebersicht_sparen::{
    KontoMitKontostandUndFarbe, UebersichtKontos,
};
use crate::model::primitives::farbe::Farbe;

pub fn make_kontouebersicht_abzug(
    kontoueberischt: UebersichtKontosViewResult,
    farben: Vec<Farbe>,
) -> UebersichtKontos {
    let mut konten = vec![];

    for konto in &kontoueberischt.konten {
        let farbe = farben.get(konten.len() % farben.len()).unwrap().clone();
        konten.push(KontoMitKontostandUndFarbe {
            konto: konto.konto.clone(),
            kontostand: konto.kontostand.clone(),
            aufbuchungen: konto.aufbuchungen.clone(),
            differenz: konto.differenz.clone(),
            farbe,
        });
    }

    UebersichtKontos {
        konten,
        gesamt: kontoueberischt.gesamt.clone(),
        aufbuchungen: kontoueberischt.aufbuchungen.clone(),
        differenz: kontoueberischt.differenz.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_kontos::{
        KontoMitKontostand, UebersichtKontosViewResult,
    };
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{fuenf, vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::farbe::green;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, generate_empty_database,
    };

    #[test]
    fn test_make_kontouebersicht_abzug_empty() {
        let kontouebersicht = UebersichtKontosViewResult {
            konten: vec![],
            gesamt: Betrag::zero(),
            aufbuchungen: Betrag::zero(),
            differenz: Betrag::zero(),
            database_version: demo_database_version(),
        };

        let result = super::make_kontouebersicht_abzug(kontouebersicht, vec![green()]);

        assert_eq!(result.konten.len(), 0);
        assert_eq!(result.gesamt, Betrag::zero());
        assert_eq!(result.aufbuchungen, Betrag::zero());
        assert_eq!(result.differenz, Betrag::zero());
    }

    #[test]
    fn test_make_kontouebersicht_abzug() {
        let konten = vec![KontoMitKontostand {
            konto: indiziert(demo_konto()),
            kontostand: fuenf(),
            aufbuchungen: vier(),
            differenz: zwei(),
        }];
        let gesamt = vier();
        let aufbuchungen = zwei();
        let differenz = fuenf();
        let database_version = generate_empty_database().db_version.clone();

        let kontouebersicht = UebersichtKontosViewResult {
            konten,
            gesamt,
            aufbuchungen,
            differenz,
            database_version,
        };

        let result = super::make_kontouebersicht_abzug(kontouebersicht, vec![green()]);

        assert_eq!(result.konten.len(), 1);
        assert_eq!(result.konten[0].konto.value, demo_konto());
        assert_eq!(result.konten[0].kontostand, fuenf());
        assert_eq!(result.konten[0].aufbuchungen, vier());
        assert_eq!(result.konten[0].differenz, zwei());
        assert_eq!(result.konten[0].farbe, green());

        assert_eq!(result.gesamt, vier());
        assert_eq!(result.aufbuchungen, zwei());
        assert_eq!(result.differenz, fuenf());
    }
}
