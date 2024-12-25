use crate::budgetbutler::database::select::selector::Selector;
use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;

impl<'a, T: BesitztBetrag<'a> + Ord + PartialOrd + PartialEq + Eq> Selector<Indiziert<T>> {
    pub fn summe(&'a self) -> Betrag {
        self.internal_state
            .iter()
            .map(|x| x.value.betrag().clone())
            .fold(Betrag::zero(), |acc, x| acc + x)
    }
}

impl<'a, T: BesitztBetrag<'a> + Ord + PartialOrd + PartialEq + Eq> Selector<T> {
    pub fn bilde_summe(&'a self) -> Betrag {
        self.internal_state
            .iter()
            .map(|x| x.betrag().clone())
            .fold(Betrag::zero(), |acc, x| acc + x)
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::select::selector::Selector;
    use crate::model::database::einzelbuchung::builder::demo_einzelbuchung;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::state::persistent_application_state::builder::leere_einzelbuchungen;
    use crate::model::state::persistent_state::einzelbuchungen::Einzelbuchungen;

    #[test]
    fn test_sum() {
        let einzelbuchungen = Einzelbuchungen {
            einzelbuchungen: vec![indiziert(demo_einzelbuchung())],
        };

        let result = einzelbuchungen.select().bilde_summe();

        assert_eq!(result, demo_einzelbuchung().betrag);
    }
    #[test]
    fn test_sum_leer() {
        let einzelbuchungen = leere_einzelbuchungen();

        let result = einzelbuchungen.select().bilde_summe();

        assert_eq!(result, Betrag::zero());
    }

    #[test]
    fn test_sum_on_betrag() {
        let selector = Selector::new(vec![zwei(), vier()]);
        assert_eq!(
            selector.bilde_summe(),
            Betrag::from_user_input(&"6,00".to_string())
        );
    }
}
