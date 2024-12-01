use crate::budgetbutler::pages::core::error_optimistic_locking::ErrorOptimisticLockingViewResult;
use crate::budgetbutler::view::menu::resolve_active_group_from_url;
use crate::budgetbutler::view::optimistic_locking::{
    check_optimistic_locking_error, OptimisticLockingResult,
};
use crate::budgetbutler::view::redirect_targets::redirect_to_optimistic_locking_error;
use crate::io::disk::reader::read_database;
use crate::io::disk::writer::write_database;
use crate::io::html::views::core::error_optimistic_locking::render_error_optimistic_locking_template;
use crate::io::html::views::index::render_index_template;
use crate::model::state::config::DatabaseConfiguration;
use crate::model::state::persistent_application_state::{
    create_initial_database_version, Database, DatabaseVersion,
};
use std::sync::Mutex;

pub fn handle_render_display_view<CONTEXT, VIEW_RESULT>(
    page_name: &str,
    page_url: &str,
    context: CONTEXT,
    display_function: impl Fn(CONTEXT) -> VIEW_RESULT,
    render_function: impl Fn(VIEW_RESULT) -> String,
) -> String {
    let view_result = display_function(context);
    let render_view = render_function(view_result);
    render_index_template(
        resolve_active_group_from_url(page_url),
        page_url.to_string(),
        page_name.to_string(),
        render_view,
        None,
    )
}

pub fn handle_modification<CONTEXT, CHANCE_TRACKER>(
    context: VersionedContext<CONTEXT>,
    change_tracer: &Mutex<Vec<CHANCE_TRACKER>>,
    modification_action: impl Fn(CONTEXT) -> RedirectResult<CHANCE_TRACKER>,
    database_configuration: &DatabaseConfiguration,
) -> ModificationResult {
    let optimistic_locking_result =
        check_optimistic_locking_error(&context.requested_db_version, context.current_db_version);
    if optimistic_locking_result == OptimisticLockingResult::Error {
        return ModificationResult {
            target: redirect_to_optimistic_locking_error(),
            changed_database: read_database(
                database_configuration,
                create_initial_database_version(database_configuration.name.clone()),
            ),
        };
    }
    let render_view = modification_action(context.context);
    change_tracer.lock().unwrap().push(render_view.change);
    save_database(&render_view.result.changed_database, database_configuration);
    ModificationResult {
        target: render_view.result.target,
        changed_database: read_database(
            database_configuration,
            render_view.result.changed_database.db_version.clone(),
        ),
    }
}

pub fn handle_modification_manual<VIEW_RESULT>(
    requested_db_version: String,
    current_db_version: DatabaseVersion,
    page_url: &str,
    page_name: &str,
    result: VIEW_RESULT,
    render_function: impl Fn(VIEW_RESULT) -> String,
    database_configuration: &DatabaseConfiguration,
    new_database: Database,
    message: SuccessMessage,
) -> ManualRenderResult {
    let optimistic_locking_result =
        check_optimistic_locking_error(&requested_db_version, current_db_version);
    let page_content: String;
    let valid_next_state: Option<Database>;
    let success_message: Option<SuccessMessage>;
    if optimistic_locking_result == OptimisticLockingResult::Error {
        page_content =
            render_error_optimistic_locking_template(ErrorOptimisticLockingViewResult {});
        valid_next_state = None;
        success_message = None;
    } else {
        save_database(&new_database, database_configuration);
        page_content = render_function(result);
        valid_next_state = Some(new_database);
        success_message = Some(message);
    }

    ManualRenderResult {
        valid_next_state,
        full_rendered_page: render_index_template(
            resolve_active_group_from_url(page_url),
            page_url.to_string(),
            page_name.to_string(),
            page_content,
            success_message,
        ),
    }
}
pub fn no_page_middleware<T>(context: T) -> T {
    context
}

fn save_database(database: &Database, database_configuration: &DatabaseConfiguration) {
    write_database(database, database_configuration);
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

pub struct RedirectResult<T> {
    pub result: ModificationResult,
    pub change: T,
}

pub struct SuccessMessage {
    pub message: String,
}

pub struct ManualRenderResult {
    pub valid_next_state: Option<Database>,
    pub full_rendered_page: String,
}
