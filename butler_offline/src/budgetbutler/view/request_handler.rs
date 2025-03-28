use crate::budgetbutler::view::menu::resolve_active_group_from_url;
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::io::disk::reader::read_database;
use crate::io::disk::updater::update_database;
use crate::io::html::views::core::error_optimistic_locking::render_error_optimistic_locking_template;
use crate::io::html::views::core::zurueck_zu::{
    render_success_message_template, SuccessZurueckZuViewResult,
};
use crate::io::html::views::index::{render_index_template, PageTitle};
use crate::model::state::config::DatabaseConfiguration;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::state::persistent_application_state::Database;
use crate::model::state::persistent_state::database_version::{
    create_initial_database_version, DatabaseVersion,
};
use std::sync::Mutex;

pub fn handle_render_display_view(
    page_name: PageTitle,
    active_page: ActivePage,
    database_name: String,
    render_view: String,
) -> String {
    render_index_template(
        resolve_active_group_from_url(&active_page),
        active_page,
        page_name,
        render_view,
        None,
        database_name,
    )
}

pub fn handle_modification<CONTEXT, ChangeTracker>(
    context: VersionedContext<CONTEXT>,
    change_tracer: &Mutex<Vec<ChangeTracker>>,
    modification_action: impl Fn(CONTEXT) -> RedirectResult<ChangeTracker>,
    database_configuration: &DatabaseConfiguration,
    user_application_directory: &UserApplicationDirectory,
) -> ModificationResult {
    let optimistic_locking_result =
        check_optimistic_locking_error(&context.requested_db_version, context.current_db_version);
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return ModificationResult {
            target: redirect_to_optimistic_locking_error(),
            changed_database: read_database(
                user_application_directory,
                database_configuration,
                create_initial_database_version(database_configuration.name.clone()),
            ),
        };
    }
    let render_view = modification_action(context.context);
    change_tracer.lock().unwrap().push(render_view.change);
    let refreshed_database = update_database(
        user_application_directory,
        database_configuration,
        render_view.result.changed_database,
    );
    ModificationResult {
        target: render_view.result.target,
        changed_database: refreshed_database,
    }
}

pub fn handle_modification_without_change<CONTEXT>(
    context: VersionedContext<CONTEXT>,
    modification_action: impl Fn(CONTEXT) -> ModificationResult,
    database_configuration: &DatabaseConfiguration,
    user_application_directory: &UserApplicationDirectory,
) -> ModificationResult {
    let optimistic_locking_result =
        check_optimistic_locking_error(&context.requested_db_version, context.current_db_version);
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return ModificationResult {
            target: redirect_to_optimistic_locking_error(),
            changed_database: read_database(
                user_application_directory,
                database_configuration,
                create_initial_database_version(database_configuration.name.clone()),
            ),
        };
    }
    let render_view = modification_action(context.context);
    let refreshed_database = update_database(
        user_application_directory,
        database_configuration,
        render_view.changed_database,
    );
    ModificationResult {
        target: render_view.target,
        changed_database: refreshed_database,
    }
}

pub fn handle_modification_manual(
    requested_db_version: String,
    current_db_version: DatabaseVersion,
    database_configuration: &DatabaseConfiguration,
    new_database: Database,
    user_application_directory: &UserApplicationDirectory,
) -> ManualRenderResult {
    let optimistic_locking_result =
        check_optimistic_locking_error(&requested_db_version, current_db_version);
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return ManualRenderResult {
            valid_next_state: Err(render_error_optimistic_locking_template(None)),
        };
    }
    let new_database = update_database(
        user_application_directory,
        database_configuration,
        new_database,
    );

    ManualRenderResult {
        valid_next_state: Ok(new_database),
    }
}

pub fn no_page_middleware<T>(context: T) -> T {
    context
}

pub struct VersionedContext<T> {
    pub requested_db_version: String,
    pub current_db_version: DatabaseVersion,
    pub context: T,
}

pub struct ModificationResult {
    pub target: Redirect,
    pub changed_database: Database,
}

pub struct Redirect {
    pub target: String,
}

impl Redirect {
    pub fn to(target: &str) -> Redirect {
        Redirect {
            target: target.to_string(),
        }
    }
}

pub struct RedirectResult<T> {
    pub result: ModificationResult,
    pub change: T,
}

pub struct SuccessMessage {
    pub message: String,
}

pub struct ManualRenderResult {
    pub valid_next_state: Result<Database, String>,
}

pub fn handle_render_success_display_message(
    page_name: &'static str,
    active_page: ActivePage,
    database_name: String,
    context: DisplaySuccessMessage,
) -> String {
    let render_view = render_success_message_template(SuccessZurueckZuViewResult {
        text: context.link_name,
        link: context.link_url,
    });
    render_index_template(
        resolve_active_group_from_url(&active_page),
        active_page,
        PageTitle::new(page_name),
        render_view,
        Some(SuccessMessage {
            message: context.message,
        }),
        database_name,
    )
}

pub struct DisplaySuccessMessage {
    pub message: String,
    pub link_name: String,
    pub link_url: String,
}

pub struct ActivePage {
    pub active_page_url: &'static str,
}

impl ActivePage {
    pub fn construct_from_url(url: &'static str) -> ActivePage {
        ActivePage {
            active_page_url: url,
        }
    }
}

#[cfg(test)]
mod tests {}
