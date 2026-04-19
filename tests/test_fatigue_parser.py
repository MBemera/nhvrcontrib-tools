from nhvrcontrib.section_parsers import parse_fatigue_management


def test_parse_fatigue_management_basic():
    html = """
    <html><head><title>Work and rest requirements | NHVR</title></head>
    <body>
      <main>
        <p>Work and rest hours for fatigue-regulated heavy vehicles.</p>
        <h2>Standard hours</h2>
        <p>Standard hours apply to all drivers without accreditation.</p>
        <h3>Solo drivers</h3>
        <p>Solo driver work/rest table content.</p>
        <h3>Two-up drivers</h3>
        <p>Two-up driver work/rest table content.</p>
        <h2>Basic Fatigue Management (BFM)</h2>
        <p>BFM gives operators more flexible hours.</p>
        <h3>BFM Solo drivers</h3>
        <p>BFM solo driver requirements.</p>
        <h2>Advanced Fatigue Management (AFM)</h2>
        <p>AFM provides tailored work and rest hours.</p>
      </main>
    </body></html>
    """
    parsed = parse_fatigue_management(html)
    assert parsed.title == "Work and rest requirements | NHVR"
    assert "fatigue" in parsed.intro.lower() or "work" in parsed.intro.lower()
    assert "Standard hours" in parsed.sections
    assert "Basic Fatigue Management (BFM)" in parsed.sections
    assert "Advanced Fatigue Management (AFM)" in parsed.sections
    # Check sub-sections
    assert "Standard hours" in parsed.sub_sections
    assert "Solo drivers" in parsed.sub_sections["Standard hours"]
    assert "Two-up drivers" in parsed.sub_sections["Standard hours"]
    assert "Basic Fatigue Management (BFM)" in parsed.sub_sections
    assert "BFM Solo drivers" in parsed.sub_sections["Basic Fatigue Management (BFM)"]


def test_parse_fatigue_management_empty():
    html = "<html><head></head><body></body></html>"
    parsed = parse_fatigue_management(html)
    assert parsed.title == "Fatigue management"
    assert parsed.sections == {}
    assert parsed.sub_sections == {}
