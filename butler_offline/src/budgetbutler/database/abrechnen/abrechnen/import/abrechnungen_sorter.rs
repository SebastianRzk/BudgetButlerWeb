use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::SortedAbrechnungsFile;
use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::{
    BUCHUNGEN_EINZEL_HEADER, BUCHUNGEN_END, BUCHUNGEN_GEMEINSAM_HEADER, BUCHUNGEN_START,
    METADATEN_END, METADATEN_START,
};
use crate::io::disk::diskrepresentation::line::Line;
use std::collections::HashMap;

#[derive(Debug, PartialEq)]
pub enum HeaderModus {
    Preserve,
    Drop,
}

pub fn sort_abrechnungs_file(file: &Vec<Line>, header_modus: HeaderModus) -> SortedAbrechnungsFile {
    let mut current_modus = Modus::Beschreibung;
    let mut result = HashMap::<Modus, Vec<Line>>::new();
    for line in file {
        let modus_check_result = check_modus(&line);
        if let ModusCheckResult::NewModus(new_modus) = modus_check_result {
            current_modus = new_modus;
            continue;
        }
        if let ModusCheckResult::Header(header_modus) = modus_check_result.clone() {
            current_modus = header_modus;
        }

        if modus_check_result == ModusCheckResult::Header(Modus::EinzelBuchungen)
            && header_modus == HeaderModus::Drop
        {
            continue;
        }

        if modus_check_result == ModusCheckResult::Header(Modus::GemeinsameBuchungen)
            && header_modus == HeaderModus::Drop
        {
            continue;
        }
        let current_list = result.entry(current_modus.clone()).or_insert_with(Vec::new);
        current_list.push(line.clone());
    }
    let empty_vec = Vec::<Line>::new();
    SortedAbrechnungsFile {
        beschreibung: result
            .get(&Modus::Beschreibung)
            .unwrap_or(&empty_vec)
            .clone(),
        einzel_buchungen: result
            .get(&Modus::EinzelBuchungen)
            .unwrap_or(&Vec::new())
            .clone(),
        gemeinsame_buchungen: result
            .get(&Modus::GemeinsameBuchungen)
            .unwrap_or(&Vec::new())
            .clone(),
        metadaten: result.get(&Modus::Metadaten).unwrap_or(&Vec::new()).clone(),
    }
}

fn check_modus(line: &Line) -> ModusCheckResult {
    match line.line.trim() {
        BUCHUNGEN_EINZEL_HEADER => ModusCheckResult::Header(Modus::EinzelBuchungen),
        BUCHUNGEN_START => ModusCheckResult::NewModus(Modus::EinzelBuchungen),
        BUCHUNGEN_GEMEINSAM_HEADER => ModusCheckResult::Header(Modus::GemeinsameBuchungen),
        BUCHUNGEN_END => ModusCheckResult::NewModus(Modus::Nothing),
        METADATEN_START => ModusCheckResult::NewModus(Modus::Metadaten),
        METADATEN_END => ModusCheckResult::NewModus(Modus::Nothing),
        _ => ModusCheckResult::SameModus,
    }
}

#[derive(PartialEq, Clone)]
enum ModusCheckResult {
    NewModus(Modus),
    Header(Modus),
    SameModus,
}

#[derive(Hash, Eq, PartialEq, Clone, Debug)]
enum Modus {
    Beschreibung,
    Nothing,
    Metadaten,
    EinzelBuchungen,
    GemeinsameBuchungen,
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::abrechnen::abrechnen::import::abrechnungen_sorter::{
        sort_abrechnungs_file, HeaderModus,
    };
    use crate::io::disk::diskrepresentation::file::File;

    const DEMO_ABRECHNUNG: &str = "\
ergebnis text
#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:Sebastian
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2024-11-29
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag
2024-11-01,NeueKategorie,Name,-117.00
2024-11-21,NeueKategorie,asd,-617.00
#######MaschinenimportEnd
";

    #[test]
    pub fn test_sorter() {
        let file = File::from_str(DEMO_ABRECHNUNG);
        let sorted_file = sort_abrechnungs_file(&file.lines, HeaderModus::Drop);
        assert_eq!(sorted_file.beschreibung.len(), 1);
        assert_eq!(
            sorted_file.beschreibung.get(0).unwrap().line,
            "ergebnis text"
        );

        assert_eq!(sorted_file.metadaten.len(), 5);
        assert_eq!(
            sorted_file.metadaten.get(0).unwrap().line,
            "Abrechnungsdatum:2024-11-29"
        );
        assert_eq!(
            sorted_file.metadaten.get(1).unwrap().line,
            "Abrechnende Person:Sebastian"
        );
        assert_eq!(
            sorted_file.metadaten.get(2).unwrap().line,
            "Titel:Mein Titel"
        );
        assert_eq!(
            sorted_file.metadaten.get(3).unwrap().line,
            "Ziel:GemeinsameAbrechnungFuerSelbst"
        );

        assert_eq!(
            sorted_file.metadaten.get(4).unwrap().line,
            "Ausfuehrungsdatum:2024-11-29"
        );

        assert_eq!(sorted_file.einzel_buchungen.len(), 2);
        assert_eq!(
            sorted_file.einzel_buchungen.get(0).unwrap().line,
            "2024-11-01,NeueKategorie,Name,-117.00"
        );
        assert_eq!(
            sorted_file.einzel_buchungen.get(1).unwrap().line,
            "2024-11-21,NeueKategorie,asd,-617.00"
        );
    }

    const DEMO_ABRECHNUNG_GEMEINSAM: &str = "\
ergebnis text
#######MaschinenimportMetadatenStart
Abrechnungsdatum:2024-11-29
Abrechnende Person:Sebastian
Titel:Mein Titel
Ziel:GemeinsameAbrechnungFuerSelbst
Ausfuehrungsdatum:2024-11-29
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Datum,Kategorie,Name,Betrag,Person
2024-11-01,NeueKategorie,Name,-117.00,PersonA
2024-11-21,NeueKategorie,asd,-617.00,PersonB
#######MaschinenimportEnd
";

    #[test]
    pub fn test_sorter_gemeinsam() {
        let file = File::from_str(DEMO_ABRECHNUNG_GEMEINSAM);
        let sorted_file = sort_abrechnungs_file(&file.lines, HeaderModus::Drop);
        assert_eq!(sorted_file.beschreibung.len(), 1);
        assert_eq!(
            sorted_file.beschreibung.get(0).unwrap().line,
            "ergebnis text"
        );

        assert_eq!(sorted_file.metadaten.len(), 5);
        assert_eq!(
            sorted_file.metadaten.get(0).unwrap().line,
            "Abrechnungsdatum:2024-11-29"
        );
        assert_eq!(
            sorted_file.metadaten.get(1).unwrap().line,
            "Abrechnende Person:Sebastian"
        );
        assert_eq!(
            sorted_file.metadaten.get(2).unwrap().line,
            "Titel:Mein Titel"
        );
        assert_eq!(
            sorted_file.metadaten.get(3).unwrap().line,
            "Ziel:GemeinsameAbrechnungFuerSelbst"
        );

        assert_eq!(
            sorted_file.metadaten.get(4).unwrap().line,
            "Ausfuehrungsdatum:2024-11-29"
        );

        assert_eq!(sorted_file.einzel_buchungen.len(), 0);

        assert_eq!(sorted_file.gemeinsame_buchungen.len(), 2);
        assert_eq!(
            sorted_file.gemeinsame_buchungen.get(0).unwrap().line,
            "2024-11-01,NeueKategorie,Name,-117.00,PersonA"
        );
        assert_eq!(
            sorted_file.gemeinsame_buchungen.get(1).unwrap().line,
            "2024-11-21,NeueKategorie,asd,-617.00,PersonB"
        );
    }
}
