use crate::budgetbutler::database::sparen::depotwert_stand_berechner::berechne_aktuellen_depotwert_stand;
use crate::budgetbutler::database::sparen::kontostand_berechner::berechne_aktuellen_kontostand;
use crate::model::database::depotwert::DepotwertTyp;
use crate::model::database::sparkonto::Kontotyp;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::farbe::Farbe;
use crate::model::state::persistent_application_state::Database;

#[derive(Clone)]
pub struct Anlagetyp {
    pub farbe: Farbe,
    pub name: String,
    pub gesamte_einzahlungen: Betrag,
    pub differenz: Betrag,
    pub kontostand: Betrag,
}

#[derive(Clone)]
pub struct AnlagetypOhneFarbe {
    pub name: String,
    pub gesamte_einzahlungen: Betrag,
    pub differenz: Betrag,
    pub kontostand: Betrag,
}

pub fn berechne_anlagetypen(database: &Database, farbe: Vec<Farbe>) -> Vec<Anlagetyp> {
    let mut sparkonto_einzahlungen = Betrag::zero();
    let mut sparkonto_diff = Betrag::zero();
    let mut sparkonto_kontostand = Betrag::zero();

    let mut genossenschaft_einzahlungen = Betrag::zero();
    let mut genossenschaft_diff = Betrag::zero();
    let mut genossenschaft_kontostand = Betrag::zero();

    let mut etc_einzahlungen = Betrag::zero();
    let mut etf_diff = Betrag::zero();
    let mut etc_kontostand = Betrag::zero();

    let mut fond_einzahlungen = Betrag::zero();
    let mut fond_diff = Betrag::zero();
    let mut fond_kontostand = Betrag::zero();

    let mut aktie_einzahlungen = Betrag::zero();
    let mut aktie_diff = Betrag::zero();
    let mut aktie_kontostand = Betrag::zero();

    let mut crypto_einzahlungen = Betrag::zero();
    let mut crypto_diff = Betrag::zero();
    let mut crypto_kontostand = Betrag::zero();

    let mut robot_einzahlungen = Betrag::zero();
    let mut robot_diff = Betrag::zero();
    let mut robot_kontostand = Betrag::zero();

    for konto in &database.sparkontos.sparkontos {
        match konto.value.kontotyp {
            Kontotyp::Sparkonto => {
                let ergebnis = berechne_aktuellen_kontostand(konto.value.clone(), &database);
                sparkonto_einzahlungen =
                    sparkonto_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                sparkonto_diff = sparkonto_diff + ergebnis.letzter_kontostand.clone()
                    - ergebnis.gesamte_einzahlungen;
                sparkonto_kontostand = sparkonto_kontostand + ergebnis.letzter_kontostand;
            }
            Kontotyp::Depot => {}
            Kontotyp::GenossenschaftsAnteile => {
                let ergebnis = berechne_aktuellen_kontostand(konto.value.clone(), &database);
                genossenschaft_einzahlungen =
                    genossenschaft_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                genossenschaft_diff = genossenschaft_diff + ergebnis.letzter_kontostand.clone()
                    - ergebnis.gesamte_einzahlungen;
                genossenschaft_kontostand = genossenschaft_kontostand + ergebnis.letzter_kontostand;
            }
        }
    }

    for depotwert in &database.depotwerte.depotwerte {
        let ergebnis = berechne_aktuellen_depotwert_stand(depotwert.value.as_referenz(), &database);

        match depotwert.value.typ {
            DepotwertTyp::ETF => {
                etc_einzahlungen = etc_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                etf_diff = etf_diff - ergebnis.gesamte_einzahlungen.clone()
                    + ergebnis.letzter_kontostand.clone();
                etc_kontostand = etc_kontostand + ergebnis.letzter_kontostand;
            }
            DepotwertTyp::Fond => {
                fond_einzahlungen = fond_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                fond_diff =
                    fond_diff + ergebnis.letzter_kontostand.clone() - ergebnis.gesamte_einzahlungen;
                fond_kontostand = fond_kontostand + ergebnis.letzter_kontostand;
            }
            DepotwertTyp::Einzelaktie => {
                aktie_einzahlungen = aktie_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                aktie_diff = aktie_diff + ergebnis.letzter_kontostand.clone()
                    - ergebnis.gesamte_einzahlungen;
                aktie_kontostand = aktie_kontostand + ergebnis.letzter_kontostand;
            }
            DepotwertTyp::Crypto => {
                crypto_einzahlungen = crypto_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                crypto_diff = crypto_diff + ergebnis.letzter_kontostand.clone()
                    - ergebnis.gesamte_einzahlungen;
                crypto_kontostand = crypto_kontostand + ergebnis.letzter_kontostand;
            }
            DepotwertTyp::Robot => {
                robot_einzahlungen = robot_einzahlungen + ergebnis.gesamte_einzahlungen.clone();
                robot_diff = robot_diff + ergebnis.letzter_kontostand.clone()
                    - ergebnis.gesamte_einzahlungen;
                robot_kontostand = robot_kontostand + ergebnis.letzter_kontostand;
            }
        }
    }

    let anlagetypen = vec![
        AnlagetypOhneFarbe {
            name: "Sparkonto".to_string(),
            gesamte_einzahlungen: sparkonto_einzahlungen,
            differenz: sparkonto_diff,
            kontostand: sparkonto_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "Genossenschaftsanteile".to_string(),
            gesamte_einzahlungen: genossenschaft_einzahlungen,
            differenz: genossenschaft_diff,
            kontostand: genossenschaft_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "ETF".to_string(),
            gesamte_einzahlungen: etc_einzahlungen,
            differenz: etf_diff,
            kontostand: etc_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "Fond".to_string(),
            gesamte_einzahlungen: fond_einzahlungen,
            differenz: fond_diff,
            kontostand: fond_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "Aktie".to_string(),
            gesamte_einzahlungen: aktie_einzahlungen,
            differenz: aktie_diff,
            kontostand: aktie_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "Crypto".to_string(),
            gesamte_einzahlungen: crypto_einzahlungen,
            differenz: crypto_diff,
            kontostand: crypto_kontostand,
        },
        AnlagetypOhneFarbe {
            name: "Robo Advisor".to_string(),
            gesamte_einzahlungen: robot_einzahlungen,
            differenz: robot_diff,
            kontostand: robot_kontostand,
        },
    ];

    let ohne_farbe = anlagetypen
        .iter()
        .filter(|anlagetyp| anlagetyp.gesamte_einzahlungen > Betrag::zero())
        .map(|anlagetyp| anlagetyp.clone())
        .collect();
    add_farbe(ohne_farbe, farbe)
}

fn add_farbe(anlagetypen: Vec<AnlagetypOhneFarbe>, farben: Vec<Farbe>) -> Vec<Anlagetyp> {
    let mut result = vec![];
    for (anlagetyp, farbe) in anlagetypen.iter().zip(farben.iter().cycle()) {
        result.push(Anlagetyp {
            farbe: farbe.clone(),
            name: anlagetyp.name.clone(),
            gesamte_einzahlungen: anlagetyp.gesamte_einzahlungen.clone(),
            differenz: anlagetyp.differenz.clone(),
            kontostand: anlagetyp.kontostand.clone(),
        });
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_vier;
    use crate::model::primitives::datum::builder::{any_datum, demo_datum};
    use crate::model::primitives::farbe::green;
    use crate::model::primitives::isin::builder::demo_isin;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::builder::kauf;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_sparkontos, generate_database_with_sparkontos_und_sparbuchungen,
        generate_empty_database,
    };
    use crate::model::state::persistent_state::depotauszuege::Depotauszuege;
    use crate::model::state::persistent_state::depotwerte::Depotwerte;
    use crate::model::state::persistent_state::order::Orders;

    #[test]
    fn test_berechne_anlagetypen_leere_db() {
        let result = super::berechne_anlagetypen(&generate_empty_database(), vec![green()]);

        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_should_contain_sparbuchungen() {
        let konto = Sparkonto {
            name: demo_name(),
            kontotyp: Kontotyp::Sparkonto,
        };
        let database = generate_database_with_sparkontos_und_sparbuchungen(
            vec![konto.clone()],
            vec![Sparbuchung {
                konto: konto.as_reference(),
                name: demo_name(),
                datum: any_datum(),
                typ: SparbuchungTyp::ManuelleEinzahlung,
                wert: u_vier(),
            }],
        );
        let result = super::berechne_anlagetypen(&database, vec![green()]);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, "Sparkonto");
        assert_eq!(result[0].gesamte_einzahlungen, vier());
        assert_eq!(result[0].differenz, Betrag::zero());
        assert_eq!(result[0].kontostand, vier());
        assert_eq!(result[0].farbe, green());
    }

    #[test]
    fn test_should_contain_genossenschaftsanteile() {
        let konto = Sparkonto {
            name: demo_name(),
            kontotyp: Kontotyp::GenossenschaftsAnteile,
        };
        let database = generate_database_with_sparkontos_und_sparbuchungen(
            vec![konto.clone()],
            vec![Sparbuchung {
                konto: konto.as_reference(),
                name: demo_name(),
                datum: any_datum(),
                typ: SparbuchungTyp::ManuelleEinzahlung,
                wert: u_vier(),
            }],
        );
        let result = super::berechne_anlagetypen(&database, vec![green()]);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, "Genossenschaftsanteile");
        assert_eq!(result[0].gesamte_einzahlungen, vier());
        assert_eq!(result[0].differenz, Betrag::zero());
        assert_eq!(result[0].kontostand, vier());
        assert_eq!(result[0].farbe, green());
    }

    #[test]
    fn test_should_contain_etfs() {
        let typ = DepotwertTyp::ETF;
        let expected_name = "ETF";
        assert_depotumsatz(typ, expected_name);
    }
    #[test]
    fn test_should_contain_aktien() {
        let typ = DepotwertTyp::Einzelaktie;
        let expected_name = "Aktie";
        assert_depotumsatz(typ, expected_name);
    }

    #[test]
    fn test_should_contain_fond() {
        let typ = DepotwertTyp::Fond;
        let expected_name = "Fond";
        assert_depotumsatz(typ, expected_name);
    }

    #[test]
    fn test_should_contain_robo() {
        let typ = DepotwertTyp::Robot;
        let expected_name = "Robo Advisor";
        assert_depotumsatz(typ, expected_name);
    }

    #[test]
    fn test_should_contain_crypt() {
        let typ = DepotwertTyp::Crypto;
        let expected_name = "Crypto";
        assert_depotumsatz(typ, expected_name);
    }

    fn assert_depotumsatz(typ: DepotwertTyp, expected_name: &str) {
        let konto = Sparkonto {
            name: demo_name(),
            kontotyp: Kontotyp::Depot,
        };
        let depotwert = Depotwert {
            name: demo_name(),
            isin: demo_isin(),
            typ: typ,
        };
        let depotauszug = Depotauszug {
            datum: demo_datum(),
            depotwert: depotwert.as_referenz(),
            konto: konto.as_reference(),
            wert: zwei(),
        };
        let order = Order {
            datum: any_datum(),
            name: demo_name(),
            konto: konto.as_reference(),
            depotwert: depotwert.as_referenz(),
            wert: kauf(u_vier()),
        };
        let database = generate_database_with_sparkontos(vec![konto.clone()])
            .change_depotauszuege(Depotauszuege {
                depotauszuege: vec![indiziert(depotauszug.clone())],
            })
            .change_depotwerte(Depotwerte {
                depotwerte: vec![indiziert(depotwert.clone())],
            })
            .change_order(Orders {
                orders: vec![indiziert(order)],
            });
        let result = super::berechne_anlagetypen(&database, vec![green()]);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, expected_name);
        assert_eq!(result[0].gesamte_einzahlungen, vier());
        assert_eq!(result[0].differenz, minus_zwei());
        assert_eq!(result[0].kontostand, zwei());
        assert_eq!(result[0].farbe, green());
    }
}
