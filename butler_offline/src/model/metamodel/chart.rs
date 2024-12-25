use crate::model::database::einzelbuchung::Einzelbuchung;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag::Betrag;
use crate::model::primitives::datum::MonatsName;
use crate::model::primitives::farbe::Farbe;
use crate::model::primitives::kategorie::Kategorie;
use crate::model::primitives::name::Name;

#[derive(Debug, Clone)]
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
    pub labels: Vec<Name>,
    pub datasets: Vec<LineChartDataSet>,
}

#[derive(Debug, PartialEq)]
pub struct LineChartDataSet {
    pub label: String,
    pub data: Vec<Betrag>,
    pub farbe: Farbe,
}

pub struct BarChart {
    pub labels: Vec<Name>,
    pub datasets: Vec<Betrag>,
}
