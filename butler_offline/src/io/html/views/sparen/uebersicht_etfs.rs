use crate::budgetbutler::pages::sparen::uebersicht_etfs::{
    ETFKosten, EtfInfo, Tabelle, TabellenZeile, TabellenZelle, UebersichtEtfViewResult,
};
use crate::io::html::views::templates::chart_templates::{map_pie_chart, PieChartTemplate};
use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_etfs.html")]
pub struct UebersichtEtfsTemplate {
    etfs: Vec<EtfInfoTemplate>,
    kosten: ETFKostenUebersichtTemplate,
    regions_pie: PieChartTemplate,
    regionen: TabelleTemplate,
    sectors_pie: PieChartTemplate,
    sektoren: TabelleTemplate,
}

pub struct EtfInfoTemplate {
    pub name_lokal: String,
    pub name_global: String,
    pub isin: String,
    pub letzte_aktualisierung: String,
}

pub struct ETFKostenUebersichtTemplate {
    pub gesamt: ETFKostenTemplate,
    pub data: Vec<ETFKostenTemplate>,
}

pub struct ETFKostenTemplate {
    pub name: String,
    pub prozent: String,
    pub euro: String,
}

pub struct TabelleTemplate {
    pub header: Vec<String>,
    pub rows: Vec<TabellenZeileTemplate>,
}

#[derive(Clone)]
pub struct TabellenZeileTemplate {
    pub row_label: String,
    pub gesamt_column: TabellenZelleTemplate,
    pub other_columns: Vec<TabellenZelleTemplate>,
}

#[derive(Clone)]
pub struct TabellenZelleTemplate {
    pub euro: String,
    pub prozent: String,
}

pub fn render_uebersicht_etf_template(view_result: UebersichtEtfViewResult) -> String {
    let as_template: UebersichtEtfsTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_to_template(view_result: UebersichtEtfViewResult) -> UebersichtEtfsTemplate {
    UebersichtEtfsTemplate {
        etfs: view_result
            .etfs
            .iter()
            .map(|x| map_etf_to_template(x))
            .collect(),
        kosten: ETFKostenUebersichtTemplate {
            gesamt: map_etf_kosten_to_template(&view_result.etfkosten.gesamt),
            data: view_result
                .etfkosten
                .data
                .iter()
                .map(|x| map_etf_kosten_to_template(x))
                .collect(),
        },
        regions_pie: map_pie_chart(view_result.regionen_pie),
        regionen: map_tabelle_to_template(view_result.regionen),
        sectors_pie: map_pie_chart(view_result.sektoren_pie),
        sektoren: map_tabelle_to_template(view_result.sektoren),
    }
}

fn map_tabelle_to_template(tabelle_template: Tabelle) -> TabelleTemplate {
    TabelleTemplate {
        header: tabelle_template.header.clone(),
        rows: tabelle_template
            .rows
            .iter()
            .map(|x| map_tabellenzeile_to_template(x))
            .collect(),
    }
}

fn map_tabellenzeile_to_template(tabellen_zeile_template: &TabellenZeile) -> TabellenZeileTemplate {
    TabellenZeileTemplate {
        row_label: tabellen_zeile_template.row_label.clone(),
        gesamt_column: map_tabellenzelle_to_template(&tabellen_zeile_template.gesamt_column),
        other_columns: tabellen_zeile_template
            .other_columns
            .iter()
            .map(|x| map_tabellenzelle_to_template(x))
            .collect(),
    }
}

fn map_tabellenzelle_to_template(tabellen_zelle: &TabellenZelle) -> TabellenZelleTemplate {
    TabellenZelleTemplate {
        euro: tabellen_zelle.euro.to_german_string(),
        prozent: tabellen_zelle.prozent.als_halbwegs_gerundeter_string(),
    }
}

fn map_etf_kosten_to_template(etfkosten: &ETFKosten) -> ETFKostenTemplate {
    ETFKostenTemplate {
        name: etfkosten.name.clone(),
        prozent: etfkosten.prozent.als_halbwegs_gerundeter_string(),
        euro: etfkosten.euro.to_german_string(),
    }
}

fn map_etf_to_template(info: &EtfInfo) -> EtfInfoTemplate {
    EtfInfoTemplate {
        name_lokal: info.name_lokal.clone(),
        name_global: info.name_global.clone(),
        isin: info.isin.isin.to_string(),
        letzte_aktualisierung: info.letzte_aktualisierung.clone(),
    }
}

#[cfg(test)]
mod tests {}
