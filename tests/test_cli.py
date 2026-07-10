"""Tests for the orchestrator CLI."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from orchestrator.__main__ import main

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def test_cli_list_exits_zero(capsys) -> None:
    assert main(["--list"]) == 0
    captured = capsys.readouterr()
    assert "gta6_news_drop" in captured.out


def test_cli_blocked_run_exits_one(capsys) -> None:
    code = main(
        [
            "gta6_news_drop",
            "--var",
            "hook=Clean",
            "--var",
            "summary=This leaked build is bad",
            "--var",
            "news_type=trailer",
            "--var",
            "source=https://rockstar.com",
            "--var",
            "cta=Join",
        ]
    )
    assert code == 1
    captured = capsys.readouterr()
    summary = json.loads(captured.out)
    assert summary["blocked"] is True


def test_cli_clean_run_exits_zero(capsys) -> None:
    code = main(
        [
            "gta6_news_drop",
            "--var",
            "hook=Clean hook",
            "--var",
            "summary=Official update",
            "--var",
            "news_type=trailer",
            "--var",
            "source=https://rockstar.com",
            "--var",
            "cta=Join",
        ]
    )
    assert code == 0


def test_cli_bad_var_exits_nonzero() -> None:
    with pytest.raises(SystemExit) as exc:
        main(["gta6_news_drop", "--var", "badformat"])
    assert exc.value.code != 0


def test_cli_out_writes_file(tmp_path, capsys, monkeypatch) -> None:
    def _save(event: str, content: str, **kwargs):
        path = tmp_path / f"{event}.md"
        path.write_text(content, encoding="utf-8")
        return path

    monkeypatch.setattr("orchestrator.__main__.output.save_draft", _save)
    code = main(
        [
            "gta6_news_drop",
            "--out",
            "--var",
            "hook=Test",
            "--var",
            "summary=Official",
            "--var",
            "news_type=news",
            "--var",
            "source=https://rockstar.com",
            "--var",
            "cta=Join",
        ]
    )
    assert code == 0
    assert list(tmp_path.glob("*.md"))


def test_cli_module_invocation() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "orchestrator", "--list"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0
    assert "product_launch" in result.stdout
