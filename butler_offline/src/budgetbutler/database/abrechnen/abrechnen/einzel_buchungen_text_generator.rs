use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::BuchungenText;
use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::{
    BUCHUNGEN_EINZEL_HEADER, BUCHUNGEN_GEMEINSAM_HEADER,
};
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;

pub fn einzelbuchungen_as_import_text(buchungen: &Vec<Einzelbuchung>) -> BuchungenText {
    let mut result = vec![BUCHUNGEN_EINZEL_HEADER.to_string()];
    for buchung in buchungen {
        result.push(format!(
            "{},{},{},{}",
            buchung.datum.to_iso_string(),
            buchung.kategorie.get_kategorie(),
            Element::create_escaped(buchung.name.get_name().clone()).element,
            buchung.betrag.to_iso_string()
        ));
    }
    BuchungenText {
        text: result.join("\n"),
    }
}
pub fn gemeinsame_buchungen_as_import_text(buchungen: &Vec<GemeinsameBuchung>) -> BuchungenText {
    let mut result = vec![BUCHUNGEN_GEMEINSAM_HEADER.to_string()];
    for buchung in buchungen {
        result.push(format!(
            "{},{},{},{},{}",
            buchung.datum.to_iso_string(),
            buchung.kategorie.get_kategorie(),
            Element::create_escaped(buchung.name.get_name().clone()).element,
            buchung.betrag.to_iso_string(),
            Element::create_escaped(buchung.person.person.clone()).element
        ));
    }
    BuchungenText {
        text: result.join("\n"),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::einzel_buchungen_text_generator::{
        einzelbuchungen_as_import_text, gemeinsame_buchungen_as_import_text,
    };
    use crate::model::database::einzelbuchung::Einzelbuchung;
    use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;
    use crate::model::primitives::betrag::builder::minus_zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;
    use crate::model::primitives::name::name;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_einzelbuchungen_as_import_text() {
        let result = einzelbuchungen_as_import_text(&vec![Einzelbuchung {
            datum: Datum::new(1, 1, 2020),
            name: name("testname"),
            kategorie: kategorie("testkategorie"),
            betrag: minus_zwei(),
        }]);

        assert_eq!(
            result.text,
            "Datum,Kategorie,Name,Betrag\n2020-01-01,testkategorie,testname,-2.00"
        );
    }

    #[test]
    fn test_gemeinsame_buchungen_as_import_text() {
        let result = gemeinsame_buchungen_as_import_text(&vec![GemeinsameBuchung {
            datum: Datum::new(1, 1, 2020),
            name: name("testname"),
            kategorie: kategorie("testkategorie"),
            betrag: minus_zwei(),
            person: person("testperson"),
        }]);

        assert_eq!(
            result.text,
            "Datum,Kategorie,Name,Betrag,Person\n2020-01-01,testkategorie,testname,-2.00,testperson"
        );
    }
}
