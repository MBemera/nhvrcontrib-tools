from nhvr_mcp.knowledge import ACCREDITATION_INFO, DIMENSION_LIMITS, FATIGUE_RULES, HML_INFO, MASS_LIMITS, PERMIT_TYPES


def test_standard_two_up_rules_match_current_nhvr_guidance() -> None:
    rules = FATIGUE_RULES["standard"]["two_up_driver"]

    assert "5 continuous hours" in rules["in_any_24_hours"]
    assert rules["in_any_52_hours"].startswith("No work cap specified")
    assert "Max 60 hours work" in rules["in_any_7_days"]
    assert "Max 120 hours work" in rules["in_any_14_days"]


def test_bfm_rules_match_current_nhvr_guidance() -> None:
    solo_rules = FATIGUE_RULES["bfm"]["solo_driver"]
    two_up_rules = FATIGUE_RULES["bfm"]["two_up_driver"]

    assert solo_rules["in_any_9_hours"].startswith("Max 8 hours 30 min work")
    assert solo_rules["in_any_12_hours"].startswith("Max 11 hours work")
    assert two_up_rules["in_any_24_hours"].startswith("Max 14 hours work")
    assert two_up_rules["in_any_82_hours"].startswith("No work cap specified")
    assert "Max 70 hours work" in two_up_rules["in_any_7_days"]
    assert "Max 140 hours work" in two_up_rules["in_any_14_days"]


def test_hml_limits_match_current_nhvr_guidance() -> None:
    limits = MASS_LIMITS["hml"]
    info_limits = HML_INFO["limits"]

    assert limits["tandem_axle_group"] == "17.0 t"
    assert limits["tri_axle_group"] == "22.5 t"
    assert info_limits["tandem_axle_group"] == "17.0 t"
    assert info_limits["tri_axle_group"] == "22.5 t"


def test_dimension_width_and_height_match_current_nhvr_guidance() -> None:
    assert "Safer Freight Vehicles" in DIMENSION_LIMITS["width"]
    assert "specified semitrailers" in DIMENSION_LIMITS["height"]
    assert "double-decker buses" in DIMENSION_LIMITS["height"]


def test_b_double_length_guidance_is_no_longer_oversimplified() -> None:
    b_double_length = DIMENSION_LIMITS["length"]["b_double"]
    mass_example = MASS_LIMITS["general"]["b_double_26m_example"]

    assert "25.0 m generally" in b_double_length
    assert "26.0 m" in b_double_length
    assert "62.5 t" in mass_example


def test_accreditation_overview_matches_current_transition_guidance() -> None:
    overview = ACCREDITATION_INFO["overview"]

    assert "progressively replaced by the HVA scheme" in overview
    assert "1 July 2026" in overview


def test_permit_summaries_match_current_vehicle_class_guidance() -> None:
    assert "B-doubles" in PERMIT_TYPES["class_2"]["summary"]
    assert "does not comply with prescribed mass or dimension requirements" in PERMIT_TYPES["class_3"]["summary"]
