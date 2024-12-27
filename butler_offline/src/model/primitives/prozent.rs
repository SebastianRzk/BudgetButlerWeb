use crate::model::primitives::betrag::Betrag;

#[derive(Debug, Clone, PartialEq)]
pub struct Prozent {
    pub int_representation: Option<u32>,
    pub float_representation: Option<f64>,
}

impl Prozent {
    pub fn as_string(&self) -> String {
        if let Some(int_representation) = self.int_representation {
            int_representation.to_string()
        } else if let Some(float_representation) = self.float_representation {
            float_representation.to_string()
        } else {
            "".to_string()
        }
    }

    pub fn from_int_representation(int_representation: u32) -> Prozent {
        Prozent {
            int_representation: Some(int_representation),
            float_representation: None,
        }
    }

    pub fn from_float_representation(float_representation: f64) -> Prozent {
        Prozent {
            int_representation: None,
            float_representation: Some(float_representation),
        }
    }

    pub fn from_betrags_differenz(einzel_betrag: &Betrag, gesamt_betrag: &Betrag) -> Prozent {
        if gesamt_betrag.as_cent() == 0 {
            return Prozent::from_int_representation(0);
        }
        let i = (einzel_betrag.as_cent() * 10000) / gesamt_betrag.as_cent();
        Prozent::from_float_representation(i as f64 / 100.00)
    }

    pub fn from_str_representation(str_representation: &str) -> Prozent {
        if let Ok(int_representation) = str_representation.parse::<u32>() {
            return Prozent::from_int_representation(int_representation);
        }
        Prozent::from_float_representation(str_representation.parse::<f64>().unwrap())
    }

    pub fn als_halbwegs_gerundeter_string(&self) -> String {
        if let Some(int_representation) = self.int_representation {
            format!("{}", int_representation)
        } else if let Some(float_representation) = self.float_representation {
            let rounded = (float_representation * 100.0).round() / 100.0;
            format!("{:.2}", rounded).replace(".", ",")
        } else {
            "".to_string()
        }
    }

    pub fn als_halbwegs_gerundeter_iso_string(&self) -> String {
        if let Some(int_representation) = self.int_representation {
            format!("{}", int_representation)
        } else if let Some(float_representation) = self.float_representation {
            let rounded = (float_representation * 100.0).round() / 100.0;
            format!("{:.2}", rounded)
        } else {
            "".to_string()
        }
    }

    pub fn invertiere(&self) -> Prozent {
        if let Some(int_representation) = self.int_representation {
            Prozent::from_int_representation(100 - int_representation)
        } else if let Some(float_representation) = self.float_representation {
            Prozent::from_float_representation(100.0 - float_representation)
        } else {
            Prozent::from_int_representation(0)
        }
    }

    pub fn zero() -> Prozent {
        Prozent::from_int_representation(0)
    }

    pub fn p50_50() -> Prozent {
        Prozent::from_int_representation(50)
    }
}

#[cfg(test)]
pub mod builder {
    pub fn any_prozent() -> super::Prozent {
        super::Prozent {
            int_representation: Some(0),
            float_representation: Some(0.0),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::Vorzeichen;

    #[test]
    fn test_as_string() {
        assert_eq!(Prozent::from_int_representation(10).as_string(), "10");
        assert_eq!(Prozent::from_float_representation(10.0).as_string(), "10");
        assert_eq!(Prozent::from_float_representation(10.5).as_string(), "10.5");
    }

    #[test]
    fn test_from_str_representation() {
        assert_eq!(
            Prozent::from_str_representation("10"),
            Prozent::from_int_representation(10)
        );
        assert_eq!(
            Prozent::from_str_representation("10.0"),
            Prozent::from_float_representation(10.0)
        );
        assert_eq!(
            Prozent::from_str_representation("10.5"),
            Prozent::from_float_representation(10.5)
        );
    }

    #[test]
    fn test_als_halbwegs_gerundeter_string() {
        assert_eq!(
            Prozent::from_int_representation(10).als_halbwegs_gerundeter_string(),
            "10"
        );
        assert_eq!(
            Prozent::from_float_representation(10.0).als_halbwegs_gerundeter_string(),
            "10,00"
        );
        assert_eq!(
            Prozent::from_float_representation(10.5).als_halbwegs_gerundeter_string(),
            "10,50"
        );
        assert_eq!(
            Prozent::from_float_representation(10.33333).als_halbwegs_gerundeter_string(),
            "10,33"
        );
    }

    #[test]
    fn test_als_halbwegs_gerundeter_iso_string() {
        assert_eq!(
            Prozent::from_int_representation(10).als_halbwegs_gerundeter_iso_string(),
            "10"
        );
        assert_eq!(
            Prozent::from_float_representation(10.0).als_halbwegs_gerundeter_iso_string(),
            "10.00"
        );
        assert_eq!(
            Prozent::from_float_representation(10.5).als_halbwegs_gerundeter_iso_string(),
            "10.50"
        );
        assert_eq!(
            Prozent::from_float_representation(10.33333).als_halbwegs_gerundeter_iso_string(),
            "10.33"
        );
    }

    #[test]
    fn test_invertiere() {
        assert_eq!(
            Prozent::from_int_representation(10).invertiere(),
            Prozent::from_int_representation(90)
        );
        assert_eq!(
            Prozent::from_float_representation(10.0).invertiere(),
            Prozent::from_float_representation(90.0)
        );
        assert_eq!(
            Prozent::from_float_representation(10.5).invertiere(),
            Prozent::from_float_representation(89.5)
        );
    }

    #[test]
    fn test_from_betrags_differenz() {
        let gesamt = Betrag::from_cent(Vorzeichen::Positiv, 100);
        let einzel = Betrag::from_cent(Vorzeichen::Positiv, 10);
        assert_eq!(
            Prozent::from_betrags_differenz(&einzel, &gesamt),
            Prozent::from_float_representation(10.0)
        );
    }

    #[test]
    fn test_from_betrags_differenz_with_zero_gesamtbetrag() {
        let gesamt = Betrag::from_cent(Vorzeichen::Positiv, 0);
        let einzel = Betrag::from_cent(Vorzeichen::Positiv, 10);
        assert_eq!(
            Prozent::from_betrags_differenz(&einzel, &gesamt),
            Prozent::from_int_representation(0)
        );
    }
}
