use crate::io::disk::primitive::segment_reader::Element;
use crate::model::database::sparkonto::Kontotyp;

const DEPOT_STR: &str = "Depot";
const SPARKONTO_STR: &str = "Sparkonto";
const GENOSSENSCHAFTS_ANTEILE_STR: &str = "Genossenschafts-Anteile";

pub fn read_sparkontotyp(kontotyp: Element) -> Kontotyp {
    match kontotyp.element.as_str() {
        DEPOT_STR => Kontotyp::Depot,
        SPARKONTO_STR => Kontotyp::Sparkonto,
        GENOSSENSCHAFTS_ANTEILE_STR => Kontotyp::GenossenschaftsAnteile,
        _ => panic!("Unknown sparkontotyp {}", kontotyp.element),
    }
}

pub fn write_sparkontotyp(kontotyp: Kontotyp) -> Element {
    Element {
        element: match kontotyp {
            Kontotyp::GenossenschaftsAnteile => GENOSSENSCHAFTS_ANTEILE_STR.to_string(),
            Kontotyp::Depot => DEPOT_STR.to_string(),
            Kontotyp::Sparkonto => SPARKONTO_STR.to_string(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_kontotyp() {
        let depot = element("Depot");
        assert_eq!(read_sparkontotyp(depot), Kontotyp::Depot);

        let sparkonto = element("Sparkonto");
        assert_eq!(read_sparkontotyp(sparkonto), Kontotyp::Sparkonto);

        let gemossenschaftsanteile = element("Genossenschafts-Anteile");
        assert_eq!(
            read_sparkontotyp(gemossenschaftsanteile),
            Kontotyp::GenossenschaftsAnteile
        );
    }

    #[test]
    fn test_write_kontotyp() {
        let sparkonto = write_sparkontotyp(Kontotyp::Sparkonto);
        assert_eq!(sparkonto.element, "Sparkonto");

        let depot = write_sparkontotyp(Kontotyp::Depot);
        assert_eq!(depot.element, "Depot");

        let genossenschafts_anteile = write_sparkontotyp(Kontotyp::GenossenschaftsAnteile);
        assert_eq!(genossenschafts_anteile.element, "Genossenschafts-Anteile");
    }
}
