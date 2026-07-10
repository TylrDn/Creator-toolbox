from orchestrator import templates


def test_render_replaces_known_variables():
    out = templates.render("Play {game} on {platforms}", {"game": "GTA VI", "platforms": "PC"})
    assert out == "Play GTA VI on PC"


def test_render_leaves_unknown_placeholders_by_default():
    out = templates.render("Hi {game} {missing}", {"game": "GTA VI"})
    assert out == "Hi GTA VI {missing}"


def test_render_strict_raises_on_unknown():
    import pytest

    with pytest.raises(KeyError):
        templates.render("Hi {missing}", {}, strict=True)


def test_find_placeholders():
    assert templates.find_placeholders("{a} text {b} {a}") == {"a", "b"}


def test_render_file_reads_real_template():
    out = templates.render_file(
        "content/short-video.md", {"game": "Grand Theft Auto VI"}
    )
    assert "Short Video Template" in out
