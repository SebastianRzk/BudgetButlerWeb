use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::Metadaten;
use crate::budgetbutler::database::abrechnen::abrechnen::import::abrechnungen_sorter::{
    sort_abrechnungs_file, HeaderModus,
};
use crate::budgetbutler::database::abrechnen::abrechnen::import::metadaten_parser::parse_metadaten;
use crate::io::disk::diskrepresentation::line::Line;

pub struct UnparsedAbrechnungsFile {
    pub file_content: Vec<Line>,
    pub file_name: String,
}

pub struct PreparedAbrechnung {
    pub file_content: Vec<Line>,
    pub file_name_original: String,
    pub abrechnung_title: String,
}

pub fn read_and_sort_abrechnungen(
    unparsed_abrechnungen: Vec<UnparsedAbrechnungsFile>,
) -> Vec<PreparedAbrechnung> {
    let mut parsed_abrechnungen: Vec<PreparedAbrechnung> = unparsed_abrechnungen
        .into_iter()
        .map(|unparsed_abrechnung| read_abrechnung(unparsed_abrechnung))
        .collect();
    parsed_abrechnungen.sort_by(|a, b| a.file_name_original.cmp(&b.file_name_original));
    parsed_abrechnungen
}

fn read_abrechnung(unparsed_abrechnungs_file: UnparsedAbrechnungsFile) -> PreparedAbrechnung {
    let sorted = sort_abrechnungs_file(
        &unparsed_abrechnungs_file.file_content,
        HeaderModus::Preserve,
    );
    let title: String;
    if sorted.metadaten.len() == 0 {
        title = unparsed_abrechnungs_file.file_name.clone();
    } else {
        let metadaten = parse_metadaten(&sorted);
        title = generate_abrechnungs_title_from_metadaten(metadaten);
    }
    PreparedAbrechnung {
        file_name_original: unparsed_abrechnungs_file.file_name.clone(),
        file_content: unparsed_abrechnungs_file.file_content,
        abrechnung_title: title,
    }
}

fn generate_abrechnungs_title_from_metadaten(metadaten: Metadaten) -> String {
    format!(
        "{} vom {}, (importiert am {})",
        metadaten.titel.titel,
        metadaten.abrechnungsdatum.to_german_string(),
        metadaten.ausfuehrungsdatum.to_german_string()
    )
}
#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{Metadaten, Ziel};
    use crate::budgetbutler::database::abrechnen::abrechnen::history::generate_abrechnungs_title_from_metadaten;
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Titel;
    use crate::io::disk::diskrepresentation::line::Line;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::person::builder::person;

    #[test]
    fn test_generate_abrechnungs_title_from_metadaten() {
        let result = generate_abrechnungs_title_from_metadaten(Metadaten {
            ausfuehrungsdatum: Datum::from_iso_string(&"2022-01-01".to_string()),
            abrechnende_person: person("Max Mustermann"),
            titel: Titel {
                titel: "Test".to_string(),
            },
            ziel: Ziel::ImportBuchungenAusApp,
            abrechnungsdatum: Datum::from_iso_string(&"2021-01-01".to_string()),
        });

        assert_eq!(result, "Test vom 01.01.2021, (importiert am 01.01.2022)");
    }

    const DEMO_ABRECHNUNG_INPUT_WITHOUT_METADATA: &str = "\
ergebnis

text
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
#######MaschinenimportEnd";

    #[test]
    fn test_generate_abrechnungs_title_from_filename() {
        let result = super::read_abrechnung(super::UnparsedAbrechnungsFile {
            file_content: Line::from_multiline_str(
                DEMO_ABRECHNUNG_INPUT_WITHOUT_METADATA.to_string(),
            ),
            file_name: "demo_abrechnung".to_string(),
        });

        assert_eq!(result.abrechnung_title, "demo_abrechnung");
    }

    const DEMO_ABRECHNUNG_INPUT: &str = "\
ergebnis

text
#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:Sebastian
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2024-11-29
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
#######MaschinenimportEnd";

    #[test]
    fn test_read_abrechnung() {
        let result = super::read_abrechnung(super::UnparsedAbrechnungsFile {
            file_content: Line::from_multiline_str(DEMO_ABRECHNUNG_INPUT.to_string()),
            file_name: "demo_abrechnung".to_string(),
        });

        assert_eq!(result.file_name_original, "demo_abrechnung");
        assert_eq!(
            result.abrechnung_title,
            "Mein Titel vom 29.11.2024, (importiert am 29.11.2024)"
        );
    }
}
