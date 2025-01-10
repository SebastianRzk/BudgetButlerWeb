use crate::budgetbutler::database::abrechnen::abrechnen::abrechnung_text_generator::{generiere_text, BuchungenText, EinfuehrungsText, HeaderInsertModus, Metadaten};
use crate::budgetbutler::database::abrechnen::abrechnen::einzel_buchungen_text_generator::{einzelbuchungen_as_import_text, gemeinsame_buchungen_as_import_text};
use crate::budgetbutler::database::abrechnen::abrechnen::import::abrechnungen_sorter::{sort_abrechnungs_file, HeaderModus};
use crate::budgetbutler::database::abrechnen::abrechnen::import::einzelbuchungen_parser::read_einzelbuchungen;
use crate::budgetbutler::database::abrechnen::abrechnen::import::gemeinsame_buchungen_parser::read_gemeinsame_buchungen;
use crate::budgetbutler::database::abrechnen::abrechnen::import::metadaten_parser::parse_metadaten;
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Abrechnung;
use crate::io::disk::diskrepresentation::line::as_string;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::state::persistent_application_state::Database;
use std::collections::HashMap;

pub fn pruefe_ob_kategorien_bereits_in_datenbank_vorhanden_sind(
    database: &Database,
    abrechnung: &Abrechnung,
) -> KategorienPruefungsErgebnis {
    let kategorien_in_abrechnung = read_kategorien_in_abrechnung(abrechnung);
    let mut fehlende_kategorien = Vec::new();
    let alle_kategorien = database.einzelbuchungen.get_kategorien();

    for kategorie in kategorien_in_abrechnung {
        if !alle_kategorien.contains(&kategorie.kategorie) {
            fehlende_kategorien.push(kategorie);
        }
    }
    KategorienPruefungsErgebnis {
        kategorien_nicht_in_datenbank: fehlende_kategorien,
    }
}

pub fn aktualisiere_kategorien(
    abrechung: Abrechnung,
    kategorien_mapping: HashMap<Kategorie, Kategorie>,
) -> Abrechnung {
    let sorted = sort_abrechnungs_file(&abrechung.lines, HeaderModus::Drop);
    let parsed_buchungen = read_einzelbuchungen(sorted.einzel_buchungen.clone());
    let parsed_gemeinsame_buchungen =
        read_gemeinsame_buchungen(sorted.gemeinsame_buchungen.clone());

    let mut neue_buchungen = Vec::new();
    for buchung in parsed_buchungen {
        let neue_kategorie = kategorien_mapping
            .get(&buchung.kategorie)
            .unwrap_or(&buchung.kategorie);
        neue_buchungen.push(buchung.change_kategorie(neue_kategorie.clone()));
    }
    let mut neue_gemeinsame_buchungen = Vec::new();
    for buchung in parsed_gemeinsame_buchungen {
        let neue_kategorie = kategorien_mapping
            .get(&buchung.kategorie)
            .unwrap_or(&buchung.kategorie);
        neue_gemeinsame_buchungen.push(buchung.change_kategorie(neue_kategorie.clone()));
    }

    let import_text;
    if neue_buchungen.len() > 0 {
        import_text = einzelbuchungen_as_import_text(&neue_buchungen);
    } else {
        import_text = gemeinsame_buchungen_as_import_text(&neue_gemeinsame_buchungen);
    }

    let new_abrechnung = Abrechnung {
        lines: generiere_text(
            EinfuehrungsText {
                lines: sorted.beschreibung.clone(),
            },
            import_text,
            parse_metadaten(&sorted),
            HeaderInsertModus::AlreadyInserted,
        ),
    };
    new_abrechnung
}

#[derive(Debug, Clone)]
pub struct KategorieMitBeispiel {
    pub kategorie: Kategorie,
    pub beispiel: Vec<String>,
}

pub struct KategorienPruefungsErgebnis {
    pub kategorien_nicht_in_datenbank: Vec<KategorieMitBeispiel>,
}

fn read_kategorien_in_abrechnung(abrechnung: &Abrechnung) -> Vec<KategorieMitBeispiel> {
    let sorted = sort_abrechnungs_file(&abrechnung.lines, HeaderModus::Drop);
    let parsed_buchungen = read_einzelbuchungen(sorted.einzel_buchungen);
    let parsed_gemeinsame_buchungen = read_gemeinsame_buchungen(sorted.gemeinsame_buchungen);

    let mut kategorien: Vec<KategorieMitBeispiel> = Vec::new();
    for buchung in parsed_buchungen {
        kategorien.push(KategorieMitBeispiel {
            kategorie: buchung.kategorie,
            beispiel: vec![format!(
                "{}({}€)",
                buchung.name.get_name(),
                buchung.betrag.to_german_string()
            )],
        });
    }
    for buchung in parsed_gemeinsame_buchungen {
        kategorien.push(KategorieMitBeispiel {
            kategorie: buchung.kategorie,
            beispiel: vec![format!(
                "{}({}€)",
                buchung.name.get_name(),
                buchung.betrag.to_german_string()
            )],
        })
    }
    unify_kategorien(kategorien)
}

fn unify_kategorien(
    kategorien_mit_beispiel: Vec<KategorieMitBeispiel>,
) -> Vec<KategorieMitBeispiel> {
    let mut data: HashMap<Kategorie, KategorieMitBeispiel> = HashMap::new();

    for kategorie_mit_beispiel in kategorien_mit_beispiel {
        if data.contains_key(&kategorie_mit_beispiel.kategorie) {
            let existing = data.get_mut(&kategorie_mit_beispiel.kategorie).unwrap();
            existing.beispiel.extend(kategorie_mit_beispiel.beispiel);
        } else {
            data.insert(
                kategorie_mit_beispiel.kategorie.clone(),
                kategorie_mit_beispiel,
            );
        }
    }

    let mut values = data.into_values().collect::<Vec<KategorieMitBeispiel>>();
    values.sort_by(|a, b| a.kategorie.cmp(&b.kategorie));
    values
}

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
        lines: generiere_text(
            einfuehrungs_text,
            buchungen_text,
            new_metadaten,
            HeaderInsertModus::AlreadyInserted,
        ),
    }
}

#[cfg(test)]
mod tests {
    use std::collections::HashMap;
    use crate::budgetbutler::database::abrechnen::abrechnen::importer::update_abrechnung_for_import;
    use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::builder::abrechnung_from_str;
    use crate::io::disk::diskrepresentation::line::builder::as_string;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::kategorie;

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
        let result =
            update_abrechnung_for_import(abrechnung_from_str(DEMO_ABRECHNUNG_INPUT), heute);

        assert_eq!(as_string(&result.lines), DEMO_ABRECHNUNG_OUTPUT);
    }

    const DEMO_ABRECHNUNG_MIT_KATEGORIE: &str = "\
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
2024-11-29,TestKategorie,TestName,10.0
#######MaschinenimportEnd";

    #[test]
    fn test_read_kategorien() {
        let abr = abrechnung_from_str(DEMO_ABRECHNUNG_MIT_KATEGORIE);
        let kategorien = super::read_kategorien_in_abrechnung(&abr);
        assert_eq!(kategorien.len(), 1);
        assert_eq!(kategorien[0].kategorie, kategorie("TestKategorie"));
        assert_eq!(kategorien[0].beispiel, vec!["TestName(10,00€)"]);
    }

    const DEMO_ABRECHNUNG_MIT_DUPLIKAT_KATEGORIE: &str = "\
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
2024-11-29,TestKategorie,TestName,10.0
2024-11-29,TestKategorie,TestName2,11.0
2024-11-29,TestKategorie3,TestName3,10.0
#######MaschinenimportEnd";

    #[test]
    fn test_read_kategorien_should_unify_on_kategorie_name() {
        let abr = abrechnung_from_str(DEMO_ABRECHNUNG_MIT_DUPLIKAT_KATEGORIE);
        let kategorien = super::read_kategorien_in_abrechnung(&abr);
        assert_eq!(kategorien.len(), 2);
        assert_eq!(kategorien[0].kategorie, kategorie("TestKategorie"));
        assert_eq!(
            kategorien[0].beispiel,
            vec!["TestName(10,00€)", "TestName2(11,00€)"]
        );
        assert_eq!(kategorien[1].kategorie, kategorie("TestKategorie3"));
        assert_eq!(kategorien[1].beispiel, vec!["TestName3(10,00€)"]);
    }

    const DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE: &str = "\
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
2024-11-29,TestKategorie2,TestName,10.00
2024-11-29,TestKategorie2,TestName2,11.00
2024-11-29,TestKategorie3,TestName3,10.00
#######MaschinenimportEnd";

    #[test]
    fn test_aktualisiere_kategorien_einzelbuchungen() {
        let abr = abrechnung_from_str(DEMO_ABRECHNUNG_MIT_DUPLIKAT_KATEGORIE);
        let mut mapping = HashMap::new();
        mapping.insert(kategorie("TestKategorie"), kategorie("TestKategorie2"));

        let result = super::aktualisiere_kategorien(abr, mapping);

        assert_eq!(
            as_string(&result.lines),
            DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE
        );
    }

    const DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE_GEMEINSAM: &str = "\
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
Datum,Kategorie,Name,Betrag,Person
2024-11-29,TestKategorie2,TestName,10.00,TestPerson
2024-11-29,TestKategorie2,TestName2,11.00,TestPerson
2024-11-29,TestKategorie3,TestName3,10.00,TestPerson
#######MaschinenimportEnd";

    const DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE_GEMEINSAM_ERGEBNIS: &str = "\
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
Datum,Kategorie,Name,Betrag,Person
2024-11-29,TestKategorieXOX,TestName,10.00,TestPerson
2024-11-29,TestKategorieXOX,TestName2,11.00,TestPerson
2024-11-29,TestKategorie3,TestName3,10.00,TestPerson
#######MaschinenimportEnd";

    #[test]
    fn test_aktualisiere_kategorien_gemeinsame_buchungen() {
        let abr =
            abrechnung_from_str(DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE_GEMEINSAM);
        let mut mapping = HashMap::new();
        mapping.insert(kategorie("TestKategorie2"), kategorie("TestKategorieXOX"));

        let result = super::aktualisiere_kategorien(abr, mapping);

        assert_eq!(
            as_string(&result.lines),
            DEMO_ABRECHNUNG_MIT_DUPLIKAT_AKTUALISIERTE_KATEGORIE_GEMEINSAM_ERGEBNIS
        );
    }
}
