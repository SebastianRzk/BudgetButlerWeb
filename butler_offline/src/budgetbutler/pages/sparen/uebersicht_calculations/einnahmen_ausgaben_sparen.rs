use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_ausgaben, filter_auf_das_jahr, filter_auf_einnahmen, filter_auf_sparen,
    filter_drop_sparen,
};
use crate::model::metamodel::jahr_range::JahrRange;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;

#[derive(Clone, PartialEq, Eq, Debug)]
pub struct EinnahmenAusgabenSparen {
    pub einnahmen: Betrag,
    pub ausgaben: Betrag,
    pub sparen: Betrag,
    pub jahr: i32,
}

pub fn berechne_einnahmen_ausgaben_sparen(
    datum_range: &JahrRange,
    database: &Database,
) -> Vec<EinnahmenAusgabenSparen> {
    let mut result = vec![];

    let mut i = datum_range.start_jahr;
    while i <= datum_range.ende_jahr {
        let selector_jahr = database
            .einzelbuchungen
            .select()
            .filter(filter_auf_das_jahr(i));
        let einnahmen = selector_jahr
            .clone()
            .filter(filter_auf_einnahmen)
            .filter(filter_drop_sparen)
            .bilde_summe();
        let ausgaben = selector_jahr
            .clone()
            .filter(filter_auf_ausgaben)
            .filter(filter_drop_sparen)
            .bilde_summe();
        let sparen = selector_jahr.filter(filter_auf_sparen).bilde_summe();

        result.push(EinnahmenAusgabenSparen {
            einnahmen,
            ausgaben,
            sparen,
            jahr: i,
        });
        i += 1;
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::pages::sparen::uebersicht_calculations::einnahmen_ausgaben_sparen::berechne_einnahmen_ausgaben_sparen;
    use crate::model::database::einzelbuchung::builder::{
        einzelbuchung_with_datum_und_betrag, sparbuchung_with_datum_und_betrag,
    };
    use crate::model::metamodel::jahr_range::JahrRange;
    use crate::model::primitives::betrag::builder::{fuenf, minus_zwei, vier};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_einzelbuchungen, generate_empty_database,
    };

    #[test]
    fn test_berechne_einnahmen_ausgaben_sparen_mit_leerer_db() {
        let result = berechne_einnahmen_ausgaben_sparen(
            &JahrRange::new(2020, 2020),
            &generate_empty_database(),
        );

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].jahr, 2020);
        assert_eq!(result[0].einnahmen, Betrag::zero());
        assert_eq!(result[0].ausgaben, Betrag::zero());
        assert_eq!(result[0].sparen, Betrag::zero());
    }

    #[test]
    fn test_berechne_einnahmen_ausgaben_sparen() {
        let demo_jahr = demo_datum().jahr;
        let result = berechne_einnahmen_ausgaben_sparen(
            &JahrRange::new(demo_jahr, demo_jahr),
            &generate_database_with_einzelbuchungen(vec![
                einzelbuchung_with_datum_und_betrag(demo_datum(), vier()),
                einzelbuchung_with_datum_und_betrag(demo_datum(), minus_zwei()),
                sparbuchung_with_datum_und_betrag(demo_datum(), fuenf()),
            ]),
        );

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].jahr, demo_jahr);
        assert_eq!(result[0].einnahmen, vier());
        assert_eq!(result[0].ausgaben, minus_zwei());
        assert_eq!(result[0].sparen, fuenf());
    }
}
