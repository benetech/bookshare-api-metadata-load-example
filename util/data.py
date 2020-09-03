def exists(record, field_name):
    """
    Our definition of whether a field exists in a Python dict
    """
    return field_name in record and record[field_name] is not None and record[field_name] != ''


def copy_fields(source, destination, field_list):
    """
    Copy a list of fields from a source dict to a destination dict
    :param source:
    :param destination:
    :param field_list:
    :return:
    """
    for field_name in field_list:
        if exists(source, field_name):
            if field_name == 'isbn13':
                destination['isbn'] = source['isbn13']
            else:
                destination[field_name] = source[field_name]
