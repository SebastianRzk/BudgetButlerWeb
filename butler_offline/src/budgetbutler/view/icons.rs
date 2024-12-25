use std::borrow::Cow;

#[derive(Debug, Clone, PartialEq)]
pub struct Icon {
    pub as_fa: Cow<'static, str>,
}

pub const LIST: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-list"),
};

pub const PLUS: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-plus"),
};

pub const LINE_CHART: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-line-chart"),
};

pub const COGS: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-cogs"),
};

pub const PENCIL: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-pencil"),
};

pub const DELETE: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-trash"),
};

pub const GEAR: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-gear"),
};

pub const RELOAD: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-refresh"),
};

pub const DASHBOARD: Icon = Icon {
    as_fa: Cow::Borrowed("fa fa-dashboard"),
};
