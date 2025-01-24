use crate::model::eigenschaften::besitzt_betrag::BesitztBetrag;
use crate::model::indiziert::Indiziert;
use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;
use crate::model::primitives::prozent::Prozent;
use std::cmp::Ordering;
use std::ops::{Add, Sub};

#[derive(Debug, Clone, Eq)]
pub struct Betrag {
    pub euro: u32,
    pub cent: u8,
    pub vorzeichen: Vorzeichen,
}

#[derive(Debug, Clone, PartialEq, Eq, Hash, Ord, PartialOrd)]
pub enum Vorzeichen {
    Positiv,
    Negativ,
}

impl Default for Betrag {
    fn default() -> Self {
        Betrag::zero()
    }
}

impl PartialEq for Betrag {
    fn eq(&self, other: &Self) -> bool {
        if self.euro == 0 && other.euro == 0 && self.cent == 0 && other.cent == 0 {
            return true;
        }
        self.euro == other.euro && self.cent == other.cent && self.vorzeichen == other.vorzeichen
    }
}

impl Betrag {
    pub fn new(vorzeichen: Vorzeichen, euro: u32, cent: u8) -> Betrag {
        Betrag {
            euro,
            cent,
            vorzeichen,
        }
    }
    pub fn equals(&self, other: &Betrag) -> bool {
        self.euro == other.euro && self.cent == other.cent && self.vorzeichen == other.vorzeichen
    }

    pub fn to_german_string(&self) -> String {
        format!("{}{},{:02}", self.vorzeichen, self.euro, self.cent)
    }

    pub fn to_iso_string(&self) -> String {
        format!("{}{}.{:02}", self.vorzeichen, self.euro, self.cent)
    }

    pub fn halbiere(&self) -> Betrag {
        let as_cent = self.as_cent();
        let halbiert = as_cent / 2;
        Betrag::from_cent(self.vorzeichen.clone(), halbiert)
    }

    pub fn zero() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 0, 0)
    }

    pub fn abs(&self) -> Betrag {
        Betrag::new(Vorzeichen::Positiv, self.euro, self.cent)
    }

    pub fn negativ(&self) -> Betrag {
        Betrag::new(Vorzeichen::Negativ, self.euro, self.cent)
    }

    pub fn as_cent(&self) -> u64 {
        self.euro as u64 * 100 + self.cent as u64
    }

    pub fn from_iso_string(iso_string: &String) -> Betrag {
        let mut string_to_parse = iso_string.clone();
        let mut vorzeichen = Vorzeichen::Positiv;
        if string_to_parse.starts_with('-') {
            vorzeichen = Vorzeichen::Negativ;
            string_to_parse = string_to_parse.strip_prefix('-').unwrap().to_string();
        }

        if !string_to_parse.contains('.') {
            return Betrag::new(vorzeichen, parse_number(string_to_parse), 0);
        }
        let mut slitted = string_to_parse.split('.');
        let euro_as_string = slitted.next().unwrap();
        let cent_as_string = slitted.next().unwrap();

        let mut cent = parse_number_str(cent_as_string) as u8;
        if cent_as_string.len() == 1 {
            cent *= 10;
        }

        Betrag::new(vorzeichen, parse_number_str(euro_as_string), cent)
    }

    pub fn from_user_input(user_input_string: &String) -> Betrag {
        Betrag::from_iso_string(&user_input_string.replace(",", "."))
    }

    pub fn from_cent(vorzeichen: Vorzeichen, cent: u64) -> Betrag {
        Betrag::new(vorzeichen, (cent / 100) as u32, (cent % 100) as u8)
    }

    pub fn anteil(&self, prozent: &Prozent) -> Betrag {
        if let Some(int_representation) = prozent.int_representation {
            let neuer_betrag_als_cent = (self.as_cent() * int_representation as u64) / 100;
            return Betrag::from_cent(self.vorzeichen.clone(), neuer_betrag_als_cent);
        } else if let Some(float_representation) = prozent.float_representation {
            let neuer_betrag_als_cent = (self.as_cent() as f64 * float_representation) / 100.00;
            return Betrag::from_cent(self.vorzeichen.clone(), neuer_betrag_als_cent as u64);
        }
        Betrag::zero()
    }

    pub fn invertiere_vorzeichen(&self) -> Betrag {
        if self.vorzeichen == Vorzeichen::Positiv {
            return Betrag::new(Vorzeichen::Negativ, self.euro, self.cent);
        }
        Betrag::new(Vorzeichen::Positiv, self.euro, self.cent)
    }

    pub fn is_negativ(&self) -> bool {
        self.vorzeichen == Vorzeichen::Negativ
    }

    pub fn unsigned(&self) -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(self.euro, self.cent)
    }
}

pub fn parse_number(number: String) -> u32 {
    let stripped_number = number.strip_prefix("0").unwrap_or(number.as_str());
    if stripped_number.is_empty() {
        return 0;
    }
    stripped_number.parse().unwrap()
}

pub fn parse_number_str(number: &str) -> u32 {
    let stripped_number = number.strip_prefix("0").unwrap_or(number);
    if stripped_number.is_empty() {
        return 0;
    }
    stripped_number.parse().unwrap()
}

impl Add for Betrag {
    type Output = Betrag;

    fn add(self, rhs: Self) -> Self::Output {
        if self.vorzeichen == Vorzeichen::Negativ && rhs.vorzeichen == Vorzeichen::Negativ
            || self.vorzeichen == Vorzeichen::Positiv && rhs.vorzeichen == Vorzeichen::Positiv
        {
            let mut euro = self.euro + rhs.euro;
            let mut cent = self.cent + rhs.cent;
            if cent >= 100 {
                euro += 1;
                cent -= 100;
            }
            return Betrag {
                euro,
                cent,
                vorzeichen: self.vorzeichen,
            };
        }
        if self.vorzeichen == Vorzeichen::Positiv {
            self - rhs.abs()
        } else {
            rhs - self.abs()
        }
    }
}

impl Sub for Betrag {
    type Output = Betrag;

    fn sub(self, rhs: Self) -> Self::Output {
        if rhs.vorzeichen == Vorzeichen::Negativ {
            // e.g. 2 - (-2) = 2 + 2
            return self + rhs.abs();
        }
        if self.vorzeichen == Vorzeichen::Negativ {
            // e.g. -2 - 2 = - (2 + 2)
            let zwischensumme = self.abs() + rhs.abs();
            return Betrag {
                euro: zwischensumme.euro,
                cent: zwischensumme.cent,
                vorzeichen: Vorzeichen::Negativ,
            };
        }

        if self.euro > rhs.euro || (self.euro == rhs.euro && self.cent >= rhs.cent) {
            // Ergebnis ist positiv oder 0
            let euro = self.euro - rhs.euro;
            if rhs.cent > self.cent {
                return Betrag {
                    euro: euro - 1,
                    cent: 100 + self.cent - rhs.cent,
                    vorzeichen: Vorzeichen::Positiv,
                };
            }
            let cent = self.cent - rhs.cent;
            return Betrag {
                euro: euro,
                cent: cent,
                vorzeichen: Vorzeichen::Positiv,
            };
        }

        // Ergebnis ist negativ
        // e.g. 2 - 4 = -2

        let mut euro_abzug = rhs.euro;
        let cent_ergebnis;
        if self.cent > rhs.cent {
            cent_ergebnis = 100 + rhs.cent - self.cent;
            euro_abzug -= 1;
        } else {
            cent_ergebnis = rhs.cent - self.cent;
        }
        Betrag {
            euro: euro_abzug - self.euro,
            cent: cent_ergebnis,
            vorzeichen: Vorzeichen::Negativ,
        }
    }
}

impl Ord for Betrag {
    fn cmp(&self, other: &Self) -> Ordering {
        if self.vorzeichen == Vorzeichen::Negativ && other.vorzeichen == Vorzeichen::Positiv {
            return Ordering::Less;
        }
        if self.vorzeichen == Vorzeichen::Positiv && other.vorzeichen == Vorzeichen::Negativ {
            return Ordering::Greater;
        }

        if self.vorzeichen == Vorzeichen::Negativ {
            let val_fuer_positiv = self.abs().cmp(&other.abs());
            return match val_fuer_positiv {
                Ordering::Less => Ordering::Greater,
                Ordering::Greater => Ordering::Less,
                Ordering::Equal => Ordering::Equal,
            };
        }

        if self.euro > other.euro {
            return Ordering::Greater;
        }
        if self.euro < other.euro {
            return Ordering::Less;
        }
        if self.cent > other.cent {
            return Ordering::Greater;
        }
        if self.cent < other.cent {
            return Ordering::Less;
        }
        Ordering::Equal
    }
}

impl PartialOrd for Betrag {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl<'a> BesitztBetrag<'a> for Betrag {
    fn betrag(&'a self) -> &'a Betrag {
        &self
    }
}

impl<'a> BesitztBetrag<'a> for Indiziert<Betrag> {
    fn betrag(&'a self) -> &'a Betrag {
        &self.value
    }
}

#[cfg(test)]
pub fn betrag(vorzeichen: Vorzeichen, euro: u32, cent: u8) -> Betrag {
    Betrag::new(vorzeichen, euro, cent)
}

#[cfg(test)]
pub mod builder {
    use crate::model::primitives::betrag::Vorzeichen::Positiv;
    use crate::model::primitives::betrag::{Betrag, Vorzeichen};
    use crate::model::primitives::betrag_ohne_vorzeichen::BetragOhneVorzeichen;

    pub fn any_betrag() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 10, 10)
    }

    pub fn eins() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 1, 0)
    }

    pub fn zwei() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 2, 0)
    }

    pub fn minus_zwei() -> Betrag {
        Betrag::new(Vorzeichen::Negativ, 2, 0)
    }

    pub fn vier() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 4, 0)
    }

    pub fn fuenf() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 5, 0)
    }

    pub fn sieben() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 7, 0)
    }

    pub fn zehn() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 10, 0)
    }

    pub fn p_zero() -> Betrag {
        Betrag::new(Vorzeichen::Positiv, 0, 0)
    }

    pub fn n_zero() -> Betrag {
        Betrag::new(Vorzeichen::Negativ, 0, 0)
    }

    pub fn minus_fuenfzig() -> Betrag {
        Betrag::new(Vorzeichen::Negativ, 50, 0)
    }
    pub fn minus_hundert() -> Betrag {
        Betrag::new(Vorzeichen::Negativ, 100, 0)
    }

    pub fn u_betrag(euro: u32, cent: u8) -> BetragOhneVorzeichen {
        BetragOhneVorzeichen::new(euro, cent)
    }
    pub fn betrag(euro: u32) -> Betrag {
        Betrag::new(Positiv, euro, 0)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::primitives::betrag::builder::{minus_zwei, vier, zwei};

    #[test]
    fn test_betrag_to_german_string() {
        let betrag = Betrag::new(Vorzeichen::Positiv, 12, 34);
        assert_eq!(betrag.to_german_string(), "12,34");
    }

    #[test]
    fn test_betrag_to_german_string_with_zero() {
        let betrag = Betrag::new(Vorzeichen::Positiv, 0, 0);
        assert_eq!(betrag.to_german_string(), "0,00");
    }

    #[test]
    fn test_betrag_to_german_string_with_negative() {
        let betrag = Betrag::new(Vorzeichen::Negativ, 12, 34);
        assert_eq!(betrag.to_german_string(), "-12,34");
    }

    #[test]
    fn test_betrag_add() {
        let betrag = zwei() + vier();
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 6, 0));
    }

    #[test]
    fn test_betrag_add_with_carry() {
        let betrag =
            Betrag::new(Vorzeichen::Positiv, 1, 99) + Betrag::new(Vorzeichen::Positiv, 1, 2);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 3, 1));
    }

    #[test]
    fn test_betrag_add_with_negative() {
        let betrag = zwei() + minus_zwei();
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 0, 0));
    }

    #[test]
    fn test_betrag_sub() {
        let betrag = vier() - zwei();
        assert_eq!(betrag, zwei());
    }

    #[test]
    fn test_betrag_sub_ueberlauf_euro() {
        let betrag = zwei() - vier();
        assert_eq!(betrag, minus_zwei());
    }

    #[test]
    fn test_betrag_sub_ueberlauf_cent() {
        let betrag =
            Betrag::new(Vorzeichen::Positiv, 1, 0) - Betrag::new(Vorzeichen::Positiv, 0, 1);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 0, 99));
    }

    #[test]
    fn test_betrag_sub_ueberlauf_null() {
        let betrag =
            Betrag::new(Vorzeichen::Positiv, 1, 0) - Betrag::new(Vorzeichen::Positiv, 1, 1);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 0, 1));
    }

    #[test]
    fn test_betrag_sub_ueberlauf() {
        let betrag =
            Betrag::new(Vorzeichen::Positiv, 1, 0) - Betrag::new(Vorzeichen::Positiv, 2, 1);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 1, 1));
    }

    #[test]
    fn test_betrag_sub_minus_minus() {
        let betrag = zwei() - minus_zwei();
        assert_eq!(betrag, vier());
    }

    #[test]
    fn test_betrag_sub_minus_minus_minus() {
        let betrag = minus_zwei() - minus_zwei();
        assert_eq!(betrag, Betrag::zero());
    }

    #[test]
    fn test_betrag_sub_minus_plus() {
        let betrag = minus_zwei() - zwei();
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 4, 0));
    }
    #[test]
    fn test_parse() {
        assert_eq!(
            Betrag::from_iso_string(&"12.34".to_string()),
            betrag(Vorzeichen::Positiv, 12, 34)
        );
        assert_eq!(
            Betrag::from_iso_string(&"-12.34".to_string()),
            betrag(Vorzeichen::Negativ, 12, 34)
        );
        assert_eq!(
            Betrag::from_iso_string(&"-12.00".to_string()),
            betrag(Vorzeichen::Negativ, 12, 0)
        );
        assert_eq!(
            Betrag::from_iso_string(&"12.00".to_string()),
            betrag(Vorzeichen::Positiv, 12, 0)
        );
    }

    #[test]
    fn test_from_user_input() {
        assert_eq!(
            Betrag::from_user_input(&"12,34".to_string()),
            betrag(Vorzeichen::Positiv, 12, 34)
        );
        assert_eq!(
            Betrag::from_user_input(&"-12,34".to_string()),
            betrag(Vorzeichen::Negativ, 12, 34)
        );
        assert_eq!(
            Betrag::from_user_input(&"-12,00".to_string()),
            betrag(Vorzeichen::Negativ, 12, 0)
        );
        assert_eq!(
            Betrag::from_user_input(&"12,00".to_string()),
            betrag(Vorzeichen::Positiv, 12, 0)
        );
    }

    #[test]
    fn test_parse_with_leading_zero() {
        assert_eq!(
            Betrag::from_iso_string(&"012.34".to_string()),
            betrag(Vorzeichen::Positiv, 12, 34)
        );
        assert_eq!(
            Betrag::from_iso_string(&"-012.34".to_string()),
            betrag(Vorzeichen::Negativ, 12, 34)
        );
    }

    #[test]
    fn test_betrag_sub_nochmal() {
        let betrag =
            Betrag::new(Vorzeichen::Positiv, 20, 25) - Betrag::new(Vorzeichen::Positiv, 30, 0);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 9, 75));

        let betrag =
            Betrag::new(Vorzeichen::Positiv, 20, 25) - Betrag::new(Vorzeichen::Positiv, 30, 30);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 10, 5));

        let betrag =
            Betrag::new(Vorzeichen::Positiv, 20, 25) - Betrag::new(Vorzeichen::Positiv, 20, 25);
        assert_eq!(betrag, Betrag::zero());

        let betrag =
            Betrag::new(Vorzeichen::Positiv, 40, 25) - Betrag::new(Vorzeichen::Positiv, 30, 30);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 9, 95));

        let betrag =
            Betrag::new(Vorzeichen::Positiv, 40, 25) - Betrag::new(Vorzeichen::Positiv, 30, 10);
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 10, 15));

        let betrag = Betrag::zero() - Betrag::zero();
        assert_eq!(betrag, Betrag::zero());
    }

    #[test]
    fn test_betrag_abs() {
        let betrag = Betrag::new(Vorzeichen::Negativ, 12, 34).abs();
        assert_eq!(betrag, Betrag::new(Vorzeichen::Positiv, 12, 34));
    }

    #[test]
    fn test_betrag_negativ() {
        let betrag = Betrag::new(Vorzeichen::Positiv, 12, 34).negativ();
        assert_eq!(betrag, Betrag::new(Vorzeichen::Negativ, 12, 34));
    }

    #[test]
    fn test_read_negativen_betrag() {
        let ergebnis = Betrag::from_iso_string(&"-123.12".to_string());
        assert_eq!(ergebnis, betrag(Vorzeichen::Negativ, 123, 12));
    }

    #[test]
    fn test_read_positiven_betrag() {
        let ergebnis = Betrag::from_iso_string(&"123.12".to_string());
        assert_eq!(ergebnis, betrag(Vorzeichen::Positiv, 123, 12));
    }

    #[test]
    fn test_read_positiven_betrag_without_comma() {
        let ergebnis = Betrag::from_iso_string(&"123".to_string());
        assert_eq!(ergebnis, betrag(Vorzeichen::Positiv, 123, 0));
    }

    #[test]
    fn test_betrag_from_cent() {
        assert_eq!(
            Betrag::from_cent(Vorzeichen::Positiv, 12312),
            betrag(Vorzeichen::Positiv, 123, 12)
        );
    }

    #[test]
    fn test_betrag_halbiere() {
        assert_eq!(
            Betrag::from_cent(Vorzeichen::Positiv, 12312).halbiere(),
            betrag(Vorzeichen::Positiv, 61, 56)
        );
    }

    #[test]
    fn test_betrag_ord() {
        let a = betrag(Vorzeichen::Positiv, 1, 0);
        let b = betrag(Vorzeichen::Positiv, 2, 0);
        assert_eq!(a.cmp(&b), Ordering::Less);
        assert_eq!(a.cmp(&a), Ordering::Equal);
        assert_eq!(b.cmp(&a), Ordering::Greater);

        let a = betrag(Vorzeichen::Positiv, 1, 0);
        let b = betrag(Vorzeichen::Negativ, 2, 0);
        assert_eq!(a.cmp(&b), Ordering::Greater);
        assert_eq!(a.cmp(&a), Ordering::Equal);
        assert_eq!(b.cmp(&a), Ordering::Less);

        let a = betrag(Vorzeichen::Negativ, 1, 0);
        let b = betrag(Vorzeichen::Negativ, 2, 0);
        assert_eq!(a.cmp(&b), Ordering::Greater);
        assert_eq!(a.cmp(&a), Ordering::Equal);
        assert_eq!(b.cmp(&a), Ordering::Less);
    }

    #[test]
    fn test_betrag_from_iso_string() {
        assert_eq!(Betrag::from_iso_string(&"0.50".to_string()).as_cent(), 50);
        assert_eq!(Betrag::from_iso_string(&"0.5".to_string()).as_cent(), 50);
        assert_eq!(Betrag::from_iso_string(&"1.23".to_string()).as_cent(), 123);
        assert_eq!(Betrag::from_iso_string(&"0.01".to_string()).as_cent(), 1);
    }

    #[test]
    fn test_anteil() {
        assert_eq!(
            betrag(Vorzeichen::Positiv, 100, 0).anteil(&Prozent::from_int_representation(50)),
            betrag(Vorzeichen::Positiv, 50, 0)
        );
        assert_eq!(
            betrag(Vorzeichen::Positiv, 20, 0).anteil(&Prozent::from_int_representation(30)),
            betrag(Vorzeichen::Positiv, 6, 0)
        );
        assert_eq!(
            betrag(Vorzeichen::Positiv, 100, 0).anteil(&Prozent::from_float_representation(30.333)),
            betrag(Vorzeichen::Positiv, 30, 33)
        );
    }

    #[test]
    fn test_invertiere_betrag() {
        assert_eq!(
            Betrag::new(Vorzeichen::Positiv, 100, 0).invertiere_vorzeichen(),
            Betrag::new(Vorzeichen::Negativ, 100, 0)
        );
    }

    #[test]
    fn test_is_negativ() {
        assert_eq!(Betrag::new(Vorzeichen::Negativ, 100, 0).is_negativ(), true);
        assert_eq!(Betrag::new(Vorzeichen::Positiv, 100, 0).is_negativ(), false);
    }
}
