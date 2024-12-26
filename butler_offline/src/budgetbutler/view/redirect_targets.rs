use crate::budgetbutler::view::request_handler::Redirect;

pub fn redirect_to_optimistic_locking_error() -> Redirect {
    Redirect {
        target: "/error-optimistic-locking".to_string(),
    }
}

pub fn redirect_to_keine_aktion_gefunden() -> Redirect {
    Redirect {
        target: "/error-keine-aktion-gefunden".to_string(),
    }
}

pub fn redirect_to_isin_bereits_erfasst() -> Redirect {
    Redirect {
        target: "/error-isin-bereits-erfasst".to_string(),
    }
}

pub fn redirect_to_depotauszug_bereits_erfasst() -> Redirect {
    Redirect {
        target: "/error-depotauszug-bereits-erfasst".to_string(),
    }
}

pub fn redirect_to_dashboard() -> Redirect {
    Redirect {
        target: "/".to_string(),
    }
}
