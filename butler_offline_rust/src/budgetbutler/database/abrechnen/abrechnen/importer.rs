use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{generiere_text, BuchungenText, EinfuehrungsText, HeaderInsertModus, Metadaten};
use crate::budgetbutler::database::abrechnen::abrechnen::import::abrechnungen_sorter::{sort_abrechnungs_file, HeaderModus};
use crate::budgetbutler::database::abrechnen::abrechnen::import::einzelbuchungen_parser::read_einzelbuchungen;
use crate::budgetbutler::database::abrechnen::abrechnen::import::gemeinsame_buchungen_parser::read_gemeinsame_buchungen;
use crate::budgetbutler::database::abrechnen::abrechnen::import::metadaten_parser::parse_metadaten;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::io::disk::diskrepresentation::line::as_string;
use crate::model::primitives::datum::Datum;
use crate::model::state::persistent_application_state::Database;

pub fn import_abrechnung(database: &Database, abrechnung: &Abrechnung) -> Database {
    let sorted = sort_abrechnungs_file(&abrechnung.lines, HeaderModus::Drop);
    let parsed_buchungen = read_einzelbuchungen(sorted.einzel_buchungen);
    let parsed_gemeinsame_buchungen = read_gemeinsame_buchungen(sorted.gemeinsame_buchungen);

    let neue_einzelbuchungen = database
        .einzelbuchungen
        .change()
        .insert_all(parsed_buchungen);
    let new_database_after_einzelbuchungen = database.change_einzelbuchungen(neue_einzelbuchungen);

    let neue_gemeinsame_buchugnen = new_database_after_einzelbuchungen
        .gemeinsame_buchungen
        .change()
        .insert_all(parsed_gemeinsame_buchungen);
    new_database_after_einzelbuchungen.change_gemeinsame_buchungen(neue_gemeinsame_buchugnen)
}

pub fn update_abrechnung_for_import(abrechnung: Abrechnung, heute: Datum) -> Abrechnung {
    let sorted = sort_abrechnungs_file(&abrechnung.lines, HeaderModus::Preserve);
    let metadaten = parse_metadaten(&sorted);
    let new_metadaten = Metadaten {
        ausfuehrungsdatum: heute,
        abrechnende_person: metadaten.abrechnende_person,
        titel: metadaten.titel,
        ziel: metadaten.ziel.clone(),
        abrechnungsdatum: metadaten.abrechnungsdatum,
    };

    let einfuehrungs_text = EinfuehrungsText {
        lines: sorted.beschreibung.clone(),
    };
    let buchungen_text = BuchungenText {
        text: as_string(&sorted.einzel_buchungen),
    };
    Abrechnung {
        lines: generiere_text(einfuehrungs_text, buchungen_text, new_metadaten, HeaderInsertModus::AlreadyInserted),
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::importer::update_abrechnung_for_import;
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::io::disk::diskrepresentation::line::Line;
    use crate::model::primitives::datum::Datum;

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

    const DEMO_ABRECHNUNG_OUTPUT: &str = "\
ergebnis

text
#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:Sebastian
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2025-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
#######MaschinenimportEnd";

    #[test]
    fn test_update_abrechnung_for_import() {
        let heute = Datum::new(1, 1, 2025);
        let result = update_abrechnung_for_import(
            Abrechnung {
                lines: Line::from_multiline_str(DEMO_ABRECHNUNG_INPUT.to_string()),
            },
            heute,
        );

        assert_eq!(as_string(&result.lines), DEMO_ABRECHNUNG_OUTPUT);
    }
}
