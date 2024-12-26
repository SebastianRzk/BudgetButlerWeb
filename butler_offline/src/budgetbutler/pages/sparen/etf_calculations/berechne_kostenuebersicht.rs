use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    DepotwertMitDaten, ETFKosten, ETFKostenUebersicht,
};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::prozent::Prozent;

pub fn berechne_kostenuebersicht(
    depotwerte_mit_kontostand: &Vec<DepotwertMitDaten>,
    gesamt_summe: Betrag,
) -> ETFKostenUebersicht {
    let mut gesamtkosten_euro = Betrag::zero();
    let mut depotwerte = vec![];

    for depotwert_mit_kontostand in depotwerte_mit_kontostand.iter() {
        let kosten_prozent =
            Prozent::from_float_representation(depotwert_mit_kontostand.data.data.kosten);
        let kosten_euro = depotwert_mit_kontostand
            .aktueller_kontostand
            .anteil(&kosten_prozent);
        gesamtkosten_euro = gesamtkosten_euro + kosten_euro.clone();

        depotwerte.push(ETFKosten {
            name: depotwert_mit_kontostand.depotwert.name.name.clone(),
            prozent: kosten_prozent,
            euro: kosten_euro,
        });
    }

    ETFKostenUebersicht {
        gesamt: ETFKosten {
            name: "Gesamt".to_string(),
            prozent: Prozent::from_betrags_differenz(&gesamtkosten_euro, &gesamt_summe),
            euro: gesamt_summe,
        },
        data: depotwerte,
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotwert::builder::depotwert_mit_name;
    use crate::model::primitives::betrag::builder::betrag;
    use crate::model::primitives::betrag::Vorzeichen::Positiv;
    use crate::model::shares::builder::share_data_mit_kosten;

    #[test]
    fn test_berechne_kostenuebersicht() {
        use crate::budgetbutler::pages::sparen::etf_calculations::berechne_kostenuebersicht::berechne_kostenuebersicht;
        use crate::budgetbutler::pages::sparen::uebersicht_etfs::DepotwertMitDaten;
        use crate::model::primitives::betrag::Betrag;
        use crate::model::primitives::prozent::Prozent;

        let depotwerte_mit_kontostand = vec![
            DepotwertMitDaten {
                depotwert: depotwert_mit_name("Depotwert1"),
                data: share_data_mit_kosten(0.25),
                aktueller_kontostand: betrag(1000),
            },
            DepotwertMitDaten {
                depotwert: depotwert_mit_name("Depotwert2"),
                data: share_data_mit_kosten(0.1),
                aktueller_kontostand: betrag(2000),
            },
        ];

        let gesamt_summe = betrag(3000);

        let result = berechne_kostenuebersicht(&depotwerte_mit_kontostand, gesamt_summe);

        assert_eq!(result.gesamt.euro, betrag(3000));
        assert_eq!(
            result.gesamt.prozent,
            Prozent::from_str_representation("0.15")
        );
        assert_eq!(result.data.len(), 2);
        assert_eq!(result.data[0].euro, Betrag::new(Positiv, 2, 50));
        assert_eq!(
            result.data[0].prozent,
            Prozent::from_str_representation("0.25")
        );
        assert_eq!(result.data[1].euro, betrag(2));
        assert_eq!(
            result.data[1].prozent,
            Prozent::from_str_representation("0.1")
        );
    }
}
