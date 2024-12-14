use crate::io::disk::diskrepresentation::line::Line;
use crate::io::disk::primitive::betrag::write_betrag;
use crate::io::disk::primitive::datum::write_datum;
use crate::io::disk::primitive::line::create_line;
use crate::io::disk::primitive::sparbuchungtyp::write_sparbuchungtyp;
use crate::model::database::sparbuchung::Sparbuchung;

pub fn write_sparbuchung(sparbuchung: &Sparbuchung) -> Line {
    create_line(vec![
        write_datum(&sparbuchung.datum),
        sparbuchung.name.clone().into(),
        write_betrag(&sparbuchung.wert),
        write_sparbuchungtyp(&sparbuchung.typ),
        sparbuchung.konto.clone().into(),
    ])
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::model::database::sparbuchung::builder::konto_referenz;
    use crate::model::database::sparbuchung::SparbuchungTyp;
    use crate::model::primitives::betrag::{betrag, Vorzeichen};
    use crate::model::primitives::datum::Datum;
    use crate::model::primitives::name::name;

    #[test]
    fn test_write_sparbuchung() {
        let sparbuchung = Sparbuchung{
            datum: Datum::new(1, 1, 2024),
            name: name("DerName"),
            wert: betrag(Vorzeichen::Negativ, 123, 12),
            typ: SparbuchungTyp::Ausschuettung,
            konto: konto_referenz("DasKonto"),
        };

        let line = write_sparbuchung(&sparbuchung);

        assert_eq!(line.line, "2024-01-01,DerName,-123.12,Ausschüttung,DasKonto");
    }
}