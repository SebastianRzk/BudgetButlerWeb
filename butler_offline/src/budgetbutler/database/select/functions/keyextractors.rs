use crate::budgetbutler::database::select::functions::datatypes::{
    JahresAggregationsIndex, MonatsAggregationsIndex, TagesAggregationsIndex,
};
use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::eigenschaften::besitzt_datum::BesitztDatum;
use crate::model::eigenschaften::besitzt_kategorie::BesitztKategorie;
use crate::model::eigenschaften::besitzt_start_und_ende_datum::BesitztStartUndEndeDatum;
use crate::model::primitives::betrag::Vorzeichen;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use std::hash::Hash;

pub fn monatsweise_aggregation<T: for<'a> BesitztDatum<'a>>(item: &T) -> MonatsAggregationsIndex {
    MonatsAggregationsIndex {
        monat: item.datum().monat,
        jahr: item.datum().jahr,
    }
}

pub fn jahresweise_aggregation<T: for<'a> BesitztDatum<'a>>(item: &T) -> JahresAggregationsIndex {
    JahresAggregationsIndex {
        jahr: item.datum().jahr,
    }
}

pub fn tagesweise_aggregation<T: for<'a> BesitztDatum<'a>>(item: &T) -> TagesAggregationsIndex {
    TagesAggregationsIndex {
        tag: item.datum().tag,
    }
}

pub fn kategorie_aggregation<T: for<'a> BesitztKategorie<'a>>(item: &T) -> Kategorie {
    item.kategorie().clone()
}

pub fn start_ende_aggregation<T: for<'a> BesitztStartUndEndeDatum<'a>>(
    heute: Datum,
) -> impl Fn(&T) -> StartEndeAggregation {
    move |item: &T| {
        if item.ende_datum() < &heute {
            StartEndeAggregation::Vergangene
        } else if item.start_datum() < &heute && item.ende_datum() > &heute {
            StartEndeAggregation::Aktuelle
        } else {
            StartEndeAggregation::Zukuenftige
        }
    }
}

pub fn einnahmen_ausgaben_aggregation<T: for<'a> BesitztBetrag<'a>>(item: &T) -> Vorzeichen {
    item.betrag().vorzeichen.clone()
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum StartEndeAggregation {
    Vergangene,
    Aktuelle,
    Zukuenftige,
}

#[cfg(test)]
mod tests {
    use crate::model::database::dauerauftrag::builder::dauerauftrag_mit_start_ende_datum;
    use crate::model::database::einzelbuchung::builder::einzelbuchung_with_datum;
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::datum::Datum;

    #[test]
    pub fn test_start_ende_aggregation() {
        let heute = Datum::new(1, 1, 2021);
        let vergangener_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2020), Datum::new(31, 12, 2020));
        let aktueller_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2020), Datum::new(31, 12, 2024));
        let zukuenftiger_dauerauftrag =
            dauerauftrag_mit_start_ende_datum(Datum::new(1, 1, 2024), Datum::new(31, 12, 2024));

        assert_eq!(
            super::start_ende_aggregation(heute.clone())(&indiziert(vergangener_dauerauftrag)),
            super::StartEndeAggregation::Vergangene
        );
        assert_eq!(
            super::start_ende_aggregation(heute.clone())(&indiziert(aktueller_dauerauftrag)),
            super::StartEndeAggregation::Aktuelle
        );
        assert_eq!(
            super::start_ende_aggregation(heute)(&indiziert(zukuenftiger_dauerauftrag)),
            super::StartEndeAggregation::Zukuenftige
        );
    }

    #[test]
    pub fn test_tagesweise_aggregation() {
        let heute = Datum::new(1, 1, 2021);
        let dauerauftrag = einzelbuchung_with_datum(heute.clone());

        assert_eq!(
            super::tagesweise_aggregation(&indiziert(dauerauftrag)),
            super::TagesAggregationsIndex { tag: 1 }
        );
    }
}
