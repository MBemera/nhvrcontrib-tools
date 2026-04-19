from nhvrcontrib.section_parsers import parse_dimension_requirements


def test_parse_dimension_requirements_basic():
    html = """
    <html><head><title>Dimension requirements | NHVR</title></head>
    <body>
      <main>
        <p>Intro text here.</p>
        <h2>Height</h2>
        <p>Height content.</p>
        <h2>Length</h2>
        <p>Length content.</p>
      </main>
    </body></html>
    """
    parsed = parse_dimension_requirements(html)
    assert parsed.title == "Dimension requirements | NHVR"
    assert parsed.intro == "Intro text here."
    assert parsed.sections["Height"] == "Height content."
    assert parsed.sections["Length"] == "Length content."
