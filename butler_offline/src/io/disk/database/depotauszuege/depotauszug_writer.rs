use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::depotauszug::Depotauszug;

pub fn write_depotauszug(depotauszug: &Depotauszug) -> Line {
    create_line(vec![
        Element::new(depotauszug.datum.to_iso_string()),
        Element::new(depotauszug.depotwert.isin.isin.to_string()),
        Element::new(depotauszug.konto.konto_name.to_string()),
        Element::new(depotauszug.wert.to_iso_string()),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::depotauszug::builder::{
        demo_depotauszug_aus_str, DEMO_DEPOTAUSZUG_STR,
    };

    #[test]
    fn test_write_depotwert() {
        let depotauszug = demo_depotauszug_aus_str();

        let line = write_depotauszug(&depotauszug);

        assert_eq!(line.line, DEMO_DEPOTAUSZUG_STR);
    }
}
