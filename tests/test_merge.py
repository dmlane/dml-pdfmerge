""" Test that merge works as expected """
import os
import tempfile
from importlib.metadata import version
from unittest.mock import patch

import pytest
from pypdf import PdfReader

from pdfmerge import MyException, PdfMerge


def test_version_setup(capsys):
    """Test that the version number is set up correctly"""
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch("sys.argv", ["pdfmerge.py", "-V"]):
            PdfMerge()
    result = capsys.readouterr()
    assert result.out == version("dml-pdfmerge") + "\n"
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_merge1_bad(capsys):
    """Test that merge works as expected"""
    resource_path = os.path.dirname(os.path.realpath(__file__)) + "/testresources/"
    infile1 = resource_path + "doc1.pdf"
    output_file = tempfile.gettempdir() + "/results_test_merge1.pdf"

    with pytest.raises(SystemExit) as pytest_wrapped_e:
        with patch(
            "sys.argv",
            [
                "pdfmerge.py",
                "-i",
                infile1,
                output_file,
            ],
        ):
            PdfMerge().run()
    result = capsys.readouterr()
    assert "usage: pdfmerge.py" in result.out

    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
    assert not os.path.exists(output_file)


def test_merge2(capsys):
    """Test that merge works as expected"""
    resource_path = os.path.dirname(os.path.realpath(__file__)) + "/testresources/"
    infile1 = resource_path + "doc1.pdf"
    infile2 = resource_path + "doc2.pdf"
    output_file = tempfile.gettempdir() + "/results_test_merge2.pdf"
    with patch(
        "sys.argv",
        [
            "pdfmerge.py",
            "-i",
            infile1,
            "-i",
            infile2,
            output_file,
        ],
    ):
        PdfMerge().run()
    assert os.path.exists(output_file)
    result = capsys.readouterr()
    assert result.out == f"Output file {output_file} created\n"


def test_merge2_bad():
    """Test that merge works as expected"""
    resource_path = os.path.dirname(os.path.realpath(__file__)) + "/testresources/"
    infile1 = resource_path + "doc1.pdf"
    infile2 = resource_path + "doc2.pdf"
    output_file = tempfile.gettempdir() + "/results_test_merge2.pdf"
    with pytest.raises(MyException) as excinfo:
        with patch(
            "sys.argv",
            [
                "pdfmerge.py",
                "-i",
                infile1,
                "-i",
                infile2,
                output_file,
            ],
        ):
            PdfMerge().run()

    assert (
        str(excinfo.value)
        == f"Output file {output_file} already exists (Use '--overwrite' if neccessary)"
    )


def test_merge2_overwrite(capsys):
    """Test that merge works as expected"""
    resource_path = os.path.dirname(os.path.realpath(__file__)) + "/testresources/"
    infile1 = resource_path + "doc1.pdf"
    infile2 = resource_path + "doc2.pdf"
    output_file = tempfile.gettempdir() + "/results_test_merge2.pdf"

    with patch(
        "sys.argv",
        [
            "pdfmerge.py",
            "-i",
            infile1,
            "-i",
            infile2,
            "--overwrite",
            output_file,
        ],
    ):
        PdfMerge().run()
    os.remove(output_file)

    result = capsys.readouterr()
    assert result.out == f"Output file {output_file} created\n"


def test_merge3_pages(capsys):
    """Test that merge works as expected"""
    resource_path = os.path.dirname(os.path.realpath(__file__)) + "/testresources/"
    infile1 = resource_path + "doc1.pdf"
    infile2 = resource_path + "doc2.pdf"
    output_file = tempfile.gettempdir() + "/results_test_merge2.pdf"

    with patch(
        "sys.argv",
        [
            "pdfmerge.py",
            "-i",
            infile1,
            "-i",
            infile2,
            "-i",
            infile2,
            "--overwrite",
            output_file,
        ],
    ):
        PdfMerge().run()
    reader = PdfReader(output_file)
    num_pages = len(reader.pages)
    os.remove(output_file)

    result = capsys.readouterr()
    assert result.out == f"Output file {output_file} created\n"
    assert num_pages == 3
