import importlib.util
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "transcribe_speakers.py"
SPEC = importlib.util.spec_from_file_location("transcribe_speakers", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_merge_turns_filters_noise_and_merges_adjacent_speaker():
    segments = [
        {"start": 0.0, "end": 0.1, "speaker": "S0"},
        {"start": 0.2, "end": 1.0, "speaker": "S1"},
        {"start": 1.3, "end": 2.0, "speaker": "S1"},
        {"start": 2.1, "end": 3.0, "speaker": "S0"},
    ]

    assert MODULE.merge_turns(segments, min_duration=0.2, max_gap=0.5) == [
        {"start": 0.2, "end": 2.0, "speaker": "S1"},
        {"start": 2.1, "end": 3.0, "speaker": "S0"},
    ]


def test_speaker_mapping_uses_first_substantial_appearance():
    segments = [
        {"start": 0.0, "end": 0.2, "speaker": "S0"},
        {"start": 0.3, "end": 1.5, "speaker": "S1"},
        {"start": 1.5, "end": 2.2, "speaker": "S0"},
    ]

    assert MODULE.speaker_mapping(segments, None) == {
        "S1": "说话人 A",
        "S0": "说话人 B",
    }
    assert MODULE.speaker_mapping(segments, ["付老师", "我"]) == {
        "S1": "付老师",
        "S0": "我",
    }


def test_timestamp_supports_hour_long_audio():
    assert MODULE.timestamp(61.8) == "01:01"
    assert MODULE.timestamp(3661.2) == "01:01:01"


def test_resolve_python_preserves_virtualenv_symlink(tmp_path):
    base_python = tmp_path / "base-python"
    base_python.touch()
    venv_python = tmp_path / "venv-python"
    venv_python.symlink_to(base_python)

    assert MODULE.resolve_python(str(venv_python), "TEST_PYTHON", base_python) == venv_python


def test_default_asr_python_prefers_persistent_runtime(tmp_path, monkeypatch):
    runtime = tmp_path / ".venvs" / "qwen3-asr-mlx" / "bin" / "python"
    runtime.parent.mkdir(parents=True)
    runtime.touch()
    monkeypatch.setenv("MODELS_DIR", str(tmp_path))

    assert MODULE.default_asr_python() == runtime
