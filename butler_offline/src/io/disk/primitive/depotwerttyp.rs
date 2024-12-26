use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::depotwert::DepotwertTyp;

const ETF_STR: &str = "ETF";
const FOND_STR: &str = "Fond";
const EINZELAKTIE_STR: &str = "Einzelaktie";
const CRYPTO_STR: &str = "Crypto";
const ROBOT_STR: &str = "Robot";

pub fn read_depotwerttyp(element: Element) -> DepotwertTyp {
    match element.element.as_str() {
        ETF_STR => DepotwertTyp::ETF,
        FOND_STR => DepotwertTyp::Fond,
        EINZELAKTIE_STR => DepotwertTyp::Einzelaktie,
        CRYPTO_STR => DepotwertTyp::Crypto,
        ROBOT_STR => DepotwertTyp::Robot,
        _ => panic!("Unknown depotwerttyp {}", element.element),
    }
}

pub fn write_depotwerttyp(depotwert_typ: DepotwertTyp) -> Element {
    Element {
        element: match depotwert_typ {
            DepotwertTyp::ETF => ETF_STR.to_string(),
            DepotwertTyp::Fond => FOND_STR.to_string(),
            DepotwertTyp::Einzelaktie => EINZELAKTIE_STR.to_string(),
            DepotwertTyp::Crypto => CRYPTO_STR.to_string(),
            DepotwertTyp::Robot => ROBOT_STR.to_string(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_depotwerttyp() {
        let etf = element("ETF");
        assert_eq!(read_depotwerttyp(etf), DepotwertTyp::ETF);

        let fond = element("Fond");
        assert_eq!(read_depotwerttyp(fond), DepotwertTyp::Fond);

        let einzelaktie = element("Einzelaktie");
        assert_eq!(read_depotwerttyp(einzelaktie), DepotwertTyp::Einzelaktie);

        let crypto = element("Crypto");
        assert_eq!(read_depotwerttyp(crypto), DepotwertTyp::Crypto);

        let robot = element("Robot");
        assert_eq!(read_depotwerttyp(robot), DepotwertTyp::Robot);
    }

    #[test]
    fn test_write_depotwerttyp() {
        let etf = write_depotwerttyp(DepotwertTyp::ETF);
        assert_eq!(etf.element, "ETF");

        let fond = write_depotwerttyp(DepotwertTyp::Fond);
        assert_eq!(fond.element, "Fond");

        let einzelaktie = write_depotwerttyp(DepotwertTyp::Einzelaktie);
        assert_eq!(einzelaktie.element, "Einzelaktie");

        let crypto = write_depotwerttyp(DepotwertTyp::Crypto);
        assert_eq!(crypto.element, "Crypto");

        let robot = write_depotwerttyp(DepotwertTyp::Robot);
        assert_eq!(robot.element, "Robot");
    }
}
