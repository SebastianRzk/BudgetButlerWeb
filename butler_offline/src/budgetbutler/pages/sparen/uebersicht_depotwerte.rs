use crate::budgetbutler::database::sparen::depotwert_stand_berechner::berechne_aktuellen_depotwert_stand;
use crate::model::database::depotwert::Depotwert;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtDepotwerteContext<'a> {
    pub database: &'a Database,
}

pub struct UebersichtDepotwerteViewResult {
    pub depotwerte: Vec<DepotwerteMitKontostand>,
    pub gesamt: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
    pub database_version: DatabaseVersion,
}

pub struct DepotwerteMitKontostand {
    pub depotwert: Indiziert<Depotwert>,
    pub kontostand: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
}

pub fn handle_uebersicht_depotwerte(
    context: UebersichtDepotwerteContext,
) -> UebersichtDepotwerteViewResult {
    let mut konten = vec![];
    let mut gesamt = Betrag::zero();
    let mut aufbuchungen = Betrag::zero();
    let mut differenz = Betrag::zero();

    for depotwert in &context.database.depotwerte.depotwerte {
        let berechneter_depotwert_stand =
            berechne_aktuellen_depotwert_stand(depotwert.value.as_referenz(), &context.database);
        let einzeldifferenz = berechneter_depotwert_stand.letzter_kontostand.clone()
            - berechneter_depotwert_stand.gesamte_einzahlungen.clone();

        gesamt = gesamt + berechneter_depotwert_stand.letzter_kontostand.clone();
        aufbuchungen = aufbuchungen + berechneter_depotwert_stand.gesamte_einzahlungen.clone();
        differenz = differenz + einzeldifferenz.clone();

        konten.push(DepotwerteMitKontostand {
            depotwert: depotwert.clone(),
            kontostand: berechneter_depotwert_stand.letzter_kontostand,
            aufbuchungen: berechneter_depotwert_stand.gesamte_einzahlungen,
            differenz: einzeldifferenz,
        })
    }

    UebersichtDepotwerteViewResult {
        depotwerte: konten,
        gesamt,
        aufbuchungen,
        differenz,
        database_version: context.database.db_version.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::depotauszug::builder::depotauszug_with_konto_and_wert;
    use crate::model::database::depotwert::builder::any_depotwert;
    use crate::model::database::order::Order;
    use crate::model::database::order::OrderTyp::Kauf;
    use crate::model::database::sparkonto::builder::demo_konto;
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_vier;
    use crate::model::primitives::datum::builder::any_datum;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::order_betrag::OrderBetrag;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_depotwerte, generate_empty_database,
    };

    #[test]
    fn test_handle_uebersicht_depotwerte_empty() {
        let database = generate_database_with_depotwerte(vec![any_depotwert()]);
        let context = super::UebersichtDepotwerteContext {
            database: &database,
        };

        let result = super::handle_uebersicht_depotwerte(context);

        assert_eq!(result.depotwerte.len(), 1);
        assert_eq!(result.depotwerte[0].depotwert.value, any_depotwert());
        assert_eq!(result.depotwerte[0].kontostand, Betrag::zero());
        assert_eq!(result.depotwerte[0].aufbuchungen, Betrag::zero());
        assert_eq!(result.depotwerte[0].differenz, Betrag::zero());

        assert_eq!(result.gesamt, Betrag::zero());
        assert_eq!(result.aufbuchungen, Betrag::zero());
        assert_eq!(result.differenz, Betrag::zero());
        assert_eq!(result.database_version, database.db_version);
    }

    #[test]
    fn test_handle_uebersicht() {
        let database = generate_empty_database();
        let depotwerte = database.depotwerte.change().insert(any_depotwert());
        let depotauszuege =
            database
                .depotauszuege
                .change()
                .insert(depotauszug_with_konto_and_wert(
                    demo_konto().as_reference(),
                    any_depotwert().as_referenz(),
                    zwei(),
                ));
        let order = database.order.change().insert(Order {
            konto: demo_konto().as_reference(),
            depotwert: any_depotwert().as_referenz(),
            wert: OrderBetrag::new(u_vier(), Kauf),
            datum: any_datum(),
            name: demo_name(),
        });
        let database = generate_empty_database()
            .change_depotwerte(depotwerte)
            .change_order(order)
            .change_depotauszuege(depotauszuege);

        let context = super::UebersichtDepotwerteContext {
            database: &database,
        };

        let result = super::handle_uebersicht_depotwerte(context);

        assert_eq!(result.depotwerte.len(), 1);
        assert_eq!(result.depotwerte[0].kontostand, zwei());
        assert_eq!(result.depotwerte[0].aufbuchungen, vier());
        assert_eq!(result.depotwerte[0].differenz, minus_zwei());

        assert_eq!(result.gesamt, zwei());
        assert_eq!(result.aufbuchungen, vier());
        assert_eq!(result.differenz, minus_zwei());
        assert_eq!(result.database_version, database.db_version);
    }
}
