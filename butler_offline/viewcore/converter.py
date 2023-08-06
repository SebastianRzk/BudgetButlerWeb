from datetime import datetime


def datum(string):
    return datetime.strptime(string , '%Y-%m-%d').date()


def dezimal_float(string):
    string = string.replace(",", ".")
    return float(string)


def from_double_to_german(value):
    string_representation = "%.2f" % value
    return string_representation.replace(".", ",")


def datum_to_string(datum_obj):
    return datum_obj.strftime('%Y-%m-%d')


def datum_to_german(datum_obj):
    return datum_obj.strftime('%d.%m.%Y')


def datum_from_german(datum_str):
    return datetime.strptime(datum_str, '%d.%m.%Y').date()


def german_to_rfc(datum_str):
    return datum_to_string(datum_from_german(datum_str))


def datetime_to_filesystem_string(datetime_object: datetime) -> str:
    return str(datetime_object)


def to_descriptive_list(db_list):
    for element in db_list:
        if 'Datum' in element:
            element['Datum'] = datum_to_german(element['Datum'])
        if 'Wert' in element:
            element['Wert'] = from_double_to_german(element['Wert'])
    return db_list
