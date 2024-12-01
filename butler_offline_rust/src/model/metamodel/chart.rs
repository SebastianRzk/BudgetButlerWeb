use crate::model::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::MonatsName;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;

pub struct PieChart {
    pub labels: Vec<String>,
    pub data: Vec<Betrag>,
    pub colors: Vec<Farbe>,
}


pub struct MonatsZusammenfassung {
    pub monat: MonatsName,
    pub buchungen: Vec<Indiziert<Einzelbuchung>>,
}

pub struct AusgabeAusKategorie {
    pub color: Farbe,
    pub wert: Betrag,
    pub kategorie: Kategorie,
}


pub struct LineChart {
    pub labels: Vec<MonatsName>,
    pub datasets: Vec<LineChartDataSet>,
}

#[derive(Debug, PartialEq)]
pub struct LineChartDataSet {
    pub label: String,
    pub data: Vec<Betrag>,
    pub farbe: Farbe,
}


pub struct BarChart {
    pub labels: Vec<String>,
    pub datasets: Vec<Betrag>,
}
