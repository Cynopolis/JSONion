import subprocess
from pathlib import Path
import json
import pytest
import filecmp
import shutil

# Paths
ROOT_DIR = Path(__file__).parent.parent.resolve()
BUILDER_SCRIPT = ROOT_DIR / "builder.py"
FIXTURES_INPUT = ROOT_DIR / "tests/fixtures/input"
FIXTURES_EXPECTED = ROOT_DIR / "tests/fixtures/expected"
BUILD_DIR = ROOT_DIR / "tests/build"


def run_builder():
    """Run builder.py to generate code in the tests/build folder."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    BUILD_DIR.mkdir(parents=True, exist_ok=True)

    subprocess.run(
        ["python3", str(BUILDER_SCRIPT), "-s",
         str(FIXTURES_INPUT), "-b", str(BUILD_DIR)],
        check=True
    )


def load_json(filename: str):
    """Load a JSON file from the input fixtures."""
    path = FIXTURES_INPUT / filename
    return json.loads(path.read_text(encoding="utf-8"))


def load_expected_file(language: str, filename: str):
    """Load an expected file from fixtures."""
    path = FIXTURES_EXPECTED / language / filename
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="session", autouse=True)
def builder_run():
    """Run builder once per test session before any tests."""
    run_builder()


@pytest.fixture
def build_dir():
    """Return the path to the generated build folder."""
    return BUILD_DIR


@pytest.fixture
def assert_build_matches_expected():
    """
    Fixture to compare generated files with expected fixtures.
    Usage: assert_build_matches_expected(generated_file, language, expected_filename)
    """
    def _assert(generated_file: Path, language: str, expected_filename: str):
        assert generated_file.exists(
        ), f"Generated file not found: {generated_file}"
        generated_content = generated_file.read_text(encoding="utf-8")
        expected_content = load_expected_file(language, expected_filename)
        assert generated_content == expected_content, f"Mismatch in {generated_file.name}"
    return _assert
