use crate::io::disk::primitive::segment_reader::Element;
use crate::model::primitives::rhythmus::Rhythmus;

const MONATLICH_STR: &str = "monatlich";
const VIERTELJAERLICH_STR: &str = "vierteljährlich";
const HALBJAEHRLICH_STR: &str = "halbjährlich";
const JAEHRLICH_STR: &str = "jährlich";

pub fn read_rhythmus(rhythmus: Element) -> Rhythmus {
    match rhythmus.element.as_str() {
        MONATLICH_STR => Rhythmus::Monatlich,
        VIERTELJAERLICH_STR => Rhythmus::Vierteljaehrlich,
        HALBJAEHRLICH_STR => Rhythmus::Halbjaehrlich,
        JAEHRLICH_STR => Rhythmus::Jaehrlich,
        _ => panic!("Unknown rhythmus {}", rhythmus.element),
    }
}

pub fn write_rhythmus(rhythmus: Rhythmus) -> Element {
    Element {
        element: match rhythmus {
            Rhythmus::Monatlich => MONATLICH_STR.to_string(),
            Rhythmus::Vierteljaehrlich => VIERTELJAERLICH_STR.to_string(),
            Rhythmus::Halbjaehrlich => HALBJAEHRLICH_STR.to_string(),
            Rhythmus::Jaehrlich => JAEHRLICH_STR.to_string(),
        },
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::io::disk::primitive::segment_reader::builder::element;

    #[test]
    fn test_read_rhythmus() {
        let monatlich = element("monatlich");
        assert_eq!(read_rhythmus(monatlich), Rhythmus::Monatlich);

        let vierteljaehrlich = element("vierteljährlich");
        assert_eq!(read_rhythmus(vierteljaehrlich), Rhythmus::Vierteljaehrlich);

        let halbjaehrlich = element("halbjährlich");
        assert_eq!(read_rhythmus(halbjaehrlich), Rhythmus::Halbjaehrlich);

        let jaehrlich = element("jährlich");
        assert_eq!(read_rhythmus(jaehrlich), Rhythmus::Jaehrlich);
    }

    #[test]
    fn test_write_rhythmus() {
        let monatlich = write_rhythmus(Rhythmus::Monatlich);
        assert_eq!(monatlich.element, "monatlich");

        let vierteljaehrlich = write_rhythmus(Rhythmus::Vierteljaehrlich);
        assert_eq!(vierteljaehrlich.element, "vierteljährlich");

        let halbjaehrlich = write_rhythmus(Rhythmus::Halbjaehrlich);
        assert_eq!(halbjaehrlich.element, "halbjährlich");

        let jaehrlich = write_rhythmus(Rhythmus::Jaehrlich);
        assert_eq!(jaehrlich.element, "jährlich");
    }
}
