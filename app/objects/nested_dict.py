from functools import reduce


def get_nested_attribute(path, dictionary):
    """Get attribute from nested dictionary"""
    path_list = path.split('.')
    return reduce(dict.get, path_list[:-1], dictionary)[path_list[-1]]


def set_nested_attribute(path, value, dictionary):
    """Set attribute in nested dictionary"""
    path_list = path.split('.')
    reduce(dict.get, path_list[:-1], dictionary)[path_list[-1]] = value


def pop_nested_attribute(path, dictionary):
    """Remove attribute from nested dictionary"""
    path_list = path.split('.')
    value = reduce(dict.get, path_list[:-1], dictionary)[path_list[-1]]
    del reduce(dict.get, path_list[:-1], dictionary)[path_list[-1]]
    return value


def pop_key_from_path(path):
    return path.split('.')[-1]
