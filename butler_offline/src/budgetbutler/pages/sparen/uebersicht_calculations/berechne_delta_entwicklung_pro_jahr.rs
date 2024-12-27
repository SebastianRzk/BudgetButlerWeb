use crate::model::metamodel::chart::{BarChart, LineChart};

pub fn make_delta_entwicklung_pro_jahr_from_delta_entwicklung(
    gesamt_entwicklung: &LineChart,
) -> BarChart {
    let mut result = vec![];

    for i in 0..gesamt_entwicklung.datasets[0].data.len() {
        if i == 0 {
            result.push(gesamt_entwicklung.datasets[0].data[i].clone());
            continue;
        }
        result.push(
            gesamt_entwicklung.datasets[0].data[i].clone()
                - gesamt_entwicklung.datasets[0].data[i - 1].clone(),
        );
    }

    BarChart {
        labels: gesamt_entwicklung.labels.clone(),
        datasets: result,
    }
}

#[cfg(test)]
mod tests {
    use crate::model::metamodel::chart::{LineChart, LineChartDataSet};
    use crate::model::primitives::betrag::builder::{vier, zwei};
    use crate::model::primitives::farbe::green;
    use crate::model::primitives::name::Name;

    #[test]
    fn test_make_delta_entwicklung_pro_jahr_from_delta_entwicklung() {
        let labels = vec![Name::new("2020".to_string())];
        let gesamt_entwicklung = LineChart {
            labels: labels.clone(),
            datasets: vec![LineChartDataSet {
                label: "Delta".to_string(),
                data: vec![zwei(), vier()],
                farbe: green(),
            }],
        };

        let result =
            super::make_delta_entwicklung_pro_jahr_from_delta_entwicklung(&gesamt_entwicklung);

        assert_eq!(result.labels.len(), 1);
        assert_eq!(result.labels, labels);
        assert_eq!(result.datasets.len(), 2);
        assert_eq!(result.datasets, vec![zwei(), zwei()]);
    }
}
