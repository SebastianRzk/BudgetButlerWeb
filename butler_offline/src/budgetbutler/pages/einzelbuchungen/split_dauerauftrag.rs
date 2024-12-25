use crate::budgetbutler::database::reader::rhythmus::get_monatsdelta_for_rhythmus;
use crate::model::eigenschaften::besitzt_start_und_ende_datum::BesitztStartUndEndeDatum;
use crate::model::metamodel::datum_selektion::DatumSelektion;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct SplitDauerauftragViewResult {
    pub database_version: DatabaseVersion,
    pub dauerauftrag_id: u32,
    pub wert: Betrag,
    pub datum: Vec<DatumSelektion>,
}

pub struct SplitDauerauftragContext<'a> {
    pub database: &'a Database,
    pub dauerauftrag_id: u32,
}

pub fn handle_split(context: SplitDauerauftragContext) -> SplitDauerauftragViewResult {
    let selected_dauerauftrag = context.database.dauerauftraege.get(context.dauerauftrag_id);
    let mut laufdatum = selected_dauerauftrag.start_datum().clone();

    let mut datum = Vec::new();

    while laufdatum <= selected_dauerauftrag.ende_datum().clone() {
        let can_be_chosen = laufdatum != selected_dauerauftrag.start_datum().clone();
        datum.push(DatumSelektion {
            datum: laufdatum.clone(),
            can_be_chosen,
        });
        laufdatum = laufdatum.add_months(get_monatsdelta_for_rhythmus(
            selected_dauerauftrag.value.rhythmus,
        ));
    }

    if datum.len() > 1 {
        let letztes_datum = datum.pop().unwrap();
        datum.push(DatumSelektion {
            datum: letztes_datum.datum,
            can_be_chosen: false,
        });
    }

    SplitDauerauftragViewResult {
        database_version: context.database.db_version.clone(),
        dauerauftrag_id: context.dauerauftrag_id,
        wert: selected_dauerauftrag.value.betrag.clone(),
        datum,
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::dauerauftrag::Dauerauftrag;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::kategorie::builder::demo_kategorie;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::rhythmus::Rhythmus::Monatlich;
    use crate::model::state::persistent_application_state::builder::generate_database_with_dauerauftraege;

    #[test]
    pub fn test_handle_split() {
        let database = generate_database_with_dauerauftraege(vec![Dauerauftrag {
            start_datum: Datum::new(1, 1, 2021),
            ende_datum: Datum::new(2, 4, 2021),
            kategorie: demo_kategorie(),
            betrag: zwei(),
            rhythmus: Monatlich,
            name: demo_name(),
        }]);

        let result = super::handle_split(super::SplitDauerauftragContext {
            database: &database,
            dauerauftrag_id: 1,
        });

        assert_eq!(result.wert, zwei());
        assert_eq!(result.datum.len(), 4);
        assert_eq!(result.datum[0].can_be_chosen, false);
        assert_eq!(result.datum[0].datum, Datum::new(1, 1, 2021));
        assert_eq!(result.datum[1].can_be_chosen, true);
        assert_eq!(result.datum[1].datum, Datum::new(1, 2, 2021));
        assert_eq!(result.datum[2].can_be_chosen, true);
        assert_eq!(result.datum[2].datum, Datum::new(1, 3, 2021));
        assert_eq!(result.datum[3].can_be_chosen, false);
        assert_eq!(result.datum[3].datum, Datum::new(1, 4, 2021));
    }
}
