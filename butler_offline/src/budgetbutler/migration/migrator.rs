use crate::budgetbutler::migration::model::ApplicationVersion;
use crate::io::disk::shares::save_shares;
use crate::io::disk::version::save_user_data_version;
use crate::model::shares::shares_state::ShareState;
use crate::model::state::non_persistent_application_state::UserApplicationDirectory;
use crate::model::user_data::SHARES_FILE_NAME;
use std::fs;

pub fn run_migrations(
    current_version: ApplicationVersion,
    data_state_version: ApplicationVersion,
    user_application_directory: &UserApplicationDirectory,
) {
    println!("Running migrations from version {data_state_version} to {current_version}");

    if data_state_version > current_version {
        panic!("Der Datenbestand ist neuer als die aktuelle Version. Bitte aktualisieren Sie die Anwendung.");
    }

    if data_state_version == current_version {
        println!("Keine Migration erforderlich.");
        return;
    }

    let version_4_3_0 = ApplicationVersion::new("4.3.0");
    if data_state_version < version_4_3_0 {
        print_running_migration(version_4_3_0);
        migriere_4_3_0(user_application_directory)
    }

    save_user_data_version(user_application_directory, &current_version);
    println!("Migrated from version {data_state_version} to {current_version}");
}

fn migriere_4_3_0(user_application_directory: &UserApplicationDirectory) {
    let shares_filename = user_application_directory.path.join(SHARES_FILE_NAME);
    if shares_filename.exists() {
        fs::copy(
            shares_filename,
            user_application_directory
                .path
                .join(format!("{SHARES_FILE_NAME}.4.3.0.migration.backup")),
        )
        .expect("Could not copy shares file");
        save_shares(user_application_directory, &ShareState::default());
    } else {
        println!("No shares file found, no migration needed.");
    }
}

fn print_running_migration(migration: ApplicationVersion) {
    println!("Running migration: {migration}");
}
