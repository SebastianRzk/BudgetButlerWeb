use std::path::Path;

pub fn  create_initial_path_if_needed(path: &String){
    let full_path = Path::new(path);
    if !full_path.exists() {
        std::fs::create_dir_all(full_path).unwrap();
    }
}