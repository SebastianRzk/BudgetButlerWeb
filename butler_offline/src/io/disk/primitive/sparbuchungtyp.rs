use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::sparbuchung::SparbuchungTyp;

const MANUELLE_EINZAHLUNG: &str = "Manuelle Einzahlung";
const MANUELLE_AUSZAHLUNG: &str = "Manuelle Auszahlung";
const ZINSEN_STR: &str = "Zinsen";
const AUSSCHUETTUNG_STR: &str = "Ausschüttung";
const SONSTIGE_KOSTEN_STR: &str = "Sonstige Kosten";

pub fn read_sparbuchungtyp(rhythmus: Element) -> SparbuchungTyp {
    match rhythmus.element.as_str() {
        MANUELLE_EINZAHLUNG => SparbuchungTyp::ManuelleEinzahlung,
        MANUELLE_AUSZAHLUNG => SparbuchungTyp::ManuelleAuszahlung,
        ZINSEN_STR => SparbuchungTyp::Zinsen,
        AUSSCHUETTUNG_STR => SparbuchungTyp::Ausschuettung,
        SONSTIGE_KOSTEN_STR => SparbuchungTyp::SonstigeKosten,
        _ => panic!("Unknown sparbuchungstyp {}", rhythmus.element),
    }
}

pub fn write_sparbuchungtyp(sparbuchung_typ: &SparbuchungTyp) -> Element {
    Element {
        element: match sparbuchung_typ {
            SparbuchungTyp::ManuelleEinzahlung => MANUELLE_EINZAHLUNG.to_string(),
            SparbuchungTyp::ManuelleAuszahlung => MANUELLE_AUSZAHLUNG.to_string(),
            SparbuchungTyp::Zinsen => ZINSEN_STR.to_string(),
            SparbuchungTyp::Ausschuettung => AUSSCHUETTUNG_STR.to_string(),
            SparbuchungTyp::SonstigeKosten => SONSTIGE_KOSTEN_STR.to_string(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_sparbuchungtyp() {
        let manueller_auftrag = element("Manuelle Auszahlung");
        assert_eq!(
            read_sparbuchungtyp(manueller_auftrag),
            SparbuchungTyp::ManuelleAuszahlung
        );

        let manueller_auftrag = element("Manuelle Einzahlung");
        assert_eq!(
            read_sparbuchungtyp(manueller_auftrag),
            SparbuchungTyp::ManuelleEinzahlung
        );

        let zinsen = element("Zinsen");
        assert_eq!(read_sparbuchungtyp(zinsen), SparbuchungTyp::Zinsen);

        let ausschuettung = element("Ausschüttung");
        assert_eq!(
            read_sparbuchungtyp(ausschuettung),
            SparbuchungTyp::Ausschuettung
        );

        let sonstige_kosten = element("Sonstige Kosten");
        assert_eq!(
            read_sparbuchungtyp(sonstige_kosten),
            SparbuchungTyp::SonstigeKosten
        );
    }

    #[test]
    fn test_write_sparbuchungtyp() {
        let manueller_auftrag = write_sparbuchungtyp(&SparbuchungTyp::ManuelleEinzahlung);
        assert_eq!(manueller_auftrag.element, "Manuelle Einzahlung");

        let manueller_auftrag = write_sparbuchungtyp(&SparbuchungTyp::ManuelleAuszahlung);
        assert_eq!(manueller_auftrag.element, "Manuelle Auszahlung");

        let zinsen = write_sparbuchungtyp(&SparbuchungTyp::Zinsen);
        assert_eq!(zinsen.element, "Zinsen");

        let ausschuettung = write_sparbuchungtyp(&SparbuchungTyp::Ausschuettung);
        assert_eq!(ausschuettung.element, "Ausschüttung");

        let sonstige_kosten = write_sparbuchungtyp(&SparbuchungTyp::SonstigeKosten);
        assert_eq!(sonstige_kosten.element, "Sonstige Kosten");
    }
}
