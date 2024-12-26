use crate::budgetbutler::database::select::functions::filters::filter_bis_einschliesslich_jahr;
use crate::budgetbutler::pages::sparen::uebersicht_calculations::einnahmen_ausgaben_sparen::EinnahmenAusgabenSparen;
use crate::model::metamodel::chart::{LineChart, LineChartDataSet};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::farbe::{aufbuchungen_farbe, kontostand_farbe};
use crate::model::primitives::name::Name;
use crate::model::state::persistent_application_state::Database;

pub fn berechne_gesamt_entwicklung(
    data: &Vec<EinnahmenAusgabenSparen>,
    database: &Database,
) -> LineChart {
    let mut labels: Vec<Name> = vec![];
    let mut aufbuchungen: Vec<Betrag> = vec![];
    let mut konstostaende: Vec<Betrag> = vec![];

    let mut bisherige_sparen = Betrag::zero();

    for einnahmen_ausgaben_sparen in data {
        bisherige_sparen = bisherige_sparen + einnahmen_ausgaben_sparen.sparen.clone();
        labels.push(Name::new(format!("{}", einnahmen_ausgaben_sparen.jahr)));
        aufbuchungen.push(bisherige_sparen.abs());

        let kontostand_depot = database
            .depotauszuege
            .select()
            .filter(filter_bis_einschliesslich_jahr(
                einnahmen_ausgaben_sparen.jahr,
            ))
            .get_kombinierter_kontostand();

        let kontostand_sparkontos = database
            .sparbuchungen
            .select()
            .filter(filter_bis_einschliesslich_jahr(
                einnahmen_ausgaben_sparen.jahr,
            ))
            .map(|buchung| buchung.value.wert.positiv())
            .bilde_summe();
        konstostaende.push(kontostand_depot + kontostand_sparkontos);
    }

    LineChart {
        labels,
        datasets: vec![
            LineChartDataSet {
                label: "Aufbuchungen".to_string(),
                data: aufbuchungen,
                farbe: aufbuchungen_farbe(),
            },
            LineChartDataSet {
                label: "Vermögen".to_string(),
                data: konstostaende,
                farbe: kontostand_farbe(),
            },
        ],
    }
}

#[cfg(test)]
mod tests {
    use crate::budgetbutler::database::reader::reader::create_database;
    use crate::budgetbutler::pages::sparen::uebersicht_calculations::einnahmen_ausgaben_sparen::berechne_einnahmen_ausgaben_sparen;
    use crate::model::database::depotauszug::Depotauszug;
    use crate::model::database::depotwert::{Depotwert, DepotwertTyp};
    use crate::model::database::order::Order;
    use crate::model::database::sparbuchung::{Sparbuchung, SparbuchungTyp};
    use crate::model::database::sparkonto::{Kontotyp, Sparkonto};
    use crate::model::metamodel::jahr_range::JahrRange;
    use crate::model::primitives::betrag::builder::{fuenf, sieben, zehn};
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::{u_fuenf, u_zwei};
    use crate::model::primitives::datum::builder::demo_datum;
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::isin::builder::demo_isin;
    use crate::model::primitives::name::builder::demo_name;
    use crate::model::primitives::name::name;
    use crate::model::primitives::order_betrag::builder::kauf;
    use crate::model::state::persistent_application_state::builder::demo_database_version;
    use crate::model::state::persistent_application_state::{DataOnDisk, Database};

    #[test]
    fn test_berechne_gesamt_entwicklung() {
        let heute = demo_datum();
        let database = create_demo_database(heute.clone());

        let result = super::berechne_gesamt_entwicklung(
            &berechne_einnahmen_ausgaben_sparen(&JahrRange::new(heute.jahr, heute.jahr), &database),
            &database,
        );

        assert_eq!(result.labels.len(), 1);
        assert_eq!(result.labels[0], name("2024"));
        assert_eq!(result.datasets.len(), 2);

        let ausbuchungen = &result.datasets[0];
        assert_eq!(ausbuchungen.label, "Aufbuchungen");
        assert_eq!(ausbuchungen.data.len(), 1);
        assert_eq!(ausbuchungen.data[0], sieben());

        let vermoegen = &result.datasets[1];
        assert_eq!(vermoegen.label, "Vermögen");
        assert_eq!(vermoegen.data.len(), 1);
        assert_eq!(vermoegen.data[0], zehn());
    }

    fn create_demo_database(heute: Datum) -> Database {
        let sparkonto = Sparkonto {
            name: name("Mein Sparkonto"),
            kontotyp: Kontotyp::Sparkonto,
        };
        let depot = Sparkonto {
            name: name("Mein Depot"),
            kontotyp: Kontotyp::Depot,
        };
        let sparbuchung = Sparbuchung {
            datum: heute.clone(),
            name: demo_name(),
            wert: u_fuenf(),
            typ: SparbuchungTyp::ManuelleEinzahlung,
            konto: sparkonto.as_reference(),
        };

        let depotwert = Depotwert {
            name: demo_name(),
            isin: demo_isin(),
            typ: DepotwertTyp::ETF,
        };

        let order = Order {
            datum: heute.clone(),
            name: demo_name(),
            wert: kauf(u_zwei()),
            konto: depot.as_reference(),
            depotwert: depotwert.as_referenz(),
        };

        let depotauszug = Depotauszug {
            datum: heute,
            konto: depot.as_reference(),
            depotwert: depotwert.as_referenz(),
            wert: fuenf(),
        };

        let database = create_database(
            DataOnDisk {
                einzelbuchungen: vec![],
                dauerauftraege: vec![],
                gemeinsame_buchungen: vec![],
                sparkontos: vec![sparkonto, depot],
                sparbuchungen: vec![sparbuchung],
                depotwerte: vec![depotwert],
                order: vec![order],
                order_dauerauftraege: vec![],
                depotauszuege: vec![depotauszug],
            },
            Datum::first(),
            demo_database_version(),
        );
        database
    }
}
