"""Unit tests for core functions."""

import os
import tempfile

import pytest

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
        valid_file = os.path.join(test_resources.FIXTURES, "rest_docs.py")
        invalid_file = os.path.join(test_resources.FIXTURES, "jython_script")
        files = docconvert.core.find_python_files(test_resources.FIXTURES)
        assert len(files) == 8
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
        invalid_file = os.path.join(test_resources.FIXTURES, "rest_docs.py")
        files = docconvert.core.find_python_files(
            test_resources.FIXTURES, file_ext=".txt"
        )
        assert len(files) == 2
        assert valid_file in files
        assert invalid_file not in files


class TestConvert(object):
    @pytest.mark.parametrize(
        "input,output",
        [
            ("rest", "google"),
            ("rest", "numpy"),
            ("rest", "epytext"),
            ("rest", "rest"),
            ("epytext", "google"),
            ("epytext", "numpy"),
            ("epytext", "epytext"),
            ("epytext", "rest"),
        ],
    )
    def test_convert(self, input, output):
        input_path = os.path.join(test_resources.FIXTURES, "{0}_docs.py".format(input))
        output_path = os.path.join(
            test_resources.FIXTURES, "{0}_docs.py".format(output)
        )
        convert_path = make_temp_file_copy(input_path)
        config = docconvert.configuration.DocconvertConfiguration.create_default()
        config.input_style = input
        config.output_style = output
        try:
            docconvert.core.convert_file(convert_path, config, in_place=True)
            with open(output_path) as expected:
                with open(convert_path) as converted:
                    assert converted.readlines() == expected.readlines()
        finally:
            os.remove(convert_path)


def make_temp_file_copy(source_path):
    """Make a temporary file that is a copy of the source file."""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with open(source_path, "r+b") as src_file:
        temp_file.writelines(src_file.readlines())
    temp_file.close()  # close the file handler so we can reopen later
    return temp_file.name
