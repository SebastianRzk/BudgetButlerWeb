use crate::budgetbutler::database::select::functions::datatypes::{
    EinnahmenAusgabenAggregation, KategorieAggregation,
};
use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::eigenschaften::besitzt_kategorie::BesitztKategorie;
use crate::model::primitives::betrag::{Betrag, Vorzeichen};

pub fn einnahmen_ausgaben_gruppierung<T: for<'a> BesitztBetrag<'a>>(
    item: &T,
) -> EinnahmenAusgabenAggregation {
    if item.betrag().vorzeichen == Vorzeichen::Positiv {
        EinnahmenAusgabenAggregation {
            einnahmen: item.betrag().clone(),
            ausgaben: Betrag::new(Vorzeichen::Negativ, 0, 0),
        }
    } else {
        EinnahmenAusgabenAggregation {
            einnahmen: Betrag::new(Vorzeichen::Positiv, 0, 0),
            ausgaben: item.betrag().clone(),
        }
    }
}

pub fn betrag_summe_gruppierung<T: for<'a> BesitztBetrag<'a>>(item: &T) -> Betrag {
    item.betrag().clone()
}

pub fn kategorie_gruppierung<T: for<'a> BesitztBetrag<'a> + for<'a> BesitztKategorie<'a>>(
    item: &T,
) -> KategorieAggregation {
    let mut map = std::collections::HashMap::new();
    map.insert(item.kategorie().clone(), item.betrag().clone());
    KategorieAggregation { content: map }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::select::functions::datatypes::{
        EinnahmenAusgabenAggregation, MonatsAggregationsIndex,
    };
    use crate::budgetbutler::database::select::functions::grouper::einnahmen_ausgaben_gruppierung;
    use crate::budgetbutler::database::select::functions::keyextractors::monatsweise_aggregation;
    use crate::budgetbutler::database::select::selector::Selector;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_datum_und_betrag;
    use crate::model::primitives::betrag::builder::{n_zero, vier, zwei};
    use crate::model::primitives::datum::Datum;

    #[test]
    fn test_group_monatsweise_by_einnahmen_ausgaben() {
        let selector = Selector::new(vec![
            einzelbuchung_with_datum_und_betrag(Datum::new(1, 1, 2020), zwei()),
            einzelbuchung_with_datum_und_betrag(Datum::new(1, 1, 2020), zwei()),
            einzelbuchung_with_datum_und_betrag(Datum::new(1, 2, 2020), zwei()),
        ]);

        let result = selector.group_by(monatsweise_aggregation, einnahmen_ausgaben_gruppierung);

        assert_eq!(result.len(), 2);
        assert_eq!(
            result.get(&MonatsAggregationsIndex {
                monat: 1,
                jahr: 2020
            }),
            Some(&EinnahmenAusgabenAggregation {
                einnahmen: vier(),
                ausgaben: n_zero(),
            })
        );
        assert_eq!(
            result.get(&MonatsAggregationsIndex {
                monat: 2,
                jahr: 2020
            }),
            Some(&EinnahmenAusgabenAggregation {
                einnahmen: zwei(),
                ausgaben: n_zero(),
            })
        );
    }
}
