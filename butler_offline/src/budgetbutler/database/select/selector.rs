use crate::budgetbutler::database::select::functions::datatypes::MonatsAggregationsIndex;
use crate::model::primitives::datum::Datum;
use std::collections::{HashMap, HashSet};
use std::hash::Hash;
use std::ops::Add;

pub struct Selector<T> {
    pub internal_state: Vec<T>,
}

impl<T: Clone> Selector<T> {
    pub fn new(items: Vec<T>) -> Selector<T> {
        Selector {
            internal_state: items,
        }
    }

    pub fn filter(self, filter_function: impl Fn(&T) -> bool) -> Selector<T> {
        Selector {
            internal_state: self
                .internal_state
                .into_iter()
                .filter(filter_function)
                .collect(),
        }
    }

    pub fn map<NEWTYPE>(self, map_function: impl Fn(&T) -> NEWTYPE) -> Selector<NEWTYPE> {
        let mut new_state = Vec::new();
        for item in self.internal_state.iter() {
            new_state.push(map_function(item));
        }
        Selector {
            internal_state: new_state,
        }
    }

    pub fn group_by<KEYTYPE: Eq + Hash, VALUETYPE: Add<Output = VALUETYPE> + Default + Clone>(
        self,
        key_extractor: impl Fn(&T) -> KEYTYPE,
        result_collector: impl Fn(&T) -> VALUETYPE,
    ) -> HashMap<KEYTYPE, VALUETYPE> {
        let mut result: HashMap<KEYTYPE, VALUETYPE> = HashMap::new();
        for item in self.internal_state.iter() {
            let key = key_extractor(item);

            if let Some(value) = result.get(&key) {
                let new_value = value.clone() + result_collector(item);
                result.insert(key, new_value);
                continue;
            } else {
                result.insert(key, result_collector(item));
            }
        }
        result
    }

    pub fn group_as_list_by<'a, KEYTYPE: Eq + Hash>(
        self,
        key_extractor: impl Fn(&T) -> KEYTYPE,
    ) -> HashMap<KEYTYPE, Vec<T>> {
        let mut result: HashMap<KEYTYPE, Vec<T>> = HashMap::new();
        for item in self.internal_state.into_iter() {
            let key = key_extractor(&item);

            if let Some(lhs) = result.get_mut(&key) {
                lhs.push(item);
            } else {
                result.insert(key, vec![item]);
            }
        }
        result
    }

    pub fn extract_unique_values<KEYTYPE: Eq + Hash + Ord>(
        &self,
        key_extractor: impl Fn(&T) -> KEYTYPE,
    ) -> Vec<KEYTYPE> {
        let mut result_set = HashSet::<KEYTYPE>::new();
        for item in self.internal_state.iter() {
            let keytype: KEYTYPE = key_extractor(item);
            result_set.insert(keytype);
        }
        let mut result_list: Vec<KEYTYPE> = result_set.into_iter().collect();
        result_list.sort();
        result_list
    }

    pub fn collect(self) -> Vec<T> {
        self.internal_state
    }

    pub fn count(&self) -> usize {
        self.internal_state.len()
    }

    pub fn as_ref(&self) -> Selector<&T> {
        Selector {
            internal_state: self.internal_state.iter().collect(),
        }
    }

    pub fn first(&self) -> &T {
        self.internal_state.first().unwrap()
    }

    pub fn find_first(&self) -> Option<&T> {
        self.internal_state.first()
    }

    pub fn last(&self) -> Option<&T> {
        self.internal_state.last()
    }

    pub fn clone(&self) -> Selector<T> {
        Selector {
            internal_state: self.internal_state.clone(),
        }
    }
}

pub fn generate_monats_indizes(from: Datum, to: Datum) -> Vec<MonatsAggregationsIndex> {
    let mut result = Vec::new();
    let mut current = to;
    while current >= from {
        result.push(MonatsAggregationsIndex {
            monat: current.monat,
            jahr: current.jahr,
        });
        current = current.substract_months(1);
    }
    result.reverse();
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::select::functions::datatypes::MonatsAggregationsIndex;
    use crate::budgetbutler::database::select::selector::{generate_monats_indizes, Selector};
    use crate::model::database::einzelbuchung::builder::{
        demo_einzelbuchung, einzelbuchung_with_kategorie, einzelbuchung_with_kategorie_und_betrag,
    };
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::datum::Datum;

    #[test]
    fn test_selector_should_filter_negative() {
        let selector = Selector::new(vec![demo_einzelbuchung()]);

        let result = selector.filter(|_x| false);

        assert_eq!(result.count(), 0);
    }

    #[test]
    fn test_selector_should_filter_positive() {
        let selector = Selector::new(vec![demo_einzelbuchung()]);

        let result = selector.filter(|_x| true);

        assert_eq!(result.count(), 1);
    }

    #[test]
    fn test_count() {
        let selector = Selector::new(vec![demo_einzelbuchung(), demo_einzelbuchung()]);

        assert_eq!(selector.count(), 2);
    }

    #[test]
    fn test_group_by() {
        let selector = Selector::new(vec![
            einzelbuchung_with_kategorie_und_betrag("k1", zwei()),
            einzelbuchung_with_kategorie_und_betrag("k1", zwei()),
            einzelbuchung_with_kategorie_und_betrag("k2", zwei()),
        ]);

        let result = selector.group_by(|x| x.kategorie.get_kategorie().clone(), |x| x.betrag.euro);

        assert_eq!(result.len(), 2);
        assert_eq!(result.get(&"k1".to_string()), Some(&4));
        assert_eq!(result.get(&"k2".to_string()), Some(&2));
    }

    #[test]
    fn test_generate_monats_indizes() {
        let from = Datum::new(1, 12, 2019);
        let to = Datum::new(1, 3, 2020);

        let result = generate_monats_indizes(from, to);

        assert_eq!(result.len(), 4);
        assert_eq!(
            result[0],
            MonatsAggregationsIndex {
                monat: 12,
                jahr: 2019
            }
        );
        assert_eq!(
            result[1],
            MonatsAggregationsIndex {
                monat: 1,
                jahr: 2020
            }
        );
        assert_eq!(
            result[2],
            MonatsAggregationsIndex {
                monat: 2,
                jahr: 2020
            }
        );
        assert_eq!(
            result[3],
            MonatsAggregationsIndex {
                monat: 3,
                jahr: 2020
            }
        );
    }

    #[test]
    fn test_extract_unique_values() {
        let selector = Selector::new(vec![
            einzelbuchung_with_kategorie("k1"),
            einzelbuchung_with_kategorie("k1"),
            einzelbuchung_with_kategorie("k2"),
        ]);

        let result = selector.extract_unique_values(|x| x.kategorie.get_kategorie().clone());

        assert_eq!(result.len(), 2);
        assert_eq!(result[0], "k1".to_string());
        assert_eq!(result[1], "k2".to_string());
    }

    #[test]
    fn test_first() {
        let selector = Selector::new(vec![
            einzelbuchung_with_kategorie("k1"),
            einzelbuchung_with_kategorie("k2"),
        ]);

        let result = selector.first();

        assert_eq!(result.kategorie.get_kategorie(), "k1");
    }

    #[test]
    fn test_last() {
        let selector = Selector::new(vec![
            einzelbuchung_with_kategorie("k1"),
            einzelbuchung_with_kategorie("k2"),
        ]);

        let result = selector.last();

        assert_eq!(result.unwrap().kategorie.get_kategorie(), "k2");
        assert_eq!(Selector::<Einzelbuchung>::new(vec![]).last(), None);
    }
}
