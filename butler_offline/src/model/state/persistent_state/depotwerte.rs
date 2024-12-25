use crate::budgetbutler::database::change::change::{ChangeSelector, Creates};
use crate::budgetbutler::database::select::selector::Selector;
use crate::model::database::depotwert::Depotwert;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::isin::ISIN;

#[derive(Debug, PartialEq, Eq, Clone)]
pub struct Depotwerte {
    pub depotwerte: Vec<Indiziert<Depotwert>>,
}

impl Creates<Depotwert, Depotwerte> for Depotwerte {
    fn create(item: Vec<Indiziert<Depotwert>>) -> Depotwerte {
        Depotwerte { depotwerte: item }
    }
}

impl Depotwerte {
    pub fn select(&self) -> Selector<Indiziert<Depotwert>> {
        Selector::new(self.depotwerte.clone())
    }

    pub fn sort(&self) -> Depotwerte {
        let mut neue_depotwerte = self.depotwerte.clone();
        neue_depotwerte.sort();

        Depotwerte {
            depotwerte: neue_depotwerte,
        }
    }

    pub fn get(&self, index: u32) -> Indiziert<Depotwert> {
        self.select().filter(|x| x.index == index).first().clone()
    }

    pub fn change(&self) -> ChangeSelector<Depotwert, Depotwerte> {
        ChangeSelector {
            content: self.depotwerte.clone(),
            output: None,
        }
    }

    pub fn isin_bereits_vorhanden(&self, isin: ISIN) -> bool {
        self.select()
            .filter(|x| x.value.isin.isin == isin.isin)
            .count()
            > 0
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::isin::ISIN;

    #[test]
    fn test_depotwerte_isin_bereits_erfasst() {
        let depotwerte = super::Depotwerte {
            depotwerte: vec![indiziert(any_depotwert())],
        };

        assert!(depotwerte.isin_bereits_vorhanden(any_depotwert().isin));
        assert!(!depotwerte.isin_bereits_vorhanden(ISIN::new("iasudghasdipfb".to_string())));
    }
}
