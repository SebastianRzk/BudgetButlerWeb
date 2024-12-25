use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::depotauszug::Depotauszug;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use std::collections::HashMap;

impl Selector<Indiziert<Depotauszug>> {
    pub fn get_letzter_kontostand(
        &self,
        depotwert: DepotwertReferenz,
        konto: KontoReferenz,
    ) -> Betrag {
        self.clone()
            .filter(|x| x.value.depotwert == depotwert)
            .filter(|x| x.value.konto == konto)
            .last()
            .map(|x| x.value.wert.clone())
            .unwrap_or(Betrag::zero())
    }

    pub fn lade_kontostand(
        &self,
        depotwert: DepotwertReferenz,
        konto: KontoReferenz,
        datum: Datum,
    ) -> Betrag {
        self.clone()
            .filter(|x| x.value.depotwert == depotwert)
            .filter(|x| x.value.konto == konto)
            .filter(|x| x.value.datum == datum)
            .last()
            .map(|x| x.value.wert.clone())
            .unwrap_or(Betrag::zero())
    }

    pub fn get_kombinierter_kontostand(&self) -> Betrag {
        let mut depot_map = HashMap::new();
        for auszug in self.internal_state.iter() {
            let depotwert = &auszug.value.depotwert;
            depot_map.insert(
                KontoWertIndex {
                    konto: auszug.value.konto.clone(),
                    depotwert_referenz: depotwert.clone(),
                },
                auszug.value.wert.clone(),
            );
        }
        depot_map
            .values()
            .into_iter()
            .map(|x| x.clone())
            .reduce(|a, b| a + b)
            .unwrap_or_else(Betrag::zero)
    }

    pub fn get_konto(&self, konto: KontoReferenz, datum: Datum) -> Vec<Indiziert<Depotauszug>> {
        self.clone()
            .filter(|x| x.value.konto == konto && x.value.datum == datum)
            .collect()
    }

    pub fn get_kombinierte_depotauszuege(&self) -> Vec<Depotuebersicht> {
        let mut combined: HashMap<DepotDatumIndex, Vec<DepotauszugEinzelwert>> = HashMap::new();

        for depotauszug in self.internal_state.iter() {
            let index = DepotDatumIndex {
                konto: depotauszug.value.konto.clone(),
                datum: depotauszug.value.datum.clone(),
            };
            let wert = DepotauszugEinzelwert {
                depotwert: depotauszug.value.depotwert.clone(),
                wert: depotauszug.value.wert.clone(),
            };
            let entry = combined.entry(index).or_insert(vec![]);
            entry.push(wert);
        }
        let mut element_list: Vec<&DepotDatumIndex> = combined.keys().into_iter().collect();
        element_list.sort();

        element_list
            .into_iter()
            .map(|index| {
                let einzelne_werte = combined.get(&index).unwrap();
                Depotuebersicht {
                    datum: index.datum.clone(),
                    konto: index.konto.clone(),
                    einzelne_werte: einzelne_werte.clone(),
                }
            })
            .collect()
    }

    pub fn existiert_auszug(&self, konto_referenz: KontoReferenz, datum: Datum) -> bool {
        self.clone()
            .filter(|x| x.value.konto == konto_referenz && x.value.datum == datum)
            .count()
            > 0
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
struct KontoWertIndex {
    pub konto: KontoReferenz,
    pub depotwert_referenz: DepotwertReferenz,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct DepotDatumIndex {
    pub konto: KontoReferenz,
    pub datum: Datum,
}

impl PartialOrd for DepotDatumIndex {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for DepotDatumIndex {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let datum_cmp = self.datum.cmp(&other.datum);
        if datum_cmp != std::cmp::Ordering::Equal {
            return datum_cmp;
        }

        self.konto.cmp(&other.konto)
    }
}

pub struct Depotuebersicht {
    pub datum: Datum,
    pub konto: KontoReferenz,
    pub einzelne_werte: Vec<DepotauszugEinzelwert>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DepotauszugEinzelwert {
    pub depotwert: DepotwertReferenz,
    pub wert: Betrag,
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::builder::demo_depotauszug;
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::{demo_depotwert_referenz, depotwert_referenz};
    use crate::model::database::sparbuchung::builder::{demo_konto_referenz, konto_referenz};
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::state::persistent_application_state::builder::leere_depotauszuege;
    use crate::model::state::persistent_state::depotauszuege::Depotauszuege;

    #[test]
    fn test_get_letzter_kontostand_mit_match() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![indiziert(Depotauszug {
                datum: demo_datum(),
                depotwert: demo_depotwert_referenz(),
                konto: demo_konto_referenz(),
                wert: vier(),
            })],
        };
        let result = depotauszuege
            .select()
            .get_letzter_kontostand(demo_depotwert_referenz(), demo_konto_referenz());
        assert_eq!(result, vier());
    }

    #[test]
    fn test_get_letzter_kontostand_without_match() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: depotwert_referenz("kein match"),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: konto_referenz("kein match"),
                    wert: vier(),
                }),
            ],
        };
        let result = depotauszuege
            .select()
            .get_letzter_kontostand(demo_depotwert_referenz(), demo_konto_referenz());
        assert_eq!(result, Betrag::zero());
    }

    #[test]
    fn test_get_konto() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: konto_referenz("kein match"),
                    wert: vier(),
                }),
            ],
        };
        let result = depotauszuege
            .select()
            .get_konto(demo_konto_referenz(), demo_datum());
        assert_eq!(result.len(), 2);
    }

    #[test]
    fn test_get_kombinierte_depotauszuege() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: depotwert_referenz("xanderer depotwert"),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: konto_referenz("xanderes konto"),
                    wert: vier(),
                }),
            ],
        };
        let result = depotauszuege.select().get_kombinierte_depotauszuege();
        assert_eq!(result.len(), 2);

        assert_eq!(result[0].datum, demo_datum());
        assert_eq!(result[0].konto, demo_konto_referenz());
        let werte = &result[0].einzelne_werte;
        assert_eq!(werte.len(), 2);
        assert_eq!(werte[0].depotwert, demo_depotwert_referenz());
        assert_eq!(werte[0].wert, vier());
        assert_eq!(werte[1].depotwert, depotwert_referenz("xanderer depotwert"));
        assert_eq!(werte[1].wert, vier());

        assert_eq!(result[1].datum, demo_datum());
        assert_eq!(result[1].konto, konto_referenz("xanderes konto"));
        let werte = &result[1].einzelne_werte;
        assert_eq!(werte.len(), 1);
        assert_eq!(werte[0].depotwert, demo_depotwert_referenz());
        assert_eq!(werte[0].wert, vier());
    }

    #[test]
    fn test_existiert_auszug() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![indiziert(demo_depotauszug())],
        };
        let result = depotauszuege
            .select()
            .existiert_auszug(demo_depotauszug().konto, demo_depotauszug().datum);
        assert_eq!(result, true);
    }

    #[test]
    fn test_existiert_auszug_without_match() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![indiziert(demo_depotauszug())],
        };
        let result = depotauszuege
            .select()
            .existiert_auszug(konto_referenz("kein match"), demo_depotauszug().datum);
        assert_eq!(result, false);
    }

    #[test]
    fn test_lade_kontostand() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![indiziert(demo_depotauszug())],
        };
        let result = depotauszuege.select().lade_kontostand(
            demo_depotauszug().depotwert,
            demo_depotauszug().konto,
            demo_depotauszug().datum,
        );
        assert_eq!(result, demo_depotauszug().wert);
    }

    #[test]
    fn test_get_kombinierter_kontostand() {
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: depotwert_referenz("anderer depotwert"),
                    konto: demo_konto_referenz(),
                    wert: vier(),
                }),
                indiziert(Depotauszug {
                    datum: demo_datum(),
                    depotwert: demo_depotwert_referenz(),
                    konto: konto_referenz("anderes depot"),
                    wert: zwei(),
                }),
            ],
        };
        let result = depotauszuege.select().get_kombinierter_kontostand();
        assert_eq!(result, vier() + vier() + zwei());
    }

    #[test]
    fn test_get_kombinierter_kontostand_leer() {
        let depotauszuege = leere_depotauszuege();
        let result = depotauszuege.select().get_kombinierter_kontostand();
        assert_eq!(result, Betrag::zero());
    }
}
