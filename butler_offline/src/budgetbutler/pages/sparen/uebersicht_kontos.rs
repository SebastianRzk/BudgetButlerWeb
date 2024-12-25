use crate::budgetbutler::database::sparen::kontostand_berechner::berechne_aktuellen_kontostand;
use crate::model::database::sparkonto::Sparkonto;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::DatabaseVersion;

pub struct UebersichtKontosContext<'a> {
    pub database: &'a Database,
}

pub struct UebersichtKontosViewResult {
    pub konten: Vec<KontoMitKontostand>,
    pub gesamt: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
    pub database_version: DatabaseVersion,
}

pub struct KontoMitKontostand {
    pub konto: Indiziert<Sparkonto>,
    pub kontostand: Betrag,
    pub aufbuchungen: Betrag,
    pub differenz: Betrag,
}

pub fn handle_uebersicht_kontos(context: UebersichtKontosContext) -> UebersichtKontosViewResult {
    let mut konten = vec![];
    let mut gesamt = Betrag::zero();
    let mut aufbuchungen = Betrag::zero();
    let mut differenz = Betrag::zero();

    for konto in &context.database.sparkontos.sparkontos {
        let berechneter_kontostand =
            berechne_aktuellen_kontostand(konto.value.clone(), &context.database);
        let einzeldifferenz = berechneter_kontostand.letzter_kontostand.clone()
            - berechneter_kontostand.gesamte_einzahlungen.clone();

        gesamt = gesamt + berechneter_kontostand.letzter_kontostand.clone();
        aufbuchungen = aufbuchungen + berechneter_kontostand.gesamte_einzahlungen.clone();
        differenz = differenz + einzeldifferenz.clone();

        konten.push(KontoMitKontostand {
            konto: konto.clone(),
            kontostand: berechneter_kontostand.letzter_kontostand,
            aufbuchungen: berechneter_kontostand.gesamte_einzahlungen,
            differenz: einzeldifferenz,
        })
    }

    UebersichtKontosViewResult {
        konten,
        gesamt,
        aufbuchungen,
        differenz,
        database_version: context.database.db_version.clone(),
    }
}

#[cfg(test)]
mod tests {
    use crate::model::database::sparbuchung::builder::sparbuchung_with_betrag_typ_und_konto;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::database::sparkonto::builder::{any_konto_with_typ, demo_konto};
    use crate::model::database::sparkonto::Kontotyp;
    use crate::model::primitives::betrag::builder::zwei;
    use crate::model::primitives::betrag::Betrag;
    use crate::model::primitives::betrag_ohne_vorzeichen::builder::u_zwei;
    use crate::model::state::persistent_application_state::builder::{
        generate_database_with_sparkontos, generate_database_with_sparkontos_und_sparbuchungen,
    };

    #[test]
    fn test_handle_uebersicht_kontos_empty() {
        let database = generate_database_with_sparkontos(vec![demo_konto()]);
        let context = super::UebersichtKontosContext {
            database: &database,
        };

        let result = super::handle_uebersicht_kontos(context);

        assert_eq!(result.konten.len(), 1);
        assert_eq!(result.konten[0].konto.value, demo_konto());
        assert_eq!(result.konten[0].kontostand, Betrag::zero());
        assert_eq!(result.konten[0].aufbuchungen, Betrag::zero());
        assert_eq!(result.konten[0].differenz, Betrag::zero());

        assert_eq!(result.gesamt, Betrag::zero());
        assert_eq!(result.aufbuchungen, Betrag::zero());
        assert_eq!(result.differenz, Betrag::zero());
        assert_eq!(result.database_version, database.db_version);
    }

    #[test]
    fn test_handle_uebersicht() {
        let database = generate_database_with_sparkontos_und_sparbuchungen(
            vec![any_konto_with_typ(Kontotyp::Sparkonto)],
            vec![sparbuchung_with_betrag_typ_und_konto(
                u_zwei(),
                SparbuchungTyp::ManuelleEinzahlung,
                demo_konto().as_reference(),
            )],
        );
        let context = super::UebersichtKontosContext {
            database: &database,
        };

        let result = super::handle_uebersicht_kontos(context);

        assert_eq!(result.konten.len(), 1);
        assert_eq!(result.konten[0].kontostand, zwei());
        assert_eq!(result.konten[0].aufbuchungen, zwei());
        assert_eq!(result.konten[0].differenz, Betrag::zero());

        assert_eq!(result.gesamt, zwei());
        assert_eq!(result.aufbuchungen, zwei());
        assert_eq!(result.differenz, Betrag::zero());
        assert_eq!(result.database_version, database.db_version);
    }
}
