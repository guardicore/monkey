import os

import pytest

from monkey_island.cc.services.post_breach_files import PostBreachFilesService


@pytest.fixture(autouse=True)
def custom_pba_directory(tmpdir):
    PostBreachFilesService.initialize(tmpdir)


def create_custom_pba_file(filename):
    assert os.path.isdir(PostBreachFilesService.get_custom_pba_directory())

    file_path = os.path.join(PostBreachFilesService.get_custom_pba_directory(), filename)
    open(file_path, "a").close()


def test_remove_pba_files():
    create_custom_pba_file("linux_file")
    create_custom_pba_file("windows_file")

    custom_pda_dir_contents = os.listdir(PostBreachFilesService.get_custom_pba_directory())
    assert len(custom_pda_dir_contents) == 2

    PostBreachFilesService.remove_PBA_files()

    custom_pda_dir_contents = os.listdir(PostBreachFilesService.get_custom_pba_directory())
    assert len(custom_pda_dir_contents) == 0
