from orchestrator import output


def test_slugify_basic():
    assert output.slugify("New Trailer!") == "new-trailer"
    assert output.slugify("  multiple   spaces ") == "multiple-spaces"


def test_slugify_empty_falls_back():
    assert output.slugify("!!!") == "draft"


def test_save_draft_writes_file(tmp_path):
    path = output.save_draft(
        "short_video", "hello world", output_dir=tmp_path, timestamp=123
    )
    assert path == tmp_path / "123-short-video.md"
    assert path.read_text(encoding="utf-8") == "hello world"


def test_save_draft_creates_missing_dir(tmp_path):
    target = tmp_path / "nested" / "out"
    path = output.save_draft("email_blast", "body", output_dir=target, timestamp=1)
    assert path.exists()
    assert path.parent == target
