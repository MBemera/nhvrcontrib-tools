"""Topic matching for NHVR search queries."""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class SearchTopic:
    key: str
    title: str
    url: str
    aliases: tuple[str, ...]
    scraper_name: str | None
    knowledge_key: str | None = None


@dataclass(frozen=True)
class TopicMatch:
    topic: SearchTopic
    alias: str
    score: float


SEARCH_TOPICS: tuple[SearchTopic, ...] = (
    SearchTopic(
        key="fatigue",
        title="Fatigue Management",
        url="https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/work-and-rest-requirements",
        aliases=(
            "fatigue",
            "fatigue management",
            "work rest",
            "work and rest",
            "rest break",
            "rest breaks",
            "work diary",
            "bfm",
            "afm",
            "standard hours",
            "basic fatigue management",
            "advanced fatigue management",
        ),
        scraper_name="scrape_fatigue_management",
        knowledge_key="fatigue_rules",
    ),
    SearchTopic(
        key="mass_limits",
        title="Mass Limits",
        url="https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits",
        aliases=(
            "mass",
            "mass limit",
            "mass limits",
            "axle mass",
            "axle limits",
            "gross mass",
            "b double mass",
            "b-double mass",
            "b double gross",
            "higher mass limits",
            "hml",
        ),
        scraper_name="scrape_mass_limits",
        knowledge_key="mass_limits",
    ),
    SearchTopic(
        key="dimension_requirements",
        title="Dimension Requirements",
        url="https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements",
        aliases=(
            "dimension",
            "dimensions",
            "dimension limits",
            "height limit",
            "width limit",
            "length limit",
            "rear overhang",
            "front overhang",
            "ground clearance",
        ),
        scraper_name="scrape_dimension_requirements",
        knowledge_key="dimension_limits",
    ),
    SearchTopic(
        key="chain_of_responsibility",
        title="Chain of Responsibility",
        url="https://www.nhvr.gov.au/safety-accreditation-compliance/chain-of-responsibility",
        aliases=(
            "chain of responsibility",
            "cor",
            "loader duty",
            "loader duties",
            "executive due diligence",
            "due diligence",
            "primary duty",
            "operator duty",
            "operator duties",
            "consignor duty",
            "consignee duty",
            "packer duty",
            "loading manager",
        ),
        scraper_name="scrape_cor_duties",
        knowledge_key="cor_duties",
    ),
    SearchTopic(
        key="breach_categories",
        title="Breach Categories",
        url="https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/breach-categorisation",
        aliases=(
            "breach",
            "breaches",
            "breach categories",
            "breach categorisation",
            "mass breach",
            "mass breach categories",
            "fatigue breach",
            "fatigue breach categories",
            "dimension breach",
            "dimension breach categories",
        ),
        scraper_name="scrape_breach_categorisation",
        knowledge_key="breach_categories",
    ),
    SearchTopic(
        key="speed_compliance",
        title="Speed Compliance",
        url="https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/speeding",
        aliases=(
            "speed",
            "speeding",
            "speed limit",
            "speed limits",
            "speed limiter",
            "100 kmh",
            "100 km h",
        ),
        scraper_name="scrape_speed_limits",
        knowledge_key="speed_limits",
    ),
    SearchTopic(
        key="accreditation",
        title="NHVAS Accreditation",
        url="https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme",
        aliases=(
            "nhvas",
            "accreditation",
            "mass management accreditation",
            "fatigue management accreditation",
            "fatigue accreditation",
            "maintenance management",
            "nhvas fatigue",
            "nhvas fatigue accreditation",
            "nhvas mass",
            "nhvas mass accreditation",
            "nhvas maintenance accreditation",
        ),
        scraper_name="scrape_nhvas_info",
        knowledge_key="accreditation_info",
    ),
    SearchTopic(
        key="permits",
        title="Access Permits",
        url="https://www.nhvr.gov.au/road-access/access-permits",
        aliases=(
            "permit",
            "permits",
            "oversize permit",
            "oversize permits",
            "overmass permit",
            "class 1 permit",
            "class 2 permit",
            "class 3 permit",
            "oversize",
        ),
        scraper_name="scrape_permit_types",
        knowledge_key="permit_types",
    ),
    SearchTopic(
        key="law_and_regulations",
        title="HVNL and Regulations",
        url="https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations",
        aliases=(
            "hvnl",
            "heavy vehicle national law",
            "law",
            "regulations",
        ),
        scraper_name=None,
        knowledge_key=None,
    ),
    SearchTopic(
        key="pbs",
        title="Performance Based Standards",
        url="https://www.nhvr.gov.au/road-access/performance-based-standards",
        aliases=(
            "pbs",
            "performance based standards",
        ),
        scraper_name=None,
        knowledge_key=None,
    ),
)


def normalize_search_query(value: str) -> str:
    compact_value = re.sub(r"[^a-z0-9]+", " ", value.lower())
    return " ".join(compact_value.split())


def find_topic_match(query: str) -> TopicMatch | None:
    normalized_query = normalize_search_query(query)
    if not normalized_query:
        return None

    best_match: TopicMatch | None = None
    for topic in SEARCH_TOPICS:
        for alias in topic.aliases:
            score = _score_alias_match(normalized_query, alias)
            candidate_match = TopicMatch(topic=topic, alias=alias, score=score)
            if best_match is None or _match_priority(candidate_match) > _match_priority(best_match):
                best_match = candidate_match

    if best_match and best_match.score >= 0.55:
        return best_match
    return None


def suggest_topics(query: str, limit: int = 3) -> list[dict[str, str]]:
    normalized_query = normalize_search_query(query)
    scored_topics: list[TopicMatch] = []
    for topic in SEARCH_TOPICS:
        best_alias = max(topic.aliases, key=lambda alias: _score_alias_match(normalized_query, alias))
        scored_topics.append(
            TopicMatch(
                topic=topic,
                alias=best_alias,
                score=_score_alias_match(normalized_query, best_alias),
            )
        )

    suggestions: list[dict[str, str]] = []
    for match in sorted(scored_topics, key=_match_priority, reverse=True)[:limit]:
        suggestions.append(
            {
                "topic": match.topic.title,
                "matched_alias": match.alias,
                "url": match.topic.url,
            }
        )
    return suggestions


def _score_alias_match(normalized_query: str, alias: str) -> float:
    normalized_alias = normalize_search_query(alias)
    if not normalized_query:
        return 0.0
    if normalized_query == normalized_alias:
        return 1.0
    if normalized_alias in normalized_query:
        return 0.95
    if normalized_query in normalized_alias:
        return 0.9

    query_tokens = set(normalized_query.split())
    alias_tokens = set(normalized_alias.split())
    token_score = 0.0
    if query_tokens and alias_tokens:
        shared_tokens = len(query_tokens & alias_tokens)
        if shared_tokens:
            token_score = shared_tokens / len(alias_tokens)

    similarity = difflib.SequenceMatcher(None, normalized_query, normalized_alias).ratio()
    return max(token_score * 0.85, similarity * 0.75)


def _match_priority(match: TopicMatch) -> tuple[float, int, int]:
    normalized_alias = normalize_search_query(match.alias)
    return (
        match.score,
        len(normalized_alias.split()),
        len(normalized_alias),
    )
