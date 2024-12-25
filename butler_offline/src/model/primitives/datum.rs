use std::cmp::Ordering;

#[derive(Debug, Hash, Clone, PartialEq, Eq)]
pub struct Datum {
    pub tag: u32,
    pub monat: u32,
    pub jahr: i32,
}

impl Datum {
    pub fn new(tag: u32, monat: u32, jahr: i32) -> Datum {
        Datum { tag, monat, jahr }
    }
    pub fn equals(&self, other: &Datum) -> bool {
        self.tag == other.tag && self.monat == other.monat && self.jahr == other.jahr
    }
    pub fn to_german_string(&self) -> String {
        format!("{:02}.{:02}.{}", self.tag, self.monat, self.jahr)
    }

    pub fn to_iso_string(&self) -> String {
        format!("{}-{:02}-{:02}", self.jahr, self.monat, self.tag)
    }

    pub fn substract_months(self, months: u32) -> Datum {
        let mut monat = self.monat as i32 - months as i32;
        let mut jahr = self.jahr;
        while monat <= 0 {
            monat += 12;
            jahr -= 1;
        }
        Datum {
            tag: Datum::berechne_ggf_letzter_tag_des_monats(monat as u32, self.tag),
            monat: monat as u32,
            jahr,
        }
    }

    pub fn add_months(self, months: u32) -> Datum {
        let mut monat = self.monat as i32 + months as i32;
        let mut jahr = self.jahr;
        while monat > 12 {
            monat -= 12;
            jahr += 1;
        }
        Datum {
            tag: Datum::berechne_ggf_letzter_tag_des_monats(monat as u32, self.tag),
            monat: monat as u32,
            jahr,
        }
    }

    fn berechne_ggf_letzter_tag_des_monats(monat: u32, tag: u32) -> u32 {
        if tag > 28 {
            if monat == 2 {
                return 28;
            }
            if tag > 30 {
                if [4, 6, 9, 11].contains(&monat) {
                    return 30;
                }
            }
        }
        tag
    }

    pub fn ziehe_einen_tag_ab(&self) -> Datum {
        if self.tag == 1 {
            if self.monat == 1 {
                return Datum::new(31, 12, self.jahr - 1);
            }
            let monat = self.monat - 1;
            return Datum::new(
                Datum::berechne_ggf_letzter_tag_des_monats(monat, 31),
                monat,
                self.jahr,
            );
        }
        Datum::new(self.tag - 1, self.monat, self.jahr)
    }

    pub fn clamp_to_first_of_month(&self) -> Datum {
        Datum {
            tag: 1,
            monat: self.monat,
            jahr: self.jahr,
        }
    }

    pub fn from_iso_string(iso_string: &String) -> Datum {
        let mut splitted = iso_string.split('-');
        let jahr = splitted.next().unwrap();
        let monat = splitted.next().unwrap();
        let tag = splitted.next().unwrap();
        Datum::new(
            tag.parse().unwrap(),
            monat.parse().unwrap(),
            jahr.parse().unwrap(),
        )
    }

    pub fn from_german_string(german_string: &String) -> Datum {
        let mut splitted = german_string.split('.');
        let tag = splitted.next().unwrap();
        let monat = splitted.next().unwrap();
        let jahr = splitted.next().unwrap();
        Datum::new(
            tag.parse().unwrap(),
            monat.parse().unwrap(),
            jahr.parse().unwrap(),
        )
    }
}

impl PartialOrd<Self> for Datum {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl Ord for Datum {
    fn cmp(&self, other: &Self) -> Ordering {
        let jahr_cmp = self.jahr.cmp(&other.jahr);
        if jahr_cmp != Ordering::Equal {
            return jahr_cmp;
        }

        let monat_cmp = self.monat.cmp(&other.monat);
        if monat_cmp != Ordering::Equal {
            return monat_cmp;
        }

        self.tag.cmp(&other.tag)
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct MonatsName {
    pub monat: String,
}

#[derive(Debug, Clone, PartialEq)]
pub struct JahresName {
    pub jahr: String,
}

pub fn monats_name(name: &str) -> MonatsName {
    MonatsName {
        monat: name.to_string(),
    }
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::datum::{Datum, JahresName};

    pub fn any_datum() -> Datum {
        Datum::new(1, 1, 2020)
    }

    pub fn demo_datum() -> Datum {
        Datum::new(1, 1, 2024)
    }

    pub fn datum(datum_iso: &str) -> Datum {
        Datum::from_iso_string(&datum_iso.to_string())
    }

    pub fn jahres_name(jahr: &str) -> JahresName {
        JahresName {
            jahr: jahr.to_string(),
        }
    }

    impl Datum {
        pub fn first() -> Datum {
            Datum::new(0, 0, 0)
        }

        pub fn last() -> Datum {
            Datum::new(31, 12, 9999)
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_substract_months() {
        let datum = Datum::new(1, 1, 2020);
        let result = datum.substract_months(1);
        assert_eq!(result, Datum::new(1, 12, 2019));
    }

    #[test]
    fn test_substract_months_over_a_year() {
        let datum = Datum::new(1, 1, 2020);
        let result = datum.substract_months(13);
        assert_eq!(result, Datum::new(1, 12, 2018));
    }

    #[test]
    fn test_clamp_to_first_of_month() {
        let datum = Datum::new(15, 1, 2020);
        let result = datum.clamp_to_first_of_month();
        assert_eq!(result, Datum::new(1, 1, 2020));
    }

    #[test]
    fn test_partial_cmp_equal() {
        let datum = Datum::new(1, 1, 2020);
        let datum2 = Datum::new(1, 1, 2020);
        assert_eq!(datum.partial_cmp(&datum2), Some(Ordering::Equal));
    }

    #[test]
    fn test_partial_cmp_year() {
        let greater = Datum::new(1, 1, 2021);
        let smaller = Datum::new(1, 1, 2020);
        assert_eq!(greater > smaller, true);
        assert_eq!(greater.partial_cmp(&smaller), Some(Ordering::Greater));
        assert_eq!(smaller.partial_cmp(&greater), Some(Ordering::Less));
    }

    #[test]
    fn test_partial_cmp_month() {
        let greater = Datum::new(1, 2, 2020);
        let smaller = Datum::new(1, 1, 2020);
        assert_eq!(greater.partial_cmp(&smaller), Some(Ordering::Greater));
        assert_eq!(smaller.partial_cmp(&greater), Some(Ordering::Less));
    }

    #[test]
    fn test_partial_cmp_day() {
        let greater = Datum::new(2, 1, 2020);
        let smaller = Datum::new(1, 1, 2020);
        assert_eq!(greater.partial_cmp(&smaller), Some(Ordering::Greater));
        assert_eq!(smaller.partial_cmp(&greater), Some(Ordering::Less));
    }

    #[test]
    fn test_berechne_ggf_letzter_tag_des_monats() {
        assert_eq!(Datum::berechne_ggf_letzter_tag_des_monats(2, 29), 28);
        assert_eq!(Datum::berechne_ggf_letzter_tag_des_monats(2, 28), 28);
        assert_eq!(Datum::berechne_ggf_letzter_tag_des_monats(3, 31), 31);
        assert_eq!(Datum::berechne_ggf_letzter_tag_des_monats(4, 31), 30);
    }

    #[test]
    fn test_add_months() {
        let datum = Datum::new(1, 1, 2020);
        let result = datum.add_months(1);
        assert_eq!(result, Datum::new(1, 2, 2020));
    }

    #[test]
    fn test_add_months_over_a_year() {
        let datum = Datum::new(1, 12, 2020);
        let result = datum.add_months(1);
        assert_eq!(result, Datum::new(1, 1, 2021));
    }

    #[test]
    fn test_to_iso_string() {
        let datum = Datum::new(1, 1, 2020);
        assert_eq!(datum.to_iso_string(), "2020-01-01");
    }

    #[test]
    fn test_read_datum() {
        let ergebnis = Datum::from_iso_string(&"2020-01-01".to_string());
        assert_eq!(ergebnis, Datum::new(1, 1, 2020));
    }

    #[test]
    fn test_ziehe_einen_tag_ab() {
        assert_eq!(
            Datum::new(2, 1, 2020).ziehe_einen_tag_ab(),
            Datum::new(1, 1, 2020)
        );
        assert_eq!(
            Datum::new(1, 1, 2020).ziehe_einen_tag_ab(),
            Datum::new(31, 12, 2019)
        );
    }

    #[test]
    fn test_from_german_string() {
        let ergebnis = Datum::from_german_string(&"01.01.2020".to_string());
        assert_eq!(ergebnis, Datum::new(1, 1, 2020));
    }
}
