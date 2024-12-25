use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;

pub fn sum_einzelbuchungen(selector: Selector<Indiziert<Einzelbuchung>>) -> Betrag {
    let mut result = Betrag::zero();
    for einzelbuchung in &selector.internal_state {
        result = result + einzelbuchung.value.betrag().clone();
    }
    result
}

pub fn sum_gemeinsame_buchungen(selector: Selector<Indiziert<GemeinsameBuchung>>) -> Betrag {
    let mut result = Betrag::zero();
    for einzelbuchung in &selector.internal_state {
        result = result + einzelbuchung.value.betrag().clone();
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::select::functions::sum_by::{
        sum_einzelbuchungen, sum_gemeinsame_buchungen,
    };
    use crate::budgetbutler::database::select::selector::Selector;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_betrag;
    use crate::model::database::gemeinsame_buchung::builder::gemeinsame_buchung_mit_betrag;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::Betrag;

    #[test]
    fn test_sum_should_sum_all() {
        let selector = Selector::new(vec![
            indiziert(einzelbuchung_with_betrag(zwei())),
            indiziert(einzelbuchung_with_betrag(zwei())),
        ]);

        let result = sum_einzelbuchungen(selector);

        assert_eq!(result, vier());
    }

    #[test]
    fn test_sum_should_sum_none() {
        let selector = Selector::new(vec![]);

        let result = sum_einzelbuchungen(selector);

        assert_eq!(result, Betrag::zero());
    }

    #[test]
    fn test_sum_should_sum_gemeinsame_buchungen_none() {
        let selector = Selector::new(vec![]);

        let result = sum_gemeinsame_buchungen(selector);

        assert_eq!(result, Betrag::zero());
    }

    #[test]
    fn test_sum_should_sum_gemeinsame_buchungen_all() {
        let selector = Selector::new(vec![
            indiziert(gemeinsame_buchung_mit_betrag(zwei())),
            indiziert(gemeinsame_buchung_mit_betrag(zwei())),
        ]);

        let result = sum_gemeinsame_buchungen(selector);

        assert_eq!(result, vier());
    }
}
