use crate::budgetbutler::database::select::functions::filters::{
    filter_auf_depot, filter_auf_konto,
};
use crate::model::primitives::datum::Datum;
use crate::model::primitives::name::Name;
use crate::model::state::persistent_application_state::Database;

pub struct DepotMetaInfo {
    pub name: Name,
    pub letzte_buchung: Option<Datum>,
    pub letzter_depotauszug: Option<Datum>,
}

pub fn berechne_depot_meta_infos(database: &Database) -> Vec<DepotMetaInfo> {
    let mut result = vec![];

    for depot in database
        .sparkontos
        .select()
        .filter(filter_auf_depot)
        .collect()
    {
        let letzter_depotauszug = database
            .depotauszuege
            .select()
            .filter(filter_auf_konto(depot.value.as_reference()))
            .last()
            .map(|depotauszug| depotauszug.value.datum.clone())
            .clone();

        let letzte_buchung = database
            .order
            .select()
            .filter(filter_auf_konto(depot.value.as_reference()))
            .last()
            .map(|order| order.value.datum.clone())
            .clone();

        result.push(DepotMetaInfo {
            name: depot.value.name.clone(),
            letzte_buchung,
            letzter_depotauszug,
        });
    }
    result
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::budgetbutler::database::sparen::berechne_depot_metainfo::berechne_depot_meta_infos;
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::builder::demo_depotwert_referenz;
    use crate::model::database::order::{Order, OrderTyp};
    use crate::model::database::sparbuchung::builder::demo_konto_referenz;
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_application_state::builder::{
        demo_database_version, generate_database_with_sparkontos, generate_empty_database,
    };
    use crate::model::state::persistent_application_state::DataOnDisk;

    #[test]
    fn test_berechne_depot_meta_infos_leere_db() {
        let result = berechne_depot_meta_infos(&generate_empty_database());
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_berechne_depot_meta_infos_keine_buchung() {
        let result =
            berechne_depot_meta_infos(&generate_database_with_sparkontos(vec![Sparkonto {
                kontotyp: Kontotyp::Depot,
                name: demo_name(),
            }]));

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, demo_name());
        assert_eq!(result[0].letzte_buchung, None);
        assert_eq!(result[0].letzter_depotauszug, None);
    }

    #[test]
    fn test_berechne_depot_meta_infos() {
        let auszug_datum = Datum::new(1, 1, 2020);
        let order_datum = Datum::new(2, 1, 2020);
        let database = &create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![Sparkonto {
                    kontotyp: Kontotyp::Depot,
                    name: demo_konto_referenz().konto_name,
                }],
                sparbuchungen: vec![],
                depotwerte: vec![],
                order: vec![Order {
                    datum: order_datum.clone(),
                    name: demo_name(),
                    konto: demo_konto_referenz(),
                    depotwert: demo_depotwert_referenz(),
                    wert: OrderBetrag::new(u_zwei(), OrderTyp::Kauf),
                }],
                order_dauerauftraege: vec![],
                depotauszuege: vec![Depotauszug {
                    konto: demo_konto_referenz(),
                    depotwert: demo_depotwert_referenz(),
                    wert: zwei(),
                    datum: auszug_datum.clone(),
                }],
            },
            any_datum(),
            demo_database_version(),
        );
        let result = berechne_depot_meta_infos(database);

        assert_eq!(result.len(), 1);
        assert_eq!(result[0].name, demo_konto_referenz().konto_name);
        assert_eq!(result[0].letzte_buchung, Some(order_datum));
        assert_eq!(result[0].letzter_depotauszug, Some(auszug_datum));
    }
}
