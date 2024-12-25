use crate::io::html::json::list::{JSONBetragList, JSONStringList};
use crate::model::metamodel::chart::{AusgabeAusKategorie, BarChart, LineChart, PieChart};

pub struct BuchungKategorieTemplate {
    pub color: String,
    pub wert: String,
    pub kategorie: String,
}

pub struct PieChartTemplate {
    pub labels: String,
    pub data: String,
    pub colors: String,
}

pub struct BarChartTemplate {
    pub labels: String,
    pub datasets: String,
}

pub struct LineChartTemplate {
    pub labels: String,
    pub datasets: Vec<LineChartDataSetTemplate>,
}

pub struct LineChartDataSetTemplate {
    pub label: String,
    pub data: String,
    pub farbe: String,
}

pub fn map_buchung_kategorie(
    ausgabe_aus_kategorie: AusgabeAusKategorie,
) -> BuchungKategorieTemplate {
    BuchungKategorieTemplate {
        color: ausgabe_aus_kategorie.color.as_string,
        wert: ausgabe_aus_kategorie.wert.to_german_string(),
        kategorie: ausgabe_aus_kategorie.kategorie.kategorie,
    }
}

pub fn map_pie_chart(pie_chart: PieChart) -> PieChartTemplate {
    PieChartTemplate {
        labels: JSONStringList::new(pie_chart.labels).to_string(),
        data: JSONBetragList::new(pie_chart.data).to_string(),
        colors: JSONStringList::new(pie_chart.colors.into_iter().map(|x| x.as_string).collect())
            .to_string(),
    }
}

pub fn map_bar_chart_to_template(bar_chart: BarChart) -> BarChartTemplate {
    BarChartTemplate {
        labels: JSONStringList::new(bar_chart.labels.iter().map(|x| x.name.clone()).collect())
            .to_string(),
        datasets: JSONBetragList::new(bar_chart.datasets).to_string(),
    }
}

pub fn map_to_linechart_template(line_chart: &LineChart) -> LineChartTemplate {
    LineChartTemplate {
        labels: JSONStringList::new(line_chart.labels.iter().map(|n| n.name.clone()).collect())
            .to_string(),
        datasets: line_chart
            .datasets
            .iter()
            .map(|x| LineChartDataSetTemplate {
                label: x.label.clone(),
                data: JSONBetragList::new(x.data.clone()).to_string(),
                farbe: x.farbe.as_string.clone(),
            })
            .collect(),
    }
}
