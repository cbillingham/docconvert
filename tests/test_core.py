"""Unit tests for core functions."""

import os
import tempfile

import docconvert

# local
from . import test_resources


class TestShebangScripts(object):
    def test_python_script(self):
        valid_script = os.path.join(test_resources.FIXTURES, "python_script")
        assert docconvert.core.has_python_shebang(valid_script) is True

    def test_invalid_script(self):
        invalid_script = os.path.join(test_resources.FIXTURES, "jython_script")
        assert docconvert.core.has_python_shebang(invalid_script) is False

    def test_custom_shebangs(self):
        valid_scripts = [
            os.path.join(test_resources.FIXTURES, script)
            for script in ["python_script", "jython_script"]
        ]
        custom_shebangs = ["python", "jython"]
        for script in valid_scripts:
            is_script = docconvert.core.has_python_shebang(
                script, accepted_shebangs=custom_shebangs
            )
            assert is_script is True


class TestFindPythonFiles(object):
    def test_correctly_identify_files(self):
        valid_file = os.path.join(test_resources.FIXTURES, "reST_docs.py")
        invalid_file = os.path.join(test_resources.FIXTURES, "jython_script")
        files = docconvert.core.find_python_files(test_resources.FIXTURES)
        assert len(files) == 7
        assert valid_file in files
        assert invalid_file not in files

    def test_correctly_identify_nested_files(self):
        valid_file = os.path.join(
            test_resources.FIXTURES, "test_nested_dir/nested_file.py"
        )
        invalid_file = os.path.join(
            test_resources.FIXTURES, "test_nested_dir/nested_file.txt"
        )
        files = docconvert.core.find_python_files(test_resources.FIXTURES)
        assert valid_file in files
        assert invalid_file not in files

    def test_file_ext(self):
        valid_file = os.path.join(test_resources.FIXTURES, "python_script")
        invalid_file = os.path.join(test_resources.FIXTURES, "reST_docs.py")
        files = docconvert.core.find_python_files(
            test_resources.FIXTURES, file_ext=".txt"
        )
        assert len(files) == 2
        assert valid_file in files
        assert invalid_file not in files


class TestConvert(object):
    def test_convert_rest_to_google(self):
        rest_path = os.path.join(test_resources.FIXTURES, "reST_docs.py")
        google_path = os.path.join(test_resources.FIXTURES, "google_docs.py")
        temp_rest_path = make_temp_file_copy(rest_path)
        config = docconvert.configuration.DocconvertConfiguration.create_default()
        config.input_style = "rest"
        config.output_style = "google"
        try:
            docconvert.core.convert_file(temp_rest_path, config, in_place=True)
            with open(google_path) as google_file:
                with open(temp_rest_path) as temp_rest_file:
                    assert google_file.readlines() == temp_rest_file.readlines()
        finally:
            os.remove(temp_rest_path)

    def test_convert_epytext_to_google(self):
        epytext_path = os.path.join(test_resources.FIXTURES, "epytext_docs.py")
        google_path = os.path.join(test_resources.FIXTURES, "google_docs.py")
        temp_epytext_path = make_temp_file_copy(epytext_path)
        config = docconvert.configuration.DocconvertConfiguration.create_default()
        config.input_style = "epytext"
        config.output_style = "google"
        try:
            docconvert.core.convert_file(temp_epytext_path, config, in_place=True)
            with open(google_path) as google_file:
                with open(temp_epytext_path) as temp_epytext_file:
                    assert google_file.readlines() == temp_epytext_file.readlines()
        finally:
            os.remove(temp_epytext_path)


def make_temp_file_copy(source_path):
    """Make a temporary file that is a copy of the source file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(source_path, "r+b") as src_file:
        temp_file.writelines(src_file.readlines())
    temp_file.close()  # close the file handler so we can reopen later
    return temp_file.name
