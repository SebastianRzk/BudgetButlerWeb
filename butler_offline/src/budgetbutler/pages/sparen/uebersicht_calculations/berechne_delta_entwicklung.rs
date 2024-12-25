use crate::model::metamodel::chart::{LineChart, LineChartDataSet};
use crate::model::primitives::farbe::aufbuchungen_farbe;

pub fn make_delta_entwicklung_from_gesamt_entwicklung(gesamt_entwicklung: &LineChart) -> LineChart {
    let mut result = vec![];

    for i in 0..gesamt_entwicklung.datasets[0].data.len() {
        result.push(
            gesamt_entwicklung.datasets[1].data[i].clone()
                - gesamt_entwicklung.datasets[0].data[i].clone(),
        );
    }

    LineChart {
        labels: gesamt_entwicklung.labels.clone(),
        datasets: vec![LineChartDataSet {
            label: "Delta Entwicklung".to_string(),
            data: result,
            farbe: aufbuchungen_farbe(),
        }],
    }
}

#[cfg(test)]
mod tests {
    use crate::model::metamodel::chart::{LineChart, LineChartDataSet};
    use crate::model::primitives::betrag::builder::{eins, fuenf, vier, zwei};
    use crate::model::primitives::farbe::green;
    use crate::model::primitives::name::Name;

    #[test]
    fn make_delta_entwicklung_from_gesamt_entwicklung() {
        let gesamt_entwicklung = LineChart {
            labels: vec![Name::new("2020".to_string())],
            datasets: vec![
                LineChartDataSet {
                    label: "Aufbuchungen".to_string(),
                    data: vec![zwei(), vier()],
                    farbe: green(),
                },
                LineChartDataSet {
                    label: "Vermoegen".to_string(),
                    data: vec![vier(), fuenf()],
                    farbe: green(),
                },
            ],
        };

        let result = super::make_delta_entwicklung_from_gesamt_entwicklung(&gesamt_entwicklung);

        assert_eq!(result.labels.len(), 1);
        assert_eq!(result.labels, vec![Name::new("2020".to_string())]);
        assert_eq!(result.datasets.len(), 1);
        assert_eq!(result.datasets[0].label, "Delta Entwicklung".to_string());
        assert_eq!(result.datasets[0].data.len(), 2);
        assert_eq!(result.datasets[0].data, vec![zwei(), eins()]);
    }
}
