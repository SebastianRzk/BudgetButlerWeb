use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::BuchungenText;
use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::BUCHUNGEN_GEMEINSAM_HEADER;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::gemeinsame_buchung::GemeinsameBuchung;

pub fn gemeinsame_buchung_as_import_text(buchungen: &Vec<GemeinsameBuchung>) -> BuchungenText {
    let mut result = vec![BUCHUNGEN_GEMEINSAM_HEADER.to_string()];
    for buchung in buchungen {
        result.push(format!(
            "{},{},{},{},{}",
            buchung.datum.to_iso_string(),
            buchung.kategorie.get_kategorie(),
            Element::create_escaped(buchung.name.get_name().clone()).element,
            buchung.betrag.to_iso_string(),
            buchung.person.person
        ));
    }
    BuchungenText {
        text: result.join("\n"),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::gemeinsame_buchungen_text_generator::gemeinsame_buchung_as_import_text;
    use crate::model::database::gemeinsame_buchung::builder::demo_gemeinsame_buchung;

    #[test]
    fn test_gemeinsame_buchungen_as_import_text() {
        let result = gemeinsame_buchung_as_import_text(&vec![demo_gemeinsame_buchung()]);

        assert_eq!(
            result.text,
            "Datum,Kategorie,Name,Betrag,Person\n2020-01-01,Test,Test,10.10,Test_User"
        );
    }
}
