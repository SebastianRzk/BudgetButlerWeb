use crate::io::disk::primitive::segment_reader::{read_next_element, Element};
use crate::io::disk::primitive::sparkontotyp::read_sparkontotyp;
use crate::model::database::sparkonto::Sparkonto;
use crate::model::primitives::name::Name;

pub fn read_sparkonto(line: Element) -> Sparkonto {
    let name_segment = read_next_element(line);
    let kontotyp = read_sparkontotyp(name_segment.rest);

    Sparkonto {
        name: Name::new(name_segment.element.element),
        kontotyp,
    }
}

#[cfg(test)]
mod tests {
    use crate::io::disk::database::sparkontos::sparkonto_reader::read_sparkonto;
    use crate::io::disk::primitive::segment_reader::builder::element;
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::name::name;

    #[test]
    fn test_read_sparkonto() {
        let line = element("MeinName,Sparkonto");
        let dauerauftrag = read_sparkonto(line);
        assert_eq!(dauerauftrag.name, name("MeinName"));
        assert_eq!(dauerauftrag.kontotyp, Kontotyp::Sparkonto);
    }
}
