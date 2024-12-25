use crate::budgetbutler::database::sparen::depotwert_stand_berechner::berechne_aktuellen_depotwert_stand;
use crate::budgetbutler::pages::sparen::etf_calculations::berechne_kostenuebersicht::berechne_kostenuebersicht;
use crate::budgetbutler::pages::sparen::etf_calculations::berechne_regionen::berechne_regionen;
use crate::budgetbutler::pages::sparen::etf_calculations::berechne_sektoren::berechne_sektoren;
use crate::budgetbutler::pages::sparen::etf_calculations::make_pie_from_table::make_pie;
use crate::model::database::depotwert::Depotwert;
use crate::model::metamodel::chart::PieChart;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
use crate::model::primitives::isin::ISIN;
use crate::model::primitives::prozent::Prozent;
use crate::model::shares::{ShareData, ShareState};
use crate::model::state::persistent_application_state::Database;

pub struct UebersichtEtfContext<'a> {
    pub database: &'a Database,
    pub shares: &'a ShareState,
}

pub struct UebersichtEtfViewResult {
    pub etfs: Vec<EtfInfo>,
    pub etfkosten: ETFKostenUebersicht,
    pub sektoren_pie: PieChart,
    pub sektoren: Tabelle,
    pub regionen_pie: PieChart,
    pub regionen: Tabelle,
}

pub struct EtfInfo {
    pub name_lokal: String,
    pub name_global: String,
    pub isin: ISIN,
    pub letzte_aktualisierung: String,
}

pub struct ETFKostenUebersicht {
    pub gesamt: ETFKosten,
    pub data: Vec<ETFKosten>,
}

pub struct ETFKosten {
    pub name: String,
    pub prozent: Prozent,
    pub euro: Betrag,
}

pub struct DepotwertMitDaten {
    pub depotwert: Depotwert,
    pub data: ShareData,
    pub aktueller_kontostand: Betrag,
}

pub struct Tabelle {
    pub header: Vec<String>,
    pub rows: Vec<TabellenZeile>,
}

#[derive(Clone)]
pub struct TabellenZeile {
    pub row_label: String,
    pub gesamt_column: TabellenZelle,
    pub other_columns: Vec<TabellenZelle>,
}

#[derive(Clone)]
pub struct TabellenZelle {
    pub euro: Betrag,
    pub prozent: Prozent,
}

pub fn handle_uebersicht_etf(context: UebersichtEtfContext) -> UebersichtEtfViewResult {
    let mut depotwerte_mit_daten = vec![];
    let mut etfs = vec![];

    for depotwert in context.database.depotwerte.depotwerte.iter() {
        let isin = depotwert.value.isin.clone();
        let share = context.shares.get_share(isin);
        let aktueller_kontostand =
            berechne_aktuellen_depotwert_stand(depotwert.value.as_referenz(), &context.database);

        if let Some(data) = share {
            depotwerte_mit_daten.push(DepotwertMitDaten {
                depotwert: depotwert.value.clone(),
                data: data.clone(),
                aktueller_kontostand: aktueller_kontostand.letzter_kontostand,
            });
            etfs.push(EtfInfo {
                name_lokal: depotwert.value.name.name.clone(),
                name_global: data.data.name.clone(),
                isin: depotwert.value.isin.clone(),
                letzte_aktualisierung: Datum::from_german_string(&data.date).to_german_string(),
            });
        } else {
            etfs.push(EtfInfo {
                name_lokal: depotwert.value.name.name.clone(),
                name_global: "Unbekannt".to_string(),
                isin: depotwert.value.isin.clone(),
                letzte_aktualisierung: "Noch nie".to_string(),
            });
        }
    }

    depotwerte_mit_daten.sort_by(|a, b| b.aktueller_kontostand.cmp(&a.aktueller_kontostand));

    let gesamt_summe = depotwerte_mit_daten
        .iter()
        .map(|x| x.aktueller_kontostand.clone())
        .reduce(|a, b| a + b)
        .unwrap_or(Betrag::zero());

    let sektoren = berechne_sektoren(&depotwerte_mit_daten, gesamt_summe.clone());
    let regionen = berechne_regionen(&depotwerte_mit_daten, gesamt_summe.clone());

    UebersichtEtfViewResult {
        etfs,
        etfkosten: berechne_kostenuebersicht(&depotwerte_mit_daten, gesamt_summe),
        sektoren_pie: make_pie(&sektoren),
        sektoren,
        regionen_pie: make_pie(&regionen),
        regionen,
    }
}

#[cfg(test)]
mod tests {}
