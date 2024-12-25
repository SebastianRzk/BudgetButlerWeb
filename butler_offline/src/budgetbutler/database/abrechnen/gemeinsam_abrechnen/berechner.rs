use crate::budgetbutler::pages::gemeinsame_buchungen::gemeinsam_abrechnen::Limit;
use crate::model::primitives::betrag::{Betrag, Vorzeichen};
use crate::model::primitives::person::Person;
use std::cmp::{max, min};

pub fn berechne_abrechnungs_summen(
    set_verhaeltnis: u32,
    set_limit: Option<Limit>,
    self_name: Person,
    eigene_summe: Betrag,
    partner_summe: Betrag,
    gesamt_summe: &Betrag,
) -> GemeinsamAbrechnenVerhaeltnis {
    let theoretisch_eigener_anteil = Betrag::from_cent(
        Vorzeichen::Negativ,
        (gesamt_summe.as_cent() * set_verhaeltnis as u64) / 100,
    );
    let theoretischer_partner_anteil = gesamt_summe.clone() - theoretisch_eigener_anteil.clone();

    if let Some(limit) = set_limit.clone() {
        let limit_restbetrag = gesamt_summe.clone() - limit.value.clone();
        if limit.fuer == self_name {
            if limit.value < theoretisch_eigener_anteil {
                return to_ergebnis(
                    eigene_summe,
                    partner_summe,
                    theoretisch_eigener_anteil,
                    theoretischer_partner_anteil,
                    BerechnungsErgebnisModus::LimitNichtErreicht,
                );
            }
            let self_soll = max(limit.value.clone(), theoretischer_partner_anteil);
            let partner_soll = min(limit_restbetrag, theoretisch_eigener_anteil.clone());
            to_ergebnis(
                eigene_summe,
                partner_summe,
                self_soll,
                partner_soll,
                BerechnungsErgebnisModus::LimitErreicht,
            )
        } else {
            if limit.value < theoretischer_partner_anteil {
                return to_ergebnis(
                    eigene_summe,
                    partner_summe,
                    theoretisch_eigener_anteil,
                    theoretischer_partner_anteil,
                    BerechnungsErgebnisModus::LimitNichtErreicht,
                );
            }

            let self_soll = min(limit_restbetrag, theoretischer_partner_anteil.clone());
            let partner_soll = max(limit.value.clone(), theoretisch_eigener_anteil);
            to_ergebnis(
                eigene_summe,
                partner_summe,
                self_soll,
                partner_soll,
                BerechnungsErgebnisModus::LimitErreicht,
            )
        }
    } else {
        to_ergebnis(
            eigene_summe,
            partner_summe,
            theoretisch_eigener_anteil,
            theoretischer_partner_anteil,
            BerechnungsErgebnisModus::KeinLimit,
        )
    }
}

fn to_ergebnis(
    eigene_summe: Betrag,
    partner_summe: Betrag,
    eigener_anteil: Betrag,
    partner_anteil: Betrag,
    modus: BerechnungsErgebnisModus,
) -> GemeinsamAbrechnenVerhaeltnis {
    GemeinsamAbrechnenVerhaeltnis {
        partner: PersonenVerhaeltnis {
            soll: partner_anteil.clone(),
            diff: partner_anteil - partner_summe.clone(),
            ist: partner_summe,
        },
        eigenes: PersonenVerhaeltnis {
            soll: eigener_anteil.clone(),
            diff: eigener_anteil - eigene_summe.clone(),
            ist: eigene_summe,
        },
        modus,
    }
}

pub struct GemeinsamAbrechnenVerhaeltnis {
    pub eigenes: PersonenVerhaeltnis,
    pub partner: PersonenVerhaeltnis,
    pub modus: BerechnungsErgebnisModus,
}

pub struct PersonenVerhaeltnis {
    pub soll: Betrag,
    pub diff: Betrag,
    pub ist: Betrag,
}

#[derive(Debug, PartialEq)]
pub enum BerechnungsErgebnisModus {
    LimitNichtErreicht,
    LimitErreicht,
    KeinLimit,
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::berechner::berechne_abrechnungs_summen;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::person::builder::demo_person;
    use crate::model::primitives::person::Person;

    #[test]
    fn test_berechne_ohne_limit_50_50_ohne_aenderungen() {
        let result = berechne_abrechnungs_summen(
            50,
            None,
            demo_person(),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            &Betrag::new(Vorzeichen::Negativ, 200, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
        assert_eq!(result.eigenes.diff, Betrag::zero());
        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
        assert_eq!(result.partner.diff, Betrag::zero());
        assert_eq!(result.modus, super::BerechnungsErgebnisModus::KeinLimit);
    }

    #[test]
    fn test_berechne_ohne_limit_50_50_mit_aenderungen() {
        let result = berechne_abrechnungs_summen(
            50,
            None,
            demo_person(),
            Betrag::new(Vorzeichen::Negativ, 200, 0),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            &Betrag::new(Vorzeichen::Negativ, 300, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 200, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.eigenes.diff, Betrag::new(Vorzeichen::Positiv, 50, 0));
        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.partner.diff, Betrag::new(Vorzeichen::Negativ, 50, 0));
        assert_eq!(result.modus, super::BerechnungsErgebnisModus::KeinLimit);
    }

    #[test]
    fn test_berechne_mit_limit_50_50_ohne_aenderungen_limit_self_nicht_erreicht() {
        let result = berechne_abrechnungs_summen(
            50,
            Some(super::Limit {
                value: Betrag::new(Vorzeichen::Negativ, 200, 0),
                fuer: demo_person(),
            }),
            demo_person(),
            Betrag::new(Vorzeichen::Negativ, 200, 0),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            &Betrag::new(Vorzeichen::Negativ, 300, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 200, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.eigenes.diff, Betrag::new(Vorzeichen::Positiv, 50, 0));
        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.partner.diff, Betrag::new(Vorzeichen::Negativ, 50, 0));
        assert_eq!(
            result.modus,
            super::BerechnungsErgebnisModus::LimitNichtErreicht
        );
    }

    #[test]
    fn test_berechne_mit_limit_50_50_ohne_aenderungen_limit_self_erreicht() {
        let self_name = demo_person();
        let result = berechne_abrechnungs_summen(
            50,
            Some(super::Limit {
                value: Betrag::new(Vorzeichen::Negativ, 100, 0),
                fuer: self_name.clone(),
            }),
            self_name,
            Betrag::new(Vorzeichen::Negativ, 200, 0),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            &Betrag::new(Vorzeichen::Negativ, 300, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 200, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
        assert_eq!(
            result.eigenes.diff,
            Betrag::new(Vorzeichen::Positiv, 100, 0)
        );

        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 200, 0)
        );
        assert_eq!(
            result.partner.diff,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
        assert_eq!(result.modus, super::BerechnungsErgebnisModus::LimitErreicht);
    }

    #[test]
    fn test_berechne_mit_limit_50_50_ohne_aenderungen_limit_partner_nicht_erreicht() {
        let result = berechne_abrechnungs_summen(
            50,
            Some(super::Limit {
                fuer: Person::new("partner".to_string()),
                value: Betrag::new(Vorzeichen::Negativ, 200, 0),
            }),
            demo_person(),
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            Betrag::new(Vorzeichen::Negativ, 200, 0),
            &Betrag::new(Vorzeichen::Negativ, 300, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.eigenes.diff, Betrag::new(Vorzeichen::Negativ, 50, 0));
        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 200, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 150, 0)
        );
        assert_eq!(result.partner.diff, Betrag::new(Vorzeichen::Positiv, 50, 0));
        assert_eq!(
            result.modus,
            super::BerechnungsErgebnisModus::LimitNichtErreicht
        );
    }

    #[test]
    fn test_berechne_mit_limit_50_50_ohne_aenderungen_limit_partner_erreicht() {
        let self_name = demo_person();
        let result = berechne_abrechnungs_summen(
            50,
            Some(super::Limit {
                value: Betrag::new(Vorzeichen::Negativ, 100, 0),
                fuer: Person::new("partner".to_string()),
            }),
            self_name,
            Betrag::new(Vorzeichen::Negativ, 100, 0),
            Betrag::new(Vorzeichen::Negativ, 200, 0),
            &Betrag::new(Vorzeichen::Negativ, 300, 0),
        );

        assert_eq!(result.eigenes.ist, Betrag::new(Vorzeichen::Negativ, 100, 0));
        assert_eq!(
            result.eigenes.soll,
            Betrag::new(Vorzeichen::Negativ, 200, 0)
        );
        assert_eq!(
            result.eigenes.diff,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );

        assert_eq!(result.partner.ist, Betrag::new(Vorzeichen::Negativ, 200, 0));
        assert_eq!(
            result.partner.soll,
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
        assert_eq!(
            result.partner.diff,
            Betrag::new(Vorzeichen::Positiv, 100, 0)
        );
        assert_eq!(result.modus, super::BerechnungsErgebnisModus::LimitErreicht);
    }
}
