from nhvrcontrib.section_parsers import parse_mass_limits


def test_parse_mass_limits_basic():
    html = """
    <html><head><title>Mass limits | NHVR</title></head>
    <body>
      <main>
        <p>Intro text here.</p>
        <h2>General Mass Limits (GML)</h2>
        <p>GML content.</p>
        <h2>Higher Mass Limits (HML)</h2>
        <p>HML content.</p>
      </main>
    </body></html>
    """
    parsed = parse_mass_limits(html)
    assert parsed.title == "Mass limits | NHVR"
    assert parsed.intro == "Intro text here."
    assert parsed.sections["General Mass Limits (GML)"] == "GML content."
    assert parsed.sections["Higher Mass Limits (HML)"] == "HML content."
