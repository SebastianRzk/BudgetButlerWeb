use crate::io::disk::diskrepresentation::file::{
    File, SortedFile, DAUERAUFTRAEGE_HEADER, DAUERAUFTRAG_ORDER_HEADER, DEPOTAUSZUEGE_HEADER,
    DEPOTWERTE_HEADER, EINZELBUCHUNGEN_HEADER, GEMEINSAME_BUCHUGEN_HEADER, ORDER_HEADER,
    SPARBUCHUNGEN_HEADER, SPARKONTOS_HEADER, *,
};
use crate::io::disk::diskrepresentation::line::Line;
use std::collections::HashMap;

pub fn sort_file(file: File) -> SortedFile {
    let mut current_modus = Modus::Einzelbuchungen;
    let mut result = HashMap::<Modus, Vec<Line>>::new();
    for line in file.lines {
        if line.line.len() == 0 {
            continue;
        }
        let modus_check_result = check_modus(&line);
        if let ModusCheckResult::NewModus(new_modus) = modus_check_result {
            current_modus = new_modus;
            continue;
        }
        if modus_check_result == ModusCheckResult::Header {
            continue;
        }
        let current_list = result.entry(current_modus.clone()).or_insert_with(Vec::new);
        current_list.push(line);
    }
    let empty_vec = Vec::<Line>::new();
    SortedFile {
        einzelbuchungen: result
            .get(&Modus::Einzelbuchungen)
            .unwrap_or(&empty_vec)
            .clone(),
        dauerauftraege: result
            .get(&Modus::Dauerauftraege)
            .unwrap_or(&Vec::new())
            .clone(),
        gemeinsame_buchungen: result
            .get(&Modus::GemeinsameBuchungen)
            .unwrap_or(&Vec::new())
            .clone(),
        sparbuchungen: result
            .get(&Modus::Sparbuchungen)
            .unwrap_or(&Vec::new())
            .clone(),
        sparkontos: result
            .get(&Modus::Sparkontos)
            .unwrap_or(&Vec::new())
            .clone(),
        depotwerte: result
            .get(&Modus::Depotwerte)
            .unwrap_or(&Vec::new())
            .clone(),
        order: result.get(&Modus::Order).unwrap_or(&Vec::new()).clone(),
        order_dauerauftrag: result
            .get(&Modus::DauerauftragOrder)
            .unwrap_or(&Vec::new())
            .clone(),
        depotauszuege: result
            .get(&Modus::Depotauszuege)
            .unwrap_or(&Vec::new())
            .clone(),
    }
}

fn check_modus(line: &Line) -> ModusCheckResult {
    match line.line.trim() {
        EINZELBUCHUNGEN_HEADER => ModusCheckResult::Header,
        DAUERAUFTRAEGE_HEADER => ModusCheckResult::Header,
        DAUERAUFTRAEGE_START_SIGNAL => ModusCheckResult::NewModus(Modus::Dauerauftraege),
        GEMEINSAME_BUCHUGEN_HEADER => ModusCheckResult::Header,
        GEMEINSAME_BUCHUGEN_START_SIGNAL => ModusCheckResult::NewModus(Modus::GemeinsameBuchungen),
        SPARBUCHUNGEN_HEADER => ModusCheckResult::Header,
        SPARBUCHUNGEN_START_SIGNAL => ModusCheckResult::NewModus(Modus::Sparbuchungen),
        SPARKONTOS_HEADER => ModusCheckResult::Header,
        SPARKONTOS_START_SIGNAL => ModusCheckResult::NewModus(Modus::Sparkontos),
        DEPOTWERTE_HEADER => ModusCheckResult::Header,
        DEPOTWERTE_START_SIGNAL => ModusCheckResult::NewModus(Modus::Depotwerte),
        ORDER_HEADER => ModusCheckResult::Header,
        ORDER_START_SIGNAL => ModusCheckResult::NewModus(Modus::Order),
        DAUERAUFTRAG_ORDER_HEADER => ModusCheckResult::Header,
        DAUERAUFTRAG_ORDER_START_SIGNAL => ModusCheckResult::NewModus(Modus::DauerauftragOrder),
        DEPOTAUSZUEGE_HEADER => ModusCheckResult::Header,
        DEPOTAUSZUEGE_START_SIGNAL => ModusCheckResult::NewModus(Modus::Depotauszuege),
        _ => ModusCheckResult::SameModus,
    }
}

#[derive(PartialEq)]
enum ModusCheckResult {
    NewModus(Modus),
    Header,
    SameModus,
}

#[derive(Hash, Eq, PartialEq, Clone, Debug)]
enum Modus {
    Einzelbuchungen,
    Dauerauftraege,
    GemeinsameBuchungen,
    Sparbuchungen,
    Sparkontos,
    Depotwerte,
    Order,
    DauerauftragOrder,
    Depotauszuege,
}

#[cfg(test)]
mod tests {
    use crate::io::disk::diskrepresentation::file::File;
    use crate::io::disk::diskrepresentation::sorter::sort_file;

    const DEMO_DATABASE: &str = "Datum,Kategorie,Name,Wert\n\
2024-01-01,NeueKategorie,EinName,-123.12\n\
\n\
 Dauerauftraege \n\
Startdatum,Endedatum,Kategorie,Name,Rhythmus,Wert\n\
2024-03-03,2024-02-02,EineKategorie,EinName,monatlich,-123.12\n\
\n\
 Gemeinsame Buchungen \n\
Datum,Kategorie,Name,Wert,Person\n\
2024-04-04,EineKategorie,EinName,-123.12,EinePerson\n\
\n\
 Sparbuchungen \n\
Datum,Name,Wert,Typ,Konto\n\
2024-05-05,EinName,-123.12,Manueller Auftrag,MeinKonto\n\
\n\
 Sparkontos \n\
Kontoname,Kontotyp\n\
MeinDepot,Depot\n\
\n\
 Depotwerte \n\
Name,ISIN,Typ\n\
MeinBeispielDepotwert,ETF999,ETF\n\
\n\
 Order \n\
Datum,Name,Konto,Depotwert,Wert,Typ\n\
2024-06-06,EinName,MeinKonto,ETF999,300.0\n\
\n\
 Dauerauftr_Ordr \n\
Startdatum,Endedatum,Rhythmus,Name,Konto,Depotwert,Wert,Typ\n\
2023-01-01,2023-04-30,monatlich,Beispiel Sparen,mein depot,123,300.0\n\
\n\
 Depotauszuege \n\
Datum,Depotwert,Konto,Wert\n\
2024-07-07,MeinDepot,MeinKonto,300.0\n\
";

    #[test]
    pub fn test_storter() {
        let file = File::from_str(DEMO_DATABASE);
        let sorted_file = sort_file(file);
        assert_eq!(sorted_file.einzelbuchungen.len(), 1);
        assert_eq!(
            sorted_file.einzelbuchungen.get(0).unwrap().line,
            "2024-01-01,NeueKategorie,EinName,-123.12"
        );

        assert_eq!(sorted_file.dauerauftraege.len(), 1);
        assert_eq!(
            sorted_file.dauerauftraege.get(0).unwrap().line,
            "2024-03-03,2024-02-02,EineKategorie,EinName,monatlich,-123.12"
        );

        assert_eq!(sorted_file.gemeinsame_buchungen.len(), 1);
        assert_eq!(
            sorted_file.gemeinsame_buchungen.get(0).unwrap().line,
            "2024-04-04,EineKategorie,EinName,-123.12,EinePerson"
        );

        assert_eq!(sorted_file.sparbuchungen.len(), 1);
        assert_eq!(
            sorted_file.sparbuchungen.get(0).unwrap().line,
            "2024-05-05,EinName,-123.12,Manueller Auftrag,MeinKonto"
        );

        assert_eq!(sorted_file.sparkontos.len(), 1);
        assert_eq!(
            sorted_file.sparkontos.get(0).unwrap().line,
            "MeinDepot,Depot"
        );

        assert_eq!(sorted_file.depotwerte.len(), 1);
        assert_eq!(
            sorted_file.depotwerte.get(0).unwrap().line,
            "MeinBeispielDepotwert,ETF999,ETF"
        );

        assert_eq!(sorted_file.order.len(), 1);
        assert_eq!(
            sorted_file.order.get(0).unwrap().line,
            "2024-06-06,EinName,MeinKonto,ETF999,300.0"
        );

        assert_eq!(sorted_file.order_dauerauftrag.len(), 1);
        assert_eq!(
            sorted_file.order_dauerauftrag.get(0).unwrap().line,
            "2023-01-01,2023-04-30,monatlich,Beispiel Sparen,mein depot,123,300.0"
        );

        assert_eq!(sorted_file.depotauszuege.len(), 1);
        assert_eq!(
            sorted_file.depotauszuege.get(0).unwrap().line,
            "2024-07-07,MeinDepot,MeinKonto,300.0"
        );
    }
}
