use crate::budgetbutler::database::change::change::ChangeSelector;
use crate::model::database::depotauszug::Depotauszug;
use crate::model::indiziert::Indiziert;
use crate::model::state::persistent_state::depotauszuege::Depotauszuege;

impl ChangeSelector<Depotauszug, Depotauszuege> {
    pub fn update_auszug(&self, depotauszug: Depotauszug) -> Depotauszuege {
        let neue_auszuege = self
            .content
            .iter()
            .map(|x| {
                if x.value.depotwert == depotauszug.depotwert
                    && x.value.konto == depotauszug.konto
                    && x.value.datum == depotauszug.datum
                {
                    Indiziert {
                        value: depotauszug.clone(),
                        dynamisch: x.dynamisch,
                        index: x.index,
                    }
                } else {
                    x.clone()
                }
            })
            .collect();
        Depotauszuege {
            depotauszuege: neue_auszuege,
        }
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::{demo_depotwert_referenz, depotwert_referenz};
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::state::persistent_state::depotauszuege::Depotauszuege;

    #[test]
    fn should_update_auszug_with_matching_auszug_should_update_all() {
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
            ],
        };
        let result = depotauszuege.change().update_auszug(Depotauszug {
            datum: demo_datum(),
            depotwert: demo_depotwert_referenz(),
            konto: demo_konto_referenz(),
            wert: zwei(),
        });

        assert_eq!(
            result.depotauszuege[0].value,
            Depotauszug {
                datum: demo_datum(),
                depotwert: demo_depotwert_referenz(),
                konto: demo_konto_referenz(),
                wert: zwei(),
            }
        );
        assert_eq!(
            result.depotauszuege[1].value,
            Depotauszug {
                datum: demo_datum(),
                depotwert: demo_depotwert_referenz(),
                konto: demo_konto_referenz(),
                wert: zwei(),
            }
        );
    }

    #[test]
    fn should_update_auszug_with_non_matching_auszug_should_not_update() {
        let erster_auszug = Depotauszug {
            datum: Datum::first(),
            depotwert: demo_depotwert_referenz(),
            konto: demo_konto_referenz(),
            wert: vier(),
        };
        let zweiter_auszug = Depotauszug {
            datum: demo_datum(),
            depotwert: depotwert_referenz("non matching"),
            konto: demo_konto_referenz(),
            wert: vier(),
        };
        let depotauszuege = Depotauszuege {
            depotauszuege: vec![
                indiziert(erster_auszug.clone()),
                indiziert(zweiter_auszug.clone()),
            ],
        };
        let result = depotauszuege.change().update_auszug(Depotauszug {
            datum: demo_datum(),
            depotwert: demo_depotwert_referenz(),
            konto: demo_konto_referenz(),
            wert: zwei(),
        });

        assert_eq!(result.depotauszuege[0].value, erster_auszug);
        assert_eq!(result.depotauszuege[1].value, zweiter_auszug);
    }
}
