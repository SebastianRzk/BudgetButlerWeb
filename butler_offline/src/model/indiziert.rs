use std::cmp::Ordering;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Indiziert<T: PartialEq + Eq + Ord + PartialOrd> {
    pub index: u32,
    pub dynamisch: bool,
    pub value: T,
}

impl<T: Eq + PartialOrd + Ord> PartialOrd for Indiziert<T> {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.value.partial_cmp(&other.value).unwrap())
    }
}

impl<T: Eq + Ord> Ord for Indiziert<T> {
    fn cmp(&self, other: &Self) -> Ordering {
        self.value.cmp(&other.value)
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::indiziert::Indiziert;

    pub fn indiziert<T: PartialEq + Eq + Ord + PartialOrd>(value: T) -> Indiziert<T> {
        Indiziert {
            index: 0,
            dynamisch: false,
            value,
        }
    }

    pub fn dynamisch_indiziert<T: PartialEq + Eq + Ord + PartialOrd>(value: T) -> Indiziert<T> {
        Indiziert {
            index: 0,
            dynamisch: true,
            value,
        }
    }
}
