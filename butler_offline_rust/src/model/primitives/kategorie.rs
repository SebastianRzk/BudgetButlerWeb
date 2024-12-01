#[derive(Debug, Clone, PartialEq, Hash, Eq)]
pub struct Kategorie {
    pub kategorie: String,
}

impl Kategorie {
    pub fn new(kategorie: String) -> Kategorie {
        Kategorie { kategorie }
    }

    pub fn get_kategorie(&self) -> &String {
        &self.kategorie
    }

    pub fn equals(&self, other: &Kategorie) -> bool {
        self.kategorie == other.kategorie
    }

    pub fn to_string(&self) -> String {
        self.kategorie.clone()
    }

    pub fn empty() -> Kategorie {
        Kategorie::new("".to_string())
    }
}

impl PartialOrd for Kategorie {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Kategorie {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.kategorie.to_lowercase().cmp(&other.kategorie.to_lowercase())
    }
}

//#[cfg(test)]
//TODO: Enable only for testing
pub fn kategorie(kategorie: &str) -> Kategorie {
    Kategorie::new(kategorie.to_string())
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::kategorie::{kategorie, Kategorie};

    pub fn any_kategorie() -> Kategorie {
        kategorie("Test")
    }
}

#[cfg(test)]
mod tests {
    use crate::model::primitives::kategorie::kategorie;

    #[test]
    fn kategorie_should_sort(){
        let mut liste = vec![
            kategorie("B"),
            kategorie("A"),
            kategorie("C"),
        ];
        liste.sort();

        assert_eq!(liste[0].get_kategorie(), "A");
        assert_eq!(liste[1].get_kategorie(), "B");
        assert_eq!(liste[2].get_kategorie(), "C");
    }
}