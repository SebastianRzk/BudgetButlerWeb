# BudgetButlerWeb Companion App API


## Installation der Datenbank mit diesel

```sh
cd databases/diesel
cargo install diesel_cli --no-default-features --features mysql


diesel setup
diesel migration run
```


## Manuelle Installation der Datenbank

Ausführen der `up.sql` Dateien im Ordner `migrations`