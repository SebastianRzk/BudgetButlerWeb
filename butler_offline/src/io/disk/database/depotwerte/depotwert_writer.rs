use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::depotwerttyp::write_depotwerttyp;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::depotwert::Depotwert;

pub fn write_depotwert(depotwert: &Depotwert) -> Line {
    create_line(vec![
        Element::create_escaped(depotwert.name.get_name().clone()),
        Element::new(depotwert.isin.isin.clone()),
        write_depotwerttyp(depotwert.typ.clone()),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::depotwert::DepotwertTyp;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::name;

    #[test]
    fn test_write_depotwert() {
        let depotwert = Depotwert {
            name: name("MeinDepotwert"),
            isin: isin("DE000A0D9PT0"),
            typ: DepotwertTyp::ETF,
        };

        let line = write_depotwert(&depotwert);

        assert_eq!(line.line, "MeinDepotwert,DE000A0D9PT0,ETF");
    }
}
