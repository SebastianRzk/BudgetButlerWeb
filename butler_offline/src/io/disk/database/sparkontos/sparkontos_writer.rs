use crate::io::disk::database::sparkontos::orders_writer::write_sparkonto;
use crate::io::disk::diskrepresentation::line::Line;
use crate::model::state::persistent_application_state::Database;

pub fn write_sparkontos(database: &Database) -> Vec<Line> {
    database
        .sparkontos
        .sparkontos
        .iter()
        .map(|l| write_sparkonto(&l.value))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_sparkontos;

    #[test]
    fn test_write_sparkontos() {
        let sparkonto = Sparkonto {
            name: name("MeinName"),
            kontotyp: Kontotyp::Sparkonto,
        };
        let database = generate_database_with_sparkontos(vec![sparkonto]);

        let lines = write_sparkontos(&database);

        assert_eq!(lines.len(), 1);
        assert_eq!(lines[0].line, "MeinName,Sparkonto");
    }
}
