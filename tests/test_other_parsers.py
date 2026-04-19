from nhvrcontrib.section_parsers import (
    parse_nhvas_info,
    parse_permit_types,
    parse_speed_limits,
)


def test_parse_speed_limits():
    html = """
    <html><head><title>Speeding | NHVR</title></head>
    <body>
      <main>
        <p>Heavy vehicle speed compliance info.</p>
        <h2>Speed limiters</h2>
        <p>Vehicles over 12t GVM must have a speed limiter.</p>
        <h2>Enforcement</h2>
        <p>Speeding enforcement details.</p>
      </main>
    </body></html>
    """
    parsed = parse_speed_limits(html)
    assert parsed.title == "Speeding | NHVR"
    assert "Speed limiters" in parsed.sections
    assert "Enforcement" in parsed.sections


def test_parse_nhvas_info():
    html = """
    <html><head><title>NHVAS | NHVR</title></head>
    <body>
      <main>
        <p>Process for recognising operators with safety systems.</p>
        <h2>About NHVAS</h2>
        <p>NHVAS overview content.</p>
        <h2>Apply for NHVAS</h2>
        <p>How to apply for NHVAS modules.</p>
      </main>
    </body></html>
    """
    parsed = parse_nhvas_info(html)
    assert parsed.title == "NHVAS | NHVR"
    assert "About NHVAS" in parsed.sections
    assert "Apply for NHVAS" in parsed.sections


def test_parse_permit_types():
    html = """
    <html><head><title>Access permits | NHVR</title></head>
    <body>
      <main>
        <p>Permits for vehicles exceeding standard limits.</p>
        <h2>Class 1 permits</h2>
        <p>Special purpose vehicle permits.</p>
        <h2>Class 2 notices</h2>
        <p>General access notices.</p>
      </main>
    </body></html>
    """
    parsed = parse_permit_types(html)
    assert parsed.title == "Access permits | NHVR"
    assert "Class 1 permits" in parsed.sections
    assert "Class 2 notices" in parsed.sections


def test_parse_speed_limits_empty():
    html = "<html><head></head><body></body></html>"
    parsed = parse_speed_limits(html)
    assert parsed.title == "Speed limits"
    assert parsed.sections == {}


def test_parse_nhvas_info_empty():
    html = "<html><head></head><body></body></html>"
    parsed = parse_nhvas_info(html)
    assert parsed.title == "NHVAS"
    assert parsed.sections == {}


def test_parse_permit_types_empty():
    html = "<html><head></head><body></body></html>"
    parsed = parse_permit_types(html)
    assert parsed.title == "Access permits"
    assert parsed.sections == {}
