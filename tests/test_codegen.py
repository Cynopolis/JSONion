import subprocess
from pathlib import Path
import filecmp
import pytest

ROOT_DIR = Path(__file__).parent.parent
BUILDER_SCRIPT = ROOT_DIR / "builder.py"
FIXTURES_INPUT = ROOT_DIR / "tests/fixtures/input"
FIXTURES_EXPECTED = ROOT_DIR / "tests/fixtures/expected"
BUILD_DIR = ROOT_DIR / "tests/build"


def run_builder(source_dir: Path, build_dir: Path):
    """Run builder.py to generate all code."""
    subprocess.run(
        ["python3", str(BUILDER_SCRIPT), "-s",
         str(source_dir), "-b", str(build_dir)],
        check=True,
    )


def compare_dirs(expected_dir: Path, actual_dir: Path):
    """Recursively compare two directories and raise an assertion if there are differences."""
    comparison = filecmp.dircmp(expected_dir, actual_dir)

    # Any files missing in actual_dir?
    if comparison.left_only:
        raise AssertionError(f"Missing files in build: {comparison.left_only}")

    # Any unexpected files?
    if comparison.right_only:
        raise AssertionError(
            f"Unexpected files in build: {comparison.right_only}")

    # Check differing files
    if comparison.diff_files:
        diffs = []
        for f in comparison.diff_files:
            expected_file = expected_dir / f
            actual_file = actual_dir / f
            expected_text = expected_file.read_text(encoding="utf-8")
            actual_text = actual_file.read_text(encoding="utf-8")
            diffs.append(
                f"\nFile: {f}\nExpected:\n{expected_text}\nActual:\n{actual_text}\n")
        raise AssertionError("Files differ:\n" + "\n".join(diffs))

    # Recurse into subdirectories
    for subdir in comparison.common_dirs:
        compare_dirs(expected_dir / subdir, actual_dir / subdir)


def test_codegen_all(tmp_path):
    # 1️⃣ Run builder.py
    run_builder(FIXTURES_INPUT, tmp_path)

    # 2️⃣ Compare entire build folder with expected fixtures
    compare_dirs(FIXTURES_EXPECTED, tmp_path)
