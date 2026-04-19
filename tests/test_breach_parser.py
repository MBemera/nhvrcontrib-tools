from nhvrcontrib.section_parsers import parse_breach_categorisation


def test_parse_breach_categorisation_basic():
    html = """
    <html><head><title>Breach categorisation | NHVR</title></head>
    <body>
      <main>
        <p>Under the HVNL, breaches are categorised based on risk.</p>
        <h2>Categories of breaches</h2>
        <p>Minor, Substantial, Severe, Critical (fatigue only).</p>
        <h2>Mass</h2>
        <p>Mass breach overview.</p>
        <h3>Breach categories</h3>
        <p>Mass breach categories proportionate to risk.</p>
        <h3>Vehicles operating under a notice or permit</h3>
        <p>If a vehicle breaches a mass condition...</p>
        <h2>Dimension</h2>
        <p>Dimension breach overview.</p>
        <h3>Breach categories</h3>
        <p>Dimension breach categories.</p>
        <h2>Fatigue</h2>
        <p>Fatigue breach overview.</p>
        <h3>Breach categories</h3>
        <p>Minor, Substantial, Severe, Critical.</p>
      </main>
    </body></html>
    """
    parsed = parse_breach_categorisation(html)
    assert parsed.title == "Breach categorisation | NHVR"
    assert "HVNL" in parsed.intro or "breach" in parsed.intro.lower()
    assert "Categories of breaches" in parsed.sections
    assert "Mass" in parsed.sections
    assert "Dimension" in parsed.sections
    assert "Fatigue" in parsed.sections
    # Check sub-sections exist for Mass, Dimension, Fatigue
    assert "Mass" in parsed.sub_sections
    assert "Breach categories" in parsed.sub_sections["Mass"]
    assert "Dimension" in parsed.sub_sections
    assert "Fatigue" in parsed.sub_sections


def test_parse_breach_categorisation_empty():
    html = "<html><head></head><body></body></html>"
    parsed = parse_breach_categorisation(html)
    assert parsed.title == "Breach categorisation"
    assert parsed.sections == {}
