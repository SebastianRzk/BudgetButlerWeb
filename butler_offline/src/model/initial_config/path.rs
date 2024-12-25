use std::path::PathBuf;

pub fn create_initial_path_if_needed(path: &PathBuf) {
    if !path.exists() {
        std::fs::create_dir_all(path).unwrap();
    }
}
