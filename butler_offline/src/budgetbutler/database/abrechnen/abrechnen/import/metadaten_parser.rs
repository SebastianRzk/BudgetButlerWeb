use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{ziel_from_str, Metadaten};
use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::{SortedAbrechnungsFile, METADATEN_ABRECHNENDE_PERSON_KEY, METADATEN_ABRECHNUNGSDATUM_KEY, METADATEN_AUSFUEHRUNGSDATUM_KEY, METADATEN_TITEL_KEY, METADATEN_ZIEL_KEY};
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Titel;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;

pub fn parse_metadaten(abrechnung: &SortedAbrechnungsFile) -> Metadaten {
    let metadaten_lines = &abrechnung.metadaten;
    let abrechnungsdatum = metadaten_lines[0]
        .line
        .strip_prefix(METADATEN_ABRECHNUNGSDATUM_KEY)
        .unwrap();
    let abrechnende_person_str = metadaten_lines[1]
        .line
        .strip_prefix(METADATEN_ABRECHNENDE_PERSON_KEY)
        .unwrap();
    let titel_str = metadaten_lines[2]
        .line
        .strip_prefix(METADATEN_TITEL_KEY)
        .unwrap();
    let ziel_str = metadaten_lines[3]
        .line
        .strip_prefix(METADATEN_ZIEL_KEY)
        .unwrap();
    let ausfuehrungsdatum_str = metadaten_lines[4]
        .line
        .strip_prefix(METADATEN_AUSFUEHRUNGSDATUM_KEY)
        .unwrap();

    Metadaten {
        ausfuehrungsdatum: Datum::from_iso_string(&ausfuehrungsdatum_str.trim().to_string()),
        abrechnende_person: Person::new(abrechnende_person_str.to_string()),
        titel: Titel {
            titel: titel_str.to_string(),
        },
        ziel: ziel_from_str(ziel_str.to_string()),
        abrechnungsdatum: Datum::from_iso_string(&abrechnungsdatum.trim().to_string()),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{Metadaten, Ziel};
    use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::SortedAbrechnungsFile;
    use crate::budgetbutler::database::abrechnen::abrechnen::import::metadaten_parser::parse_metadaten;
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Titel;
    use crate::io::disk::diskrepresentation::line::builder::line;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_parse_metadaten() {
        let metadaten_lines = vec![
            line("Abrechnungsdatum:2022-01-01"),
            line("Abrechnende Person:Max Mustermann"),
            line("Titel:Test"),
            line("Ziel:ImportBuchungenAusApp"),
            line("Ausfuehrungsdatum:2021-01-01"),
        ];
        let sorted_abrechnungs_file = SortedAbrechnungsFile {
            beschreibung: vec![],
            metadaten: metadaten_lines,
            einzel_buchungen: vec![],
            gemeinsame_buchungen: vec![],
        };
        let expected_metadaten = Metadaten {
            ausfuehrungsdatum: Datum::from_iso_string(&"2021-01-01".to_string()),
            abrechnende_person: person("Max Mustermann"),
            titel: Titel {
                titel: "Test".to_string(),
            },
            ziel: Ziel::ImportBuchungenAusApp,
            abrechnungsdatum: Datum::from_iso_string(&"2022-01-01".to_string()),
        };
        assert_eq!(
            parse_metadaten(&sorted_abrechnungs_file),
            expected_metadaten
        );
    }
}
