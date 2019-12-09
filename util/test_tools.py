from pathlib import Path
import os
import shutil

TEST_RESOURCES_PATH = Path(str(Path.home()), "python-test-resources")

def create_test_resources_dir():
    clean_test_resources()
    os.mkdir(TEST_RESOURCES_PATH)


def clean_test_resources():
    if TEST_RESOURCES_PATH.exists() and TEST_RESOURCES_PATH.is_dir():
        shutil.rmtree(TEST_RESOURCES_PATH)


def get_test_resources_path():
    return TEST_RESOURCES_PATH