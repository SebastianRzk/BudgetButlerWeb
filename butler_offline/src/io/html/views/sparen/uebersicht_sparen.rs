use crate::budgetbutler::pages::sparen::uebersicht_sparen::UebersichtSparenViewResult;
use crate::io::disk::primitive::sparkontotyp::write_sparkontotyp;
use crate::io::html::json::list::{JSONBetragList, JSONStringList};
use crate::io::html::views::templates::chart_templates::{
    map_bar_chart_to_template, map_pie_chart, map_to_linechart_template, BarChartTemplate,
    LineChartTemplate, PieChartTemplate,
};
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::Datum;
pub use askama::Template;

#[derive(Template)]
#[template(path = "sparen/uebersicht_sparen.html")]
pub struct UebersichtSparenTemplate {
    pub einnahmen_ausgaben_sparen: EinnahmenAusgabenSparenTemplate,
    pub gesamt_entwicklung: LineChartTemplate,
    pub gesamt_entwicklung_delta: LineChartTemplate,
    pub gesamt_entwicklung_delta_jahr: BarChartTemplate,
    pub depot_metainfos: Vec<DepotMetaInfoTemplate>,
    pub uebersicht_kontos: UebersichtKontosTemplate,
    pub uebersicht_kontos_pie: PieChartTemplate,
    pub anlagetypen: Vec<AnlagetypTemplate>,
    pub anlagetypen_gesamt: AnlagetypTemplate,
    pub anlagetypen_pie: PieChartTemplate,
    pub order_typen: OrderTypenTemplate,
    pub order_typen_pie: PieChartTemplate,
    pub aktuelle_dauerauftraege: Vec<OrderDauerauftragAbstractTemplate>,
    pub aktuelle_dauerauftrege_pie: PieChartTemplate,
}

pub struct EinnahmenAusgabenSparenTemplate {
    pub einnahmen: JSONBetragList,
    pub ausgaben: JSONBetragList,
    pub sparen: JSONBetragList,
    pub labels: JSONStringList,
}

pub struct OrderDauerauftragAbstractTemplate {
    pub color: String,
    pub name: String,
    pub wert: String,
    pub depotwert: String,
}

pub struct DepotMetaInfoTemplate {
    pub name: String,
    pub letzte_buchung: String,
    pub warning: bool,
    pub letzter_depotauszug: String,
}

pub struct UebersichtKontosTemplate {
    pub konten: Vec<SparkontoMitFarbeTemplate>,
    pub gesamt: String,
    pub aufbuchungen: String,
    pub difference: String,
    pub difference_is_negativ: bool,
}

pub struct SparkontoMitFarbeTemplate {
    pub color: String,
    pub kontoname: String,
    pub kontotyp: String,
    pub aufbuchungen: String,
    pub difference: String,
    pub difference_is_negativ: bool,
    pub wert: String,
}

pub struct AnlagetypTemplate {
    pub color: String,
    pub name: String,
    pub gesamte_einzahlungen: String,
    pub difference: String,
    pub difference_is_negativ: bool,
    pub kontostand: String,
}

pub struct OrderTypenTemplate {
    pub gesamt_dynamisch: String,
    pub gesamt_statisch: String,
}

pub fn render_uebersicht_sparen_template(view_result: UebersichtSparenViewResult) -> String {
    let as_template: UebersichtSparenTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_to_template(view_result: UebersichtSparenViewResult) -> UebersichtSparenTemplate {
    let diff = sum_to_german_string(
        view_result
            .anlagetypen
            .iter()
            .map(|a| a.differenz.clone())
            .collect(),
    );
    let anlagetypen_gesamt = AnlagetypTemplate {
        color: "black".to_string(),
        name: "Gesamt".to_string(),
        gesamte_einzahlungen: sum_to_german_string(
            view_result
                .anlagetypen
                .iter()
                .map(|a| a.gesamte_einzahlungen.clone())
                .collect(),
        ),
        difference_is_negativ: diff.starts_with("-"),
        difference: diff,
        kontostand: sum_to_german_string(
            view_result
                .anlagetypen
                .iter()
                .map(|a| a.kontostand.clone())
                .collect(),
        ),
    };
    UebersichtSparenTemplate {
        einnahmen_ausgaben_sparen: EinnahmenAusgabenSparenTemplate {
            einnahmen: JSONBetragList::new(
                view_result
                    .einnahmen_ausgaben_sparen
                    .iter()
                    .map(|e| e.einnahmen.clone())
                    .collect(),
            ),
            ausgaben: JSONBetragList::new(
                view_result
                    .einnahmen_ausgaben_sparen
                    .iter()
                    .map(|e| e.ausgaben.abs())
                    .collect(),
            ),
            sparen: JSONBetragList::new(
                view_result
                    .einnahmen_ausgaben_sparen
                    .iter()
                    .map(|e| e.sparen.abs())
                    .collect(),
            ),
            labels: JSONStringList::new(
                view_result
                    .einnahmen_ausgaben_sparen
                    .iter()
                    .map(|e| format!("{}", e.jahr))
                    .collect(),
            ),
        },
        gesamt_entwicklung: map_to_linechart_template(&view_result.gesamt_entwicklung),
        gesamt_entwicklung_delta: map_to_linechart_template(&view_result.gesamt_entwicklung_delta),
        gesamt_entwicklung_delta_jahr: map_bar_chart_to_template(
            view_result.gesamt_entwicklung_delta_jahr,
        ),
        depot_metainfos: view_result
            .depot_metainfos
            .iter()
            .map(|d| DepotMetaInfoTemplate {
                name: d.name.name.clone(),
                letzte_buchung: optional_datum(&d.letzte_buchung),
                warning: is_warning(&d.letzte_buchung, &d.letzter_depotauszug),
                letzter_depotauszug: optional_datum(&d.letzter_depotauszug),
            })
            .collect(),
        uebersicht_kontos: UebersichtKontosTemplate {
            konten: view_result
                .uebersicht_kontos
                .konten
                .iter()
                .map(|k| SparkontoMitFarbeTemplate {
                    kontoname: k.konto.value.name.name.clone(),
                    kontotyp: write_sparkontotyp(k.konto.value.kontotyp.clone()).element,
                    aufbuchungen: k.aufbuchungen.to_german_string(),
                    difference: k.differenz.to_german_string(),
                    difference_is_negativ: k.differenz.is_negativ(),
                    wert: k.kontostand.to_german_string(),
                    color: k.farbe.as_string.clone(),
                })
                .collect(),
            gesamt: view_result.uebersicht_kontos.gesamt.to_german_string(),
            aufbuchungen: view_result
                .uebersicht_kontos
                .aufbuchungen
                .to_german_string(),
            difference_is_negativ: view_result.uebersicht_kontos.differenz.is_negativ(),
            difference: view_result.uebersicht_kontos.differenz.to_german_string(),
        },
        uebersicht_kontos_pie: map_pie_chart(view_result.uebersicht_kontos_pie.clone()),
        anlagetypen: view_result
            .anlagetypen
            .iter()
            .map(|a| AnlagetypTemplate {
                color: a.farbe.as_string.clone(),
                name: a.name.clone(),
                gesamte_einzahlungen: a.gesamte_einzahlungen.to_german_string(),
                difference: a.differenz.to_german_string(),
                difference_is_negativ: a.differenz.is_negativ(),
                kontostand: a.kontostand.to_german_string(),
            })
            .collect(),
        anlagetypen_gesamt: anlagetypen_gesamt,
        anlagetypen_pie: map_pie_chart(view_result.anlagetypen_pie.clone()),
        order_typen: OrderTypenTemplate {
            gesamt_dynamisch: view_result.order_typen.gesamt_dynamisch.to_german_string(),
            gesamt_statisch: view_result.order_typen.gesamt_statisch.to_german_string(),
        },
        order_typen_pie: map_pie_chart(view_result.order_typen_pie.clone()),
        aktuelle_dauerauftraege: view_result
            .aktuelle_dauerauftraege
            .iter()
            .map(|a| OrderDauerauftragAbstractTemplate {
                color: a.farbe.as_string.clone(),
                depotwert: a.depotwert_beschreibung.clone(),
                name: a.name.name.clone(),
                wert: a.wert.get_realer_wert().to_german_string(),
            })
            .collect(),
        aktuelle_dauerauftrege_pie: map_pie_chart(view_result.aktuelle_dauerauftrege_pie.clone()),
    }
}

fn sum_to_german_string(betrag_list: Vec<Betrag>) -> String {
    betrag_list
        .into_iter()
        .reduce(|x, y| x + y)
        .unwrap_or(Betrag::zero())
        .to_german_string()
}

fn optional_datum(d: &Option<Datum>) -> String {
    d.clone()
        .map(|dd| dd.to_german_string())
        .unwrap_or("Noch nichts erfasst".to_string())
}

fn is_warning(letzte_erfassung: &Option<Datum>, letzter_depotauszug: &Option<Datum>) -> bool {
    let letzte_erfassung = letzte_erfassung.clone().unwrap_or(Datum::new(0, 0, 0));
    let letzter_depotauszug = letzter_depotauszug.clone().unwrap_or(Datum::new(0, 0, 0));
    letzte_erfassung > letzter_depotauszug
}

#[cfg(test)]
mod tests {}
