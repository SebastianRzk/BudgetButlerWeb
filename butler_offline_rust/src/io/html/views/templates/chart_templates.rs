use crate::io::html::json::list::{JSONBetragList, JSONStringList};
use crate::model::metamodel::chart::{AusgabeAusKategorie, PieChart};

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


pub fn map_buchung_kategorie(ausgabe_aus_kategorie: AusgabeAusKategorie) -> BuchungKategorieTemplate{
    BuchungKategorieTemplate {
        color: ausgabe_aus_kategorie.color.as_string,
        wert: ausgabe_aus_kategorie.wert.to_german_string(),
        kategorie: ausgabe_aus_kategorie.kategorie.kategorie,
    }
}

pub fn map_pie_chart(pie_chart: PieChart)-> PieChartTemplate {
    PieChartTemplate {
        labels: JSONStringList::new(pie_chart.labels).to_string(),
        data: JSONBetragList::new(pie_chart.data).to_string(),
        colors: JSONStringList::new(pie_chart.colors.into_iter().map(|x| x.as_string).collect()).to_string(),
    }
}
