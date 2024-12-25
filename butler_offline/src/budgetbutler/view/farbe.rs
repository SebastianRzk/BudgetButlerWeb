use crate::model::primitives::farbe::{ausgaben_farbe, einnahmen_farbe, Farbe};
use crate::model::primitives::kategorie::Kategorie;
use std::collections::HashMap;

pub struct FarbenSelektor {
    map: HashMap<Kategorie, Farbe>,
}

impl FarbenSelektor {
    pub fn new(kategorien: Vec<Kategorie>, konfigurierte_farben: Vec<Farbe>) -> FarbenSelektor {
        let mut map = HashMap::new();
        let mut index = 0;
        let farben_count = konfigurierte_farben.len();

        for kategorie in kategorien {
            let farben_index = index % farben_count;
            let farbe = konfigurierte_farben.get(farben_index).unwrap();
            map.insert(kategorie.clone(), farbe.clone());
            index += 1;
        }
        FarbenSelektor { map }
    }

    pub fn get(&self, kategorie: &Kategorie) -> Farbe {
        self.map.get(kategorie).unwrap().clone()
    }
}

pub struct EinnahmenAusgabenFarbenSelektor {}

impl EinnahmenAusgabenFarbenSelektor {
    pub fn get_einnahmen(&self) -> Farbe {
        einnahmen_farbe()
    }

    pub fn get_ausgaben(&self) -> Farbe {
        ausgaben_farbe()
    }
}

pub struct RandomFarbenSelektor {
    internal_farben: Vec<Farbe>,
}

impl RandomFarbenSelektor {
    pub fn new(farben: Vec<Farbe>) -> RandomFarbenSelektor {
        RandomFarbenSelektor {
            internal_farben: farben,
        }
    }

    pub fn get_farben_liste(&self, size: usize) -> Vec<Farbe> {
        let mut result = vec![];
        let mut index = 0;
        for _ in 0..size {
            let farben_index = index % self.internal_farben.len();
            let farbe = self.internal_farben.get(farben_index).unwrap();
            result.push(farbe.clone());
            index += 1;
        }
        result
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::view::farbe::FarbenSelektor;
    use crate::model::primitives::farbe::builder::farbe;
    use crate::model::primitives::kategorie::kategorie;

    #[test]
    pub fn test_with_kategorie_index_in_farben_range() {
        let selektor = FarbenSelektor::new(
            vec![kategorie("K1"), kategorie("K2")],
            vec![farbe("F1"), farbe("F2")],
        );

        assert_eq!(selektor.get(&kategorie("K1")), farbe("F1"));
        assert_eq!(selektor.get(&kategorie("K2")), farbe("F2"));
    }

    #[test]
    pub fn test_with_kategorie_index_in_farben_out_of_range() {
        let selektor = FarbenSelektor::new(
            vec![kategorie("K1"), kategorie("K2"), kategorie("K3")],
            vec![farbe("F1"), farbe("F2")],
        );

        assert_eq!(selektor.get(&kategorie("K3")), farbe("F1"));
    }
}
