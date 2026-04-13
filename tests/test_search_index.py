from nhvr_mcp.search_index import find_topic_match


def test_find_topic_match_prefers_exact_afm_alias() -> None:
    match = find_topic_match("afm")

    assert match is not None
    assert match.topic.title == "Fatigue Management"
    assert match.alias == "afm"
