use crate::model::primitives::datum::Datum;

pub fn calc_jahres_selektion(
    angefordertes_jahr: Option<i32>,
    verfuegbare_jahre: &Vec<i32>,
    today: Datum,
) -> i32 {
    let selektiertes_jahr;
    if let Some(jahr) = angefordertes_jahr {
        selektiertes_jahr = jahr;
    } else {
        if let Some(jahr) = verfuegbare_jahre.last() {
            selektiertes_jahr = jahr.clone();
        } else {
            selektiertes_jahr = today.jahr;
        }
    }
    selektiertes_jahr
}

#[cfg(test)]
mod tests {
    use super::calc_jahres_selektion;
    use crate::model::primitives::datum::Datum;

    #[test]
    fn test_calc_jahresselektion_mit_keinen_daten_should_selekt_this_year() {
        let result = calc_jahres_selektion(None, &vec![], Datum::new(1, 1, 2020));
        assert_eq!(result, 2020);
    }

    #[test]
    fn test_calc_jahresselektion_mit_daten_should_selekt_last_year() {
        let result = calc_jahres_selektion(None, &vec![2019], Datum::new(1, 1, 2020));
        assert_eq!(result, 2019);
    }

    #[test]
    fn test_calc_jahresselektion_mit_daten_should_selekt_requested_year() {
        let result = calc_jahres_selektion(Some(2018), &vec![2019], Datum::new(1, 1, 2020));
        assert_eq!(result, 2018);
    }
}
