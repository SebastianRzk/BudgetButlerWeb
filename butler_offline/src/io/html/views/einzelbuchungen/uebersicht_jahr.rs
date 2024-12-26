use crate::budgetbutler::pages::einzelbuchungen::uebersicht_jahr::UebersichtJahrViewResult;
use crate::io::html::input::select::Select;
use crate::io::html::json::list::{JSONBetragList, JSONStringList};
use crate::io::html::views::templates::chart_templates::{
    map_bar_chart_to_template, map_buchung_kategorie, map_pie_chart, BarChartTemplate,
    BuchungKategorieTemplate, LineChartDataSetTemplate, LineChartTemplate, PieChartTemplate,
};
use crate::model::metamodel::chart::LineChartDataSet;
pub use askama::Template;

#[derive(Template)]
#[template(path = "einzelbuchungen/uebersicht_jahr.html")]
pub struct UebersichtJahrTemplate {
    pub jahre: Select<String>,
    pub selected_jahr: String,

    pub durchschnittlich_monat: BarChartTemplate,
    pub einnahmen_ausgaben: LineChartTemplate,

    pub einnahmen: LineChartTemplate,
    pub ausgaben: LineChartTemplate,

    pub zusammenfassung_ausgaben: Vec<BuchungKategorieTemplate>,
    pub zusammenfassung_einnahmen: Vec<BuchungKategorieTemplate>,

    pub gesamt_ausgaben: String,
    pub gesamt_einnahmen: String,

    pub pie_einnahmen: PieChartTemplate,
    pub pie_ausgaben: PieChartTemplate,
}

pub fn render_uebersicht_jahr_template(view_result: UebersichtJahrViewResult) -> String {
    let as_template: UebersichtJahrTemplate = map_to_template(view_result);
    as_template.render().unwrap()
}

fn map_line_chart_data_set(data_set: LineChartDataSet) -> LineChartDataSetTemplate {
    LineChartDataSetTemplate {
        label: data_set.label,
        data: JSONBetragList::new(data_set.data).to_string(),
        farbe: data_set.farbe.as_string,
    }
}

fn map_to_template(view_result: UebersichtJahrViewResult) -> UebersichtJahrTemplate {
    UebersichtJahrTemplate {
        jahre: Select::new(view_result.jahre, Some(view_result.selected_jahr.clone())),
        selected_jahr: view_result.selected_jahr,
        gesamt_ausgaben: view_result.gesamt_ausgaben.to_german_string(),
        gesamt_einnahmen: view_result.gesamt_einnahmen.to_german_string(),

        pie_ausgaben: map_pie_chart(view_result.pie_ausgaben),
        pie_einnahmen: map_pie_chart(view_result.pie_einnahmen),

        zusammenfassung_ausgaben: view_result
            .zusammenfassung_ausgaben
            .into_iter()
            .map(map_buchung_kategorie)
            .collect(),
        zusammenfassung_einnahmen: view_result
            .zusammenfassung_einnahmen
            .into_iter()
            .map(map_buchung_kategorie)
            .collect(),

        durchschnittlich_monat: map_bar_chart_to_template(view_result.durchschnittlich_monat),
        einnahmen: LineChartTemplate {
            labels: JSONStringList::new(
                view_result
                    .einnahmen
                    .labels
                    .iter()
                    .map(|x| x.name.clone())
                    .collect(),
            )
            .to_string(),
            datasets: view_result
                .einnahmen
                .datasets
                .into_iter()
                .map(map_line_chart_data_set)
                .collect(),
        },

        ausgaben: LineChartTemplate {
            labels: JSONStringList::new(
                view_result
                    .ausgaben
                    .labels
                    .iter()
                    .map(|x| x.name.clone())
                    .collect(),
            )
            .to_string(),
            datasets: view_result
                .ausgaben
                .datasets
                .into_iter()
                .map(map_line_chart_data_set)
                .collect(),
        },

        einnahmen_ausgaben: LineChartTemplate {
            labels: JSONStringList::new(
                view_result
                    .einnahmen_ausgaben
                    .labels
                    .iter()
                    .map(|x| x.name.clone())
                    .collect(),
            )
            .to_string(),
            datasets: view_result
                .einnahmen_ausgaben
                .datasets
                .into_iter()
                .map(map_line_chart_data_set)
                .collect(),
        },
    }
}

#[cfg(test)]
mod tests {}
