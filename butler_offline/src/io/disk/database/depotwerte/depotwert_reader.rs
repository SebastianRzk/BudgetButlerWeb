use crate::io::disk::primitive::depotwerttyp::read_depotwerttyp;
use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::model::database::depotwert::Depotwert;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;

pub fn read_depotwert(line: Element) -> Depotwert {
    let name_segment = read_next_element(line);
    let isin = read_next_element(name_segment.rest);
    let typ_str = read_next_element(isin.rest);
    let typ = read_depotwerttyp(typ_str.element);

    Depotwert {
        name: Name::new(name_segment.element.element),
        isin: ISIN::new(isin.element.element),
        typ,
    }
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::depotwerte::depotwert_reader::read_depotwert;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_depotwert() {
        let line = element("MeinDepotwert,DE000A0D9PT0,ETF");
        let depotwert = read_depotwert(line);
        assert_eq!(depotwert.name, name("MeinDepotwert"));
        assert_eq!(depotwert.isin, isin("DE000A0D9PT0"));
        assert_eq!(depotwert.typ, DepotwertTyp::ETF);
    }
}
