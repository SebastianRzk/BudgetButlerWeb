from butler_offline.core.database.database_object import DatabaseObject


def extract_column_values(database_object: DatabaseObject, col_name: str):
    column = database_object.content[col_name]
    return column.to_list()


def extract_name_column(database_object: DatabaseObject):
    return extract_column_values(database_object=database_object, col_name='Name')


def extract_index(database_object: DatabaseObject):
    return database_object.content.index.to_list()
