use crate::io::disk::primitive::betrag_ohne_vorzeichen::read_betrag_ohne_vorzeichen;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::io::disk::primitive::sparbuchungtyp::read_sparbuchungtyp;
use crate::model::database::sparbuchung::{KontoReferenz, Sparbuchung};
use crate::model::primitives::name::Name;

pub fn read_sparbuchung(line: Element) -> Sparbuchung {
    let datum_segment = read_next_element(line);
    let datum = read_datum(datum_segment.element);
    let name_segment = read_next_element(datum_segment.rest);
    let betrag_segment = read_next_element(name_segment.rest);
    let betrag = read_betrag_ohne_vorzeichen(betrag_segment.element);
    let sparbuchungtyp_segment = read_next_element(betrag_segment.rest);
    let sparbuchungtyp = read_sparbuchungtyp(sparbuchungtyp_segment.element);
    let konto_segment = read_next_element(sparbuchungtyp_segment.rest);

    Sparbuchung {
        datum,
        name: Name::new(name_segment.element.element),
        wert: betrag,
        typ: sparbuchungtyp,
        konto: KontoReferenz::new(Name::new(konto_segment.element.element)),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::primitives::betrag::builder::u_betrag;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_sparbuchung() {
        let line = element("2024-01-01,DerName,123.12,Zinsen,DasKonto");
        let sparbuchung = read_sparbuchung(line);

        assert_eq!(sparbuchung.datum, Datum::new(1, 1, 2024));
        assert_eq!(sparbuchung.name, name("DerName"));
        assert_eq!(sparbuchung.wert, u_betrag(123, 12));
        assert_eq!(sparbuchung.typ, SparbuchungTyp::Zinsen);
        assert_eq!(sparbuchung.konto, konto_referenz("DasKonto"));
    }
}
