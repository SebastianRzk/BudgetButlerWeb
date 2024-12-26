use crate::model::database::sparbuchung::SparbuchungTyp;
use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;
use std::collections::HashMap;

pub struct Kontostand {
    pub letzter_kontostand: Betrag,
    pub gesamte_einzahlungen: Betrag,
}

pub fn berechne_aktuellen_kontostand(konto: Sparkonto, database: &Database) -> Kontostand {
    Kontostand {
        letzter_kontostand: berechne_kontostand(konto.clone(), database),
        gesamte_einzahlungen: berechne_einzahlungen(konto, database),
    }
}

fn berechne_kontostand(konto: Sparkonto, database: &Database) -> Betrag {
    match konto.kontotyp {
        Kontotyp::Sparkonto => berechne_kontostand_fuer_sparkonto(&konto, database),
        Kontotyp::GenossenschaftsAnteile => berechne_kontostand_fuer_sparkonto(&konto, database),
        Kontotyp::Depot => {
            let mut depotwert_map = HashMap::new();
            let auszuege = database
                .depotauszuege
                .select()
                .filter(|k| konto.name == k.value.konto.konto_name)
                .collect();
            for auszug in auszuege {
                let wert = auszug.value.wert;
                let depotwert = auszug.value.depotwert;
                depotwert_map.insert(depotwert.isin.isin, wert);
            }
            depotwert_map
                .values()
                .into_iter()
                .map(|x| x.clone())
                .reduce(|a, b| a + b)
                .unwrap_or_else(Betrag::zero)
        }
    }
}

fn berechne_kontostand_fuer_sparkonto(konto: &Sparkonto, database: &Database) -> Betrag {
    let mut letzter_kontostand = Betrag::zero();
    for sparbuchung in database
        .sparbuchungen
        .select()
        .filter(|buchung| buchung.value.konto.konto_name == konto.name)
        .collect()
    {
        match sparbuchung.value.typ {
            SparbuchungTyp::ManuelleEinzahlung => {
                letzter_kontostand = letzter_kontostand + sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::ManuelleAuszahlung => {
                letzter_kontostand = letzter_kontostand - sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::Zinsen => {
                letzter_kontostand = letzter_kontostand + sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::Ausschuettung => {}
            SparbuchungTyp::SonstigeKosten => {}
        }
    }

    letzter_kontostand
}

fn berechne_einzahlungen(konto: Sparkonto, database: &Database) -> Betrag {
    let mut gesamte_einzahlungen = Betrag::zero();
    for sparbuchung in database
        .sparbuchungen
        .select()
        .filter(|buchung| buchung.value.konto.konto_name == konto.name)
        .collect()
    {
        match sparbuchung.value.typ {
            SparbuchungTyp::ManuelleEinzahlung => {
                gesamte_einzahlungen = gesamte_einzahlungen + sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::ManuelleAuszahlung => {
                gesamte_einzahlungen = gesamte_einzahlungen - sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::Zinsen => {}
            SparbuchungTyp::Ausschuettung => {
                gesamte_einzahlungen = gesamte_einzahlungen - sparbuchung.value.wert.positiv();
            }
            SparbuchungTyp::SonstigeKosten => {
                gesamte_einzahlungen = gesamte_einzahlungen + sparbuchung.value.wert.positiv();
            }
        }
    }

    for order in database
        .order
        .select()
        .filter(|order| order.value.konto.konto_name == konto.name)
        .collect()
    {
        gesamte_einzahlungen =
            gesamte_einzahlungen + order.value.wert.get_betrag_fuer_geleistete_investition();
    }

    gesamte_einzahlungen
}

#[cfg(test)]
mod tests_fuer_depot {
    use crate::budgetbutler::database::sparen::kontostand_berechner::berechne_aktuellen_kontostand;
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::order::builder::order_with_konto_und_betrag;
    use crate::model::database::sparbuchung::builder::sparbuchung_with_betrag_typ_und_konto;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::builder::{any_konto_with_typ, demo_konto};
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::initial_config::database::generate_initial_database;
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::order_betrag::builder::kauf;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotauszuege, generate_database_with_orders,
        generate_database_with_sparbuchungen,
    };

    #[test]
    fn test_berechne_kontostand_fuer_leere_db() {
        let database = generate_initial_database();

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            Betrag::zero()
        );

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            Betrag::zero()
        );

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            Betrag::zero()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_order_beruecksichtigen() {
        let database = generate_database_with_orders(vec![order_with_konto_und_betrag(
            demo_konto().as_reference(),
            kauf(u_zwei()),
        )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_depotauszuege_beruecksichtigen() {
        let database = generate_database_with_depotauszuege(vec![
            Depotauszug {
                konto: demo_konto().as_reference(),
                wert: vier(),
                depotwert: demo_depotwert_referenz(),
                datum: any_datum(),
            },
            Depotauszug {
                konto: demo_konto().as_reference(),
                wert: zwei(),
                depotwert: demo_depotwert_referenz(),
                datum: Datum::first(),
            },
        ]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            vier()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            Betrag::zero()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_sparbuchungen_ausschuettung_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::Ausschuettung,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            minus_zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_sparbuchungen_sonstige_kosten_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::SonstigeKosten,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_sparbuchungen_zinsen_ignorieren() {
        assert_nothing_changed(SparbuchungTyp::Zinsen);
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_manuelle_einzahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleEinzahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_fuer_depot_sollte_manuelle_auszahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleAuszahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            minus_zwei()
        );
    }

    fn assert_nothing_changed(typ: SparbuchungTyp) {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Depot), &database)
                .gesamte_einzahlungen,
            Betrag::zero()
        );
    }
}

#[cfg(test)]
mod tests_fuer_sparkonto {
    use crate::budgetbutler::database::sparen::kontostand_berechner::berechne_aktuellen_kontostand;
    use crate::model::database::sparbuchung::builder::sparbuchung_with_betrag_typ_und_konto;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::builder::{any_konto_with_typ, demo_konto};
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::betrag::builder::{minus_zwei, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparbuchungen;

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_ausschuettung_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::Ausschuettung,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            minus_zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_sonstige_kosten_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::SonstigeKosten,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_zinsen_ignorieren() {
        let typ = SparbuchungTyp::Zinsen;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            Betrag::zero()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_manuelle_einzahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleEinzahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_manuelle_auszahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleAuszahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .letzter_kontostand,
            minus_zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(any_konto_with_typ(Kontotyp::Sparkonto), &database)
                .gesamte_einzahlungen,
            minus_zwei()
        );
    }
}

#[cfg(test)]
mod tests_fuer_genossenschaftsanteile {
    use crate::budgetbutler::database::sparen::kontostand_berechner::berechne_aktuellen_kontostand;
    use crate::model::database::sparbuchung::builder::sparbuchung_with_betrag_typ_und_konto;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::builder::{any_konto_with_typ, demo_konto};
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::betrag::builder::{minus_zwei, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparbuchungen;

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_ausschuettung_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::Ausschuettung,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            minus_zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_sonstige_kosten_beruecksichtigen() {
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::SonstigeKosten,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            Betrag::zero()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_sparbuchungen_zinsen_ignorieren() {
        let typ = SparbuchungTyp::Zinsen;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            Betrag::zero()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_manuelle_einzahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleEinzahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            zwei()
        );
    }

    #[test]
    fn test_berechne_kontostand_sollte_manuelle_auszahlung_beruecksichtigen() {
        let typ = SparbuchungTyp::ManuelleAuszahlung;
        let database =
            generate_database_with_sparbuchungen(vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                typ,
                demo_konto().as_reference(),
            )]);

        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .letzter_kontostand,
            minus_zwei()
        );
        assert_eq!(
            berechne_aktuellen_kontostand(
                any_konto_with_typ(Kontotyp::GenossenschaftsAnteile),
                &database
            )
            .gesamte_einzahlungen,
            minus_zwei()
        );
    }
}
