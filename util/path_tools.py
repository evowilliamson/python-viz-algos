from pathlib import Path
import os
import shutil

def create_dir_in_user_home(dir, overwrite=True):
    if overwrite:
        clean_dir_in_user_home(dir)
    os.mkdir(Path(get_user_home(), dir))


def clean_dir_in_user_home(dir):
    if Path(str(get_user_home()), dir).exists() and Path(str(get_user_home()), dir).is_dir():
        shutil.rmtree(Path(get_user_home(), dir))

def get_dir_in_user_home(dir):
    return str(Path(get_user_home(), dir))

def get_user_home():
    return str(Path.home())