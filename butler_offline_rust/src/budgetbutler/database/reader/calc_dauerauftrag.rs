use crate::budgetbutler::database::reader::rhythmus::get_monatsdelta_for_rhythmus;
use crate::model::dauerauftrag::Dauerauftrag;
use crate::model::einzelbuchung::Einzelbuchung;
use crate::model::primitives::datum::Datum;
use std::cmp::min;

pub fn calc_dauerauftrag(dauerauftrag: &Dauerauftrag, heute: Datum) -> Vec<Einzelbuchung> {
    let mut lauf_datum = dauerauftrag.start_datum.clone();
    let ende_datum = min(dauerauftrag.ende_datum.clone(), heute);
    let mut buchungen: Vec<Einzelbuchung> = Vec::new();
    while lauf_datum < ende_datum {
        let einzelbuchung = Einzelbuchung {
            datum: lauf_datum.clone(),
            name: dauerauftrag.name.clone(),
            kategorie: dauerauftrag.kategorie.clone(),
            betrag: dauerauftrag.betrag.clone(),
        };
        buchungen.push(einzelbuchung);

        lauf_datum = lauf_datum.add_months(get_monatsdelta_for_rhythmus(dauerauftrag.rhythmus));
    }
    buchungen
}


#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::rhythmus::Rhythmus;

    #[test]
    fn test_calc_dauerauftrag_monatlich() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 4, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Monatlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 3);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
        assert_eq!(result[1].datum, Datum::new(1, 2, 2020));
        assert_eq!(result[2].datum, Datum::new(1, 3, 2020));
    }

    #[test]
    fn test_calc_dauerauftrag_vierteljährlich() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 7, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Vierteljaehrlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2024));

        assert_eq!(result.len(), 2);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
        assert_eq!(result[1].datum, Datum::new(1, 4, 2020));
    }


    #[test]
    fn test_calc_dauerauftrag_should_end_heute_when_endedatum_nach_heute() {
        let dauerauftrag = Dauerauftrag {
            start_datum: Datum::new(1, 1, 2020),
            ende_datum: Datum::new(1, 7, 2020),
            name: name("Normal"),
            kategorie: kategorie("NeueKategorie"),
            betrag: Betrag::new(Vorzeichen::Negativ, 123, 12),
            rhythmus: Rhythmus::Jaehrlich,
        };

        let result = calc_dauerauftrag(&dauerauftrag, Datum::new(1, 3, 2020));

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].datum, Datum::new(1, 1, 2020));
    }
}