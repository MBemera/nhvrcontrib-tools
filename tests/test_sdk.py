"""Tests for the NHVR Python SDK."""

from nhvr_mcp import NHVR


def test_fatigue_rules_default():
    client = NHVR()
    rules = client.fatigue_rules()
    assert "summary" in rules
    assert "solo_driver" in rules
    assert "provenance" in rules


def test_fatigue_rules_bfm():
    client = NHVR()
    rules = client.fatigue_rules(scheme="bfm")
    assert "requirement" in rules


def test_fatigue_rules_unknown():
    client = NHVR()
    result = client.fatigue_rules(scheme="nonexistent")
    assert "error" in result


def test_mass_limits_general():
    client = NHVR()
    limits = client.mass_limits()
    assert "general" in limits
    assert "hml" not in limits


def test_mass_limits_with_hml():
    client = NHVR()
    limits = client.mass_limits(include_hml=True)
    assert "general" in limits
    assert "hml" in limits


def test_dimension_limits():
    client = NHVR()
    dims = client.dimension_limits()
    assert "height" in dims
    assert "width" in dims
    assert "length" in dims


def test_breach_categories_all():
    client = NHVR()
    breaches = client.breach_categories()
    assert "mass" in breaches
    assert "fatigue" in breaches


def test_breach_categories_filtered():
    client = NHVR()
    breaches = client.breach_categories(breach_type="mass")
    assert "mass" in breaches
    assert "provenance" in breaches


def test_speed_limits():
    client = NHVR()
    speed = client.speed_limits()
    assert "default" in speed


def test_cor_duties_all():
    client = NHVR()
    cor = client.cor_duties()
    assert "primary_duty" in cor


def test_cor_duties_filtered():
    client = NHVR()
    cor = client.cor_duties(role="operator")
    assert "operator" in cor
    assert "provenance" in cor


def test_accreditation_all():
    client = NHVR()
    accred = client.accreditation()
    assert "mass" in accred


def test_accreditation_filtered():
    client = NHVR()
    accred = client.accreditation(module="mass")
    assert "mass" in accred
    assert "provenance" in accred


def test_permit_types_all():
    client = NHVR()
    permits = client.permit_types()
    assert "class_1" in permits


def test_permit_types_filtered():
    client = NHVR()
    permits = client.permit_types(permit_type="class_1")
    assert "class_1" in permits
    assert "provenance" in permits


def test_hml_info():
    client = NHVR()
    hml = client.hml_info()
    assert "eligibility" in hml
    assert "limits" in hml


def test_api_key_from_constructor():
    client = NHVR(api_key="test-key")
    assert client.api_key == "test-key"


def test_api_key_default_none():
    client = NHVR()
    # Will be None unless NHVR_API_KEY env var is set
    assert client.api_key is None or isinstance(client.api_key, str)
