from nhvrcontrib.section_parsers import parse_cor_duties, parse_cor_sub_page


def test_parse_cor_duties_basic():
    html = """
    <html><head><title>Chain of Responsibility | NHVR</title></head>
    <body>
      <main>
        <p>The CoR makes parties other than drivers responsible.</p>
        <h2>The primary duty</h2>
        <p>The obligation to ensure safety of transport activities.</p>
        <h2>Executive duty and due diligence</h2>
        <p>Executives must exercise due diligence.</p>
        <h2>Other duties</h2>
        <p>Drivers have other duties under the HVNL.</p>
        <a href="/safety-accreditation-compliance/chain-of-responsibility/primary-duty">Primary duty</a>
        <a href="/safety-accreditation-compliance/chain-of-responsibility/other-duties">Other duties</a>
      </main>
    </body></html>
    """
    parsed = parse_cor_duties(html)
    assert parsed.title == "Chain of Responsibility | NHVR"
    assert "CoR" in parsed.intro
    assert "The primary duty" in parsed.sections
    assert "Executive duty and due diligence" in parsed.sections
    assert "Other duties" in parsed.sections
    assert len(parsed.sub_pages) >= 2


def test_parse_cor_sub_page():
    html = """
    <html><head><title>Primary duty | NHVR</title></head>
    <body>
      <main>
        <p>Intro text.</p>
        <h2>Parties in the CoR</h2>
        <p>You are a party because of a function you perform.</p>
        <h2>Primary duty scope</h2>
        <p>Learn about shared responsibilities.</p>
      </main>
    </body></html>
    """
    sections = parse_cor_sub_page(html)
    assert "Parties in the CoR" in sections
    assert "Primary duty scope" in sections


def test_parse_cor_duties_empty():
    html = "<html><head><title>Empty</title></head><body></body></html>"
    parsed = parse_cor_duties(html)
    assert parsed.title == "Empty"
    assert parsed.sections == {}
