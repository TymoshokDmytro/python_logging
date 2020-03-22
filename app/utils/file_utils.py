import os


def get_parent_folder(module_path):
    return os.path.dirname(module_path)


def get_parent_folder_basename(module_path):
    return os.path.basename(get_parent_folder(module_path))
