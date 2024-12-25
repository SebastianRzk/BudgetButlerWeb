use crate::model::database::depotwert::DepotwertReferenz;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;
use std::collections::HashMap;

pub struct Kontostand {
    pub letzter_kontostand: Betrag,
    pub gesamte_einzahlungen: Betrag,
}

pub fn berechne_aktuellen_depotwert_stand(
    depotwert: DepotwertReferenz,
    database: &Database,
) -> Kontostand {
    Kontostand {
        letzter_kontostand: berechne_kontostand(depotwert.clone(), database),
        gesamte_einzahlungen: berechne_einzahlungen(depotwert, database),
    }
}

fn berechne_kontostand(depotwert: DepotwertReferenz, database: &Database) -> Betrag {
    let mut konto_map = HashMap::new();
    let auszuege = database
        .depotauszuege
        .select()
        .filter(|k| k.value.depotwert.isin == depotwert.isin)
        .collect();
    for auszug in auszuege {
        konto_map.insert(auszug.value.konto.konto_name.name, auszug.value.wert);
    }
    konto_map
        .values()
        .into_iter()
        .map(|x| x.clone())
        .reduce(|a, b| a + b)
        .unwrap_or_else(Betrag::zero)
}

fn berechne_einzahlungen(depotwert: DepotwertReferenz, database: &Database) -> Betrag {
    let mut gesamte_einzahlungen = Betrag::zero();

    for order in database
        .order
        .select()
        .filter(|order| order.value.depotwert.isin == depotwert.isin)
        .collect()
    {
        gesamte_einzahlungen =
            gesamte_einzahlungen + order.value.wert.get_betrag_fuer_geleistete_investition();
    }

    gesamte_einzahlungen
}

#[cfg(test)]
mod tests_fuer_depot {
    use crate::model::database::depotauszug::builder::depotauszug_with_konto_and_wert;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::builder::{demo_konto_referenz, konto_referenz};
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_vier;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotauszuege, generate_database_with_orders,
        generate_empty_database,
    };

    #[test]
    fn test_berechne_kontostand_fuer_leere_db() {
        let result = super::berechne_aktuellen_depotwert_stand(
            any_depotwert().as_referenz(),
            &generate_empty_database(),
        );

        assert_eq!(result.letzter_kontostand, Betrag::zero());
        assert_eq!(result.gesamte_einzahlungen, Betrag::zero());
    }

    #[test]
    fn test_berechne_einzahlungen() {
        let depotwert = any_depotwert();
        let order = Order {
            wert: OrderBetrag::new(u_vier(), crate::model::database::order::OrderTyp::Kauf),
            depotwert: depotwert.as_referenz(),
            konto: demo_konto_referenz(),
            name: demo_name(),
            datum: any_datum(),
        };

        let database = generate_database_with_orders(vec![order.clone()]);

        let result = super::berechne_aktuellen_depotwert_stand(depotwert.as_referenz(), &database);
        assert_eq!(result.gesamte_einzahlungen, vier());
        assert_eq!(result.letzter_kontostand, Betrag::zero());
    }

    #[test]
    fn test_kontostand() {
        let depotauszug1 = depotauszug_with_konto_and_wert(
            demo_konto().as_reference(),
            any_depotwert().as_referenz(),
            vier(),
        );
        let depotauszug2 = depotauszug_with_konto_and_wert(
            konto_referenz("asdasd"),
            any_depotwert().as_referenz(),
            zwei(),
        );

        let database = generate_database_with_depotauszuege(vec![depotauszug1, depotauszug2]);

        let result =
            super::berechne_aktuellen_depotwert_stand(any_depotwert().as_referenz(), &database);

        assert_eq!(result.gesamte_einzahlungen, Betrag::zero());
        assert_eq!(
            result.letzter_kontostand,
            Betrag::new(Vorzeichen::Positiv, 6, 0)
        );
    }
}
