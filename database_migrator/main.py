import database_manager
import sys
import config
import json
import os
import shutil

def makedir(name):
    if not os.path.exists(name):
        print(f"Creating directory {name}")
        os.makedirs(name)

def copy_all_files(src, dest):
    for file in os.listdir(src):
        shutil.copy2(os.path.join(src, file), dest)

def copy_file(src, dest):
    shutil.copyfile(src, dest)

def move_file(src, dest):
    shutil.move(src, dest)

def move_folder(src, dest):
    if not os.path.exists(src):
        print("Directory does not exist")
        return
    print(f"Moving {src} to {dest}")
    shutil.move(src, dest)

if __name__ == '__main__':
    path = sys.argv[1]
    print("Reading database from", path)
    database = database_manager.read(path)
    print("Database read")
    print()
    print("Reading configuration")
    configuration = config.get_applied_configuration()
    print("Configuration read")
    print()

    print("Create data directory")
    makedir('./data')
    makedir('./data/abrechnungen')
    makedir('./data/backups')
    makedir('./data/backups/import_backup')
    print("Data directory created")
    print()

    print("Create migration backup directory")
    makedir('./data/backups/migration_backup')
    print("Create migration backup directory")
    print("")

    print("Writing database to file")
    file_object = open(f'./data/Database_{configuration['user_configuration']['self_name']['person']}.csv', 'w')
    file_object.write(database)
    file_object.close()
    print("Database written")
    print()
    print("Writing configuration to file")
    config = open(f'./data/configuration.json', 'w')
    config.write(json.dumps(configuration))
    config.close()
    print("Configuration written")
    print()

    print("Start migrating files")
    print("")
    print("Copy abrechnungen")
    copy_all_files('./Abrechnungen', './data/abrechnungen')
    print("Abrechnungen copied")
    print()
    print("Copy shares info cache")
    copy_file('./shares_info_cache.json', './data/backups/import_backup/shares_info_cache.json')
    move_file('./shares_info_cache.json', './data/shares_data.cache.json')
    print("Abrechnungen copied")
    print()
    print("Move Abrechnungen")
    move_folder('./Abrechnungen', './data/backups/import_backup/Abrechnungen')
    print("Abrechnungen moved")
    print()
    print("Move backups")
    move_folder('./Backups', './data/backups/import_backup/Backups')
    print("Backups moved")
    print()
    print("Move import")
    move_folder('./Import', './data/backups/import_backup/Import')
    print("Import moved")
    print()
    print("Move Online_Import")
    move_folder('./Online_Import', './data/backups/import_backup/Online_Import')
    print("Online_Import moved")
    print()
    print("Move config")
    move_folder('./config', './data/backups/import_backup/config')
    print("Config moved")
    print()
    print("Move Database")
    move_folder(path, './data/backups/import_backup/' + os.path.basename(path))
    print("Database moved")
    print()

    print("Migration finished")