use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::segment_reader::Element;
use crate::io::disk::primitive::sparkontotyp::write_sparkontotyp;
use crate::model::database::sparkonto::Sparkonto;

pub fn write_sparkonto(sparkonto: &Sparkonto) -> Line {
    create_line(vec![
        Element::create_escaped(sparkonto.name.get_name().clone()),
        write_sparkontotyp(sparkonto.kontotyp.clone()),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::name::name;

    #[test]
    fn test_write_sparkonto() {
        let sparkonto = Sparkonto {
            name: name("MeinSparkonto"),
            kontotyp: Kontotyp::Sparkonto,
        };

        let line = write_sparkonto(&sparkonto);

        assert_eq!(line.line, "MeinSparkonto,Sparkonto");
    }
}
