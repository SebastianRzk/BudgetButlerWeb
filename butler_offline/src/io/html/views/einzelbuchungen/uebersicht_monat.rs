use crate::budgetbutler::pages::einzelbuchungen::uebersicht_monat::{
    Buchung, PlusMinusChart, Tag, UebersichtMonatViewResult,
};
use crate::io::html::input::select::Select;
use crate::io::html::views::templates::chart_templates::{
    map_buchung_kategorie, map_pie_chart, BuchungKategorieTemplate, PieChartTemplate,
};
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/uebersicht_monat.html")]
pub struct UebersichtMonatTemplate {
    pub monate: Select<String>,
    pub selected_date: String,
    pub selected_year: String,

    pub monat_chart: PlusMinusChartTemplate,
    pub jahr_chart: PlusMinusChartTemplate,

    pub ausgaben_chart: PieChartTemplate,
    pub einnahmen_chart: PieChartTemplate,

    pub ausgaben: Vec<BuchungKategorieTemplate>,
    pub einnahmen: Vec<BuchungKategorieTemplate>,

    pub gesamt: String,
    pub gesamt_einnahmen: String,

    pub zusammenfassung: Vec<TagTemplate>,
}

pub struct PlusMinusChartTemplate {
    pub name_uebersicht_gruppe_1: String,
    pub name_uebersicht_gruppe_2: String,

    pub color_uebersicht_gruppe_1: String,
    pub color_uebersicht_gruppe_2: String,

    pub wert_uebersicht_gruppe_1: String,
    pub wert_uebersicht_gruppe_2: String,
}

pub struct TagTemplate {
    pub name: String,
    pub items: Vec<BuchungTemplate>,
}

pub struct BuchungTemplate {
    pub color: String,
    pub name: String,
    pub wert: String,
    pub kategorie: String,
}

pub fn render_uebersicht_monat_template(view_result: UebersichtMonatViewResult) -> String {
    let as_template: UebersichtMonatTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_plus_minus_chart(chart: PlusMinusChart) -> PlusMinusChartTemplate {
    PlusMinusChartTemplate {
        name_uebersicht_gruppe_1: chart.name_uebersicht_gruppe_1,
        name_uebersicht_gruppe_2: chart.name_uebersicht_gruppe_2,

        color_uebersicht_gruppe_1: chart.color_uebersicht_gruppe_1.as_string,
        color_uebersicht_gruppe_2: chart.color_uebersicht_gruppe_2.as_string,

        wert_uebersicht_gruppe_1: chart.wert_uebersicht_gruppe_1.to_iso_string(),
        wert_uebersicht_gruppe_2: chart.wert_uebersicht_gruppe_2.to_iso_string(),
    }
}

fn map_to_tag_template(tag: Tag) -> TagTemplate {
    TagTemplate {
        name: tag.name,
        items: tag.items.into_iter().map(map_to_buchung_template).collect(),
    }
}

fn map_to_buchung_template(buchung: Buchung) -> BuchungTemplate {
    BuchungTemplate {
        color: buchung.color.as_string,
        name: buchung.name.to_string(),
        wert: buchung.wert.to_german_string(),
        kategorie: buchung.kategorie.kategorie,
    }
}

fn map_to_template(view_result: UebersichtMonatViewResult) -> UebersichtMonatTemplate {
    UebersichtMonatTemplate {
        monate: Select::new(view_result.monate, Some(view_result.selected_date.clone())),
        selected_date: view_result.selected_date,
        selected_year: view_result.selected_year,

        monat_chart: map_plus_minus_chart(view_result.monat_chart),

        jahr_chart: map_plus_minus_chart(view_result.jahr_chart),

        ausgaben_chart: map_pie_chart(view_result.ausgaben_chart),

        einnahmen_chart: map_pie_chart(view_result.einnahmen_chart),

        ausgaben: view_result
            .ausgaben
            .into_iter()
            .map(map_buchung_kategorie)
            .collect(),
        einnahmen: view_result
            .einnahmen
            .into_iter()
            .map(map_buchung_kategorie)
            .collect(),

        gesamt: view_result.gesamt_ausgaben.to_german_string(),
        gesamt_einnahmen: view_result.gesamt_einnahmen.to_german_string(),

        zusammenfassung: view_result
            .zusammenfassung
            .into_iter()
            .map(map_to_tag_template)
            .collect(),
    }
}

#[cfg(test)]
mod tests {
    //todo: test
}
