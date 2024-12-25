use crate::io::disk::primitive::betrag::read_betrag;
use crate::io::disk::primitive::datum::read_datum;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::depotauszug::Depotauszug;
use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::database::sparbuchung::KontoReferenz;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;

pub fn read_depotauszug(line: Element) -> Depotauszug {
    let datum_segment = read_next_element(line);
    let datum = read_datum(datum_segment.element);
    let isin_segment = read_next_element(datum_segment.rest);
    let konto_segment = read_next_element(isin_segment.rest);
    let wert_segment = read_next_element(konto_segment.rest);
    let wert = read_betrag(wert_segment.element);

    Depotauszug {
        datum,
        depotwert: DepotwertReferenz::new(ISIN::new(isin_segment.element.element)),
        konto: KontoReferenz::new(Name::new(konto_segment.element.element)),
        wert,
    }
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::depotauszuege::depotauszug_reader::read_depotauszug;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::database::depotauszug::builder::{
        demo_depotauszug_aus_str, DEMO_DEPOTAUSZUG_STR,
    };

    #[test]
    fn test_read_depotwert() {
        let line = element(DEMO_DEPOTAUSZUG_STR);
        let depotauszug = read_depotauszug(line);

        assert_eq!(depotauszug, demo_depotauszug_aus_str());
    }
}
