use crate::budgetbutler::database::abrechnen::abrechnen::history::{
    read_and_sort_abrechnungen, PreparedAbrechnung, UnparsedAbrechnungsFile,
};

pub struct UebersichtAbrechnugnenContext {
    pub abrechnungen: Vec<UnparsedAbrechnungsFile>,
}

pub struct UebersichtAbrechnungenViewResult {
    pub abrechnugnen: Vec<PreparedAbrechnung>,
}

pub fn handle_view_abrechnungen(
    context: UebersichtAbrechnugnenContext,
) -> UebersichtAbrechnungenViewResult {
    let mut alle_abrechnungen = read_and_sort_abrechnungen(context.abrechnungen);
    alle_abrechnungen.reverse();
    UebersichtAbrechnungenViewResult {
        abrechnugnen: alle_abrechnungen,
    }
}
