use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
use crate::model::indiziert::Indiziert;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::name::Name;
use crate::model::primitives::type_description::TypeDescription;
use crate::model::state::persistent_application_state::Database;

pub fn calc_depotwert_beschreibungen(
    depotwerte: Vec<Indiziert<Depotwert>>,
) -> Vec<TypeDescription<String>> {
    depotwerte
        .iter()
        .map(|depotwert| TypeDescription {
            value: depotwert.value.isin.isin.clone(),
            description: format!(
                "{} ({})",
                depotwert.value.name.get_name(),
                depotwert.value.isin.isin
            ),
        })
        .collect()
}

pub fn calc_depotwert_beschreibung(isin: &ISIN, database: &Database) -> TypeDescription<String> {
    let unknown = Indiziert {
        index: 0,
        value: Depotwert {
            name: Name::new("Unbekannt".to_string()),
            isin: isin.clone(),
            typ: DepotwertTyp::ETF,
        },
        dynamisch: true,
    };
    let filter_for_find = database
        .depotwerte
        .select()
        .filter(|x| x.value.isin.isin == isin.isin);

    let depotwert = filter_for_find.find_first().unwrap_or(&unknown);
    TypeDescription {
        value: depotwert.value.isin.isin.clone(),
        description: format!(
            "{} ({})",
            depotwert.value.name.get_name(),
            depotwert.value.isin.isin
        ),
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::indiziert::builder::indiziert;
    use crate::model::primitives::isin::builder::isin;
    use crate::model::primitives::name::name;
    use crate::model::state::persistent_application_state::builder::generate_database_with_depotwerte;

    #[test]
    fn test_berechne_depotwert_beschreibung() {
        let depotwerte = vec![indiziert(Depotwert {
            name: name("Name1"),
            isin: isin("ISIN1"),
            typ: DepotwertTyp::Fond,
        })];
        let result = super::calc_depotwert_beschreibungen(depotwerte);
        assert_eq!(result.len(), 1);
        assert_eq!(result[0].value, "ISIN1");
        assert_eq!(result[0].description, "Name1 (ISIN1)");
    }

    #[test]
    fn test_calc_depotwert_beschreibung() {
        let depotwert = Depotwert {
            name: name("Name1"),
            isin: isin("ISIN1"),
            typ: DepotwertTyp::Fond,
        };
        let database = generate_database_with_depotwerte(vec![depotwert]);
        let result = super::calc_depotwert_beschreibung(&isin("ISIN1"), &database);
        assert_eq!(result.value, "ISIN1");
        assert_eq!(result.description, "Name1 (ISIN1)");
    }

    #[test]
    fn test_calc_depotwert_beschreibung_unknown() {
        let database = generate_database_with_depotwerte(vec![]);
        let result = super::calc_depotwert_beschreibung(&isin("ISIN1"), &database);
        assert_eq!(result.value, "ISIN1");
        assert_eq!(result.description, "Unbekannt (ISIN1)");
    }
}
