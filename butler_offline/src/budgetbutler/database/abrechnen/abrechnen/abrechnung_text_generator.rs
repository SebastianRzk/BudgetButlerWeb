use crate::budgetbutler::database::abrechnen::abrechnen::abrechnungs_file::{BUCHUNGEN_END, BUCHUNGEN_START, METADATEN_ABRECHNENDE_PERSON_KEY, METADATEN_ABRECHNUNGSDATUM_KEY, METADATEN_AUSFUEHRUNGSDATUM_KEY, METADATEN_END, METADATEN_START, METADATEN_TITEL_KEY, METADATEN_ZIEL_KEY, ZIEL_ABRECHNUNG_PARTNER, ZIEL_ABRECHNUNG_SELBST, ZIEL_IMPORT_EINZELBUCHUNGEN, ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP};
use crate::budgetbutler::database::abrechnen::gemeinsam_abrechnen::gemeinsame_abrechnung_generator::Titel;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::person::Person;

pub struct EinfuehrungsText {
    pub lines: Vec<Line>,
}

pub struct BuchungenText {
    pub text: String,
}

#[derive(Debug, PartialEq)]
pub struct Metadaten {
    pub ausfuehrungsdatum: Datum,
    pub abrechnungsdatum: Datum,
    pub abrechnende_person: Person,
    pub titel: Titel,
    pub ziel: Ziel,
}

#[derive(Debug, PartialEq)]
pub enum HeaderInsertModus {
    Insert,
    AlreadyInserted,
}

pub fn generiere_text(
    einfuehrungs_text: EinfuehrungsText,
    buchungen_text: BuchungenText,
    metadaten: Metadaten,
    header_modus: HeaderInsertModus,
) -> Vec<Line> {
    let mut lines = vec![];
    if header_modus == HeaderInsertModus::Insert {
        lines.push(Line::from(metadaten.titel.titel.clone()))
    }
    lines.append(&mut einfuehrungs_text.lines.clone());
    lines.append(&mut Line::from_multiline_str(maschinen_import_metadaten(
        metadaten,
    )));
    lines.append(&mut Line::from_multiline_str(maschienen_import(
        buchungen_text,
    )));
    lines
}

fn maschienen_import(buchungen: BuchungenText) -> String {
    format!("{}\n{}\n{}", BUCHUNGEN_START, buchungen.text, BUCHUNGEN_END)
}

#[derive(Debug, PartialEq, Clone)]
pub enum Ziel {
    GemeinsameAbrechnungFuerPartner,
    GemeinsameAbrechnungFuerSelbst,
    ImportGemeinsamerBuchungenAusApp,
    ImportBuchungenAusApp,
}

fn ziel_as_str(ziel: Ziel) -> String {
    match ziel {
        Ziel::GemeinsameAbrechnungFuerPartner => ZIEL_ABRECHNUNG_PARTNER.to_string(),
        Ziel::GemeinsameAbrechnungFuerSelbst => ZIEL_ABRECHNUNG_SELBST.to_string(),
        Ziel::ImportGemeinsamerBuchungenAusApp => {
            ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP.to_string()
        }
        Ziel::ImportBuchungenAusApp => ZIEL_IMPORT_EINZELBUCHUNGEN.to_string(),
    }
}

pub fn ziel_from_str(ziel_str: String) -> Ziel {
    match ziel_str.as_str() {
        ZIEL_ABRECHNUNG_PARTNER => Ziel::GemeinsameAbrechnungFuerPartner,
        ZIEL_ABRECHNUNG_SELBST => Ziel::GemeinsameAbrechnungFuerSelbst,
        ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP => Ziel::ImportGemeinsamerBuchungenAusApp,
        ZIEL_IMPORT_EINZELBUCHUNGEN => Ziel::ImportBuchungenAusApp,
        _ => panic!("Unbekanntes Ziel: {}", ziel_str),
    }
}

pub fn maschinen_import_metadaten(metadaten: Metadaten) -> String {
    let mut result = format!("{}\n", METADATEN_START).to_string();
    result.push_str(&format!(
        "{}{}\n",
        METADATEN_ABRECHNUNGSDATUM_KEY,
        metadaten.abrechnungsdatum.to_iso_string()
    ));
    result.push_str(&format!(
        "{}{}\n",
        METADATEN_ABRECHNENDE_PERSON_KEY, metadaten.abrechnende_person.person
    ));
    result.push_str(&format!(
        "{}{}\n",
        METADATEN_TITEL_KEY, metadaten.titel.titel
    ));
    result.push_str(&format!(
        "{}{}\n",
        METADATEN_ZIEL_KEY,
        ziel_as_str(metadaten.ziel)
    ));
    result.push_str(&format!(
        "{}{}\n",
        METADATEN_AUSFUEHRUNGSDATUM_KEY,
        metadaten.ausfuehrungsdatum.to_iso_string()
    ));
    result.push_str(&format!("{}\n", METADATEN_END));
    result
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::diskrepresentation::line::builder::as_string;

    #[test]
    fn test_ziel_from_str() {
        assert_eq!(
            ziel_from_str(ZIEL_ABRECHNUNG_PARTNER.to_string()),
            Ziel::GemeinsameAbrechnungFuerPartner
        );
        assert_eq!(
            ziel_from_str(ZIEL_ABRECHNUNG_SELBST.to_string()),
            Ziel::GemeinsameAbrechnungFuerSelbst
        );
        assert_eq!(
            ziel_from_str(ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP.to_string()),
            Ziel::ImportGemeinsamerBuchungenAusApp
        );
        assert_eq!(
            ziel_from_str(ZIEL_IMPORT_EINZELBUCHUNGEN.to_string()),
            Ziel::ImportBuchungenAusApp
        );
    }

    #[test]
    fn test_ziel_as_str() {
        assert_eq!(
            ziel_as_str(Ziel::GemeinsameAbrechnungFuerPartner),
            ZIEL_ABRECHNUNG_PARTNER.to_string()
        );
        assert_eq!(
            ziel_as_str(Ziel::GemeinsameAbrechnungFuerSelbst),
            ZIEL_ABRECHNUNG_SELBST.to_string()
        );
        assert_eq!(
            ziel_as_str(Ziel::ImportGemeinsamerBuchungenAusApp),
            ZIEL_IMPORT_GEMEINSAME_BUCHUNGEN_AUS_APP.to_string()
        );
        assert_eq!(
            ziel_as_str(Ziel::ImportBuchungenAusApp),
            ZIEL_IMPORT_EINZELBUCHUNGEN.to_string()
        );
    }

    #[test]
    fn test_generiere_text() {
        let einfuehrungs_text = EinfuehrungsText {
            lines: vec![Line::new("Hallo")],
        };
        let buchungen_text = BuchungenText {
            text: "Welt".to_string(),
        };
        let metadaten = Metadaten {
            ausfuehrungsdatum: Datum::new(1, 1, 2020),
            abrechnende_person: Person::new("Test_User".to_string()),
            titel: Titel {
                titel: "mein Titel".to_string(),
            },
            abrechnungsdatum: Datum::new(1, 1, 2021),
            ziel: Ziel::GemeinsameAbrechnungFuerPartner,
        };
        let result = generiere_text(
            einfuehrungs_text,
            buchungen_text,
            metadaten,
            HeaderInsertModus::Insert,
        );

        let result_as_str = as_string(&result);

        assert_eq!(
            result_as_str,
            "mein Titel
Hallo
#######MaschinenimportMetadatenStart
Abrechnungsdatum:2021-01-01
Abrechnende Person:Test_User
Titel:mein Titel
Ziel:GemeinsameAbrechnungFuerPartner
Ausfuehrungsdatum:2020-01-01
#######MaschinenimportMetadatenEnd
#######MaschinenimportStart
Welt
#######MaschinenimportEnd"
        );
    }
}
