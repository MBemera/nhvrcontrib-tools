"""Built-in NHVR knowledge base.

Authoritative data sourced from the NHVR website and HVNL legislation.
Used as quick-lookup fallback when live scraping is not required.
"""

from __future__ import annotations

from copy import deepcopy

LEGISLATION_BASE_URL = "https://www.legislation.qld.gov.au/view/whole/html/inforce/current/act-2012-hvnlq"

FATIGUE_RULES = {
    "standard": {
        "summary": "Standard hours – default work/rest option for all drivers without BFM/AFM accreditation.",
        "section_reference": None,
        "solo_driver": {
            "in_any_5.5_hours": "Max 5 hours 15 min work, then ≥15 min continuous rest",
            "in_any_8_hours": "Max 7 hours 30 min work, then ≥30 min rest in blocks ≥15 min",
            "in_any_11_hours": "Max 10 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 12 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": "Max 72 hours work, then ≥24 continuous hours stationary rest",
            "in_any_14_days": (
                "Max 144 hours work; must have 2 night rest breaks and "
                "2 night rest breaks taken on consecutive days"
            ),
        },
        "two_up_driver": {
            "in_any_5.5_hours": "Max 5 hours 15 min work, then ≥15 min continuous rest",
            "in_any_8_hours": "Max 7 hours 30 min work, then ≥30 min rest in blocks ≥15 min",
            "in_any_11_hours": "Max 10 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": (
                "Max 12 hours work, then ≥5 continuous hours stationary rest or "
                "≥5 continuous hours rest in an approved sleeper berth while the vehicle is moving"
            ),
            "in_any_52_hours": "No work cap specified; must have ≥10 continuous hours stationary rest",
            "in_any_7_days": (
                "Max 60 hours work; must have ≥24 continuous hours stationary rest and "
                "a further 24 hours stationary rest in blocks of at least 7 continuous hours"
            ),
            "in_any_14_days": (
                "Max 120 hours work; must have 2 night rest breaks and "
                "2 night rest breaks taken on consecutive days"
            ),
        },
        "night_rest": "7 continuous hours stationary rest between 10pm and 8am (base time zone).",
    },
    "bfm": {
        "summary": "Basic Fatigue Management – NHVAS module allowing more flexible work/rest hours.",
        "section_reference": None,
        "solo_driver": {
            "in_any_6.25_hours": "Max 6 hours work, then ≥15 min continuous rest",
            "in_any_9_hours": "Max 8 hours 30 min work, then ≥30 min rest in blocks ≥15 min",
            "in_any_12_hours": "Max 11 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 14 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": (
                "Max 36 hours long/night work time; no separate rest minimum is "
                "set for that 7-day period"
            ),
            "in_any_14_days": (
                "Max 144 hours work; must have 24 continuous hours stationary "
                "rest after no more than 84 hours work time, plus a further "
                "24 continuous hours stationary rest, 2 night rest breaks, and "
                "2 night rest breaks taken on consecutive days"
            ),
        },
        "two_up_driver": {
            "in_any_24_hours": "Max 14 hours work; no minimum rest break is set in that 24-hour period",
            "in_any_82_hours": "No work cap specified; must have ≥10 continuous hours stationary rest",
            "in_any_7_days": (
                "Max 70 hours work; must have ≥24 continuous hours stationary rest and "
                "a further 24 hours stationary rest in blocks of at least 7 continuous hours"
            ),
            "in_any_14_days": "Max 140 hours work; must have 4 night rest breaks",
        },
        "requirement": "Operator must hold NHVAS BFM accreditation.",
    },
    "afm": {
        "summary": "Advanced Fatigue Management – tailored work/rest hours via an NHVR-assessed safety case.",
        "section_reference": None,
        "description": (
            "AFM is currently the only mechanism under the HVNL that can provide tailored "
            "work and rest hours. Applications are assessed against fatigue principles, "
            "the operator's proposed controls, and the risks of the specific operation."
        ),
        "requirement": (
            "Operator must hold NHVAS Fatigue Management accreditation with "
            "approved AFM work and rest hours."
        ),
    },
}

MASS_LIMITS = {
    "general": {
        "summary": (
            "General Mass Limits (GML) – default statutory mass limits, subject "
            "to manufacturer and axle spacing limits."
        ),
        "steer_axle": "6.0 t by default; 6.5 t for a complying steer axle vehicle",
        "single_axle_dual_tyres": "9.0 t",
        "tandem_axle_group": "16.5 t",
        "tri_axle_group": "20.0 t",
        "general_access_examples": (
            "Common general access examples include a rigid vehicle up to 31 t, "
            "a prime mover and semitrailer up to 42.5 t, a rigid truck and trailer up to 42.5 t, "
            "and a 19 m B-double up to 42.5 t"
        ),
        "b_double_26m_example": (
            "A 26 m B-double can operate up to 62.5 t under GML if it meets "
            "axle spacing and notice conditions"
        ),
    },
    "cml": {
        "summary": (
            "Concessional Mass Limits (CML) – above GML for eligible vehicles "
            "operating under NHVAS Mass Management."
        ),
        "requirement": (
            "NHVAS Mass Management accreditation and compliance with the CML "
            "axle group tables and gross mass caps."
        ),
        "tandem_axle_group": "17.0 t",
        "tri_axle_group": "21.0 t",
        "gross_mass_concession": (
            "Up to 1 t above GML for a vehicle or combination with allowable gross mass up to 55 t, "
            "or up to 2 t above GML if allowable gross mass exceeds 55 t"
        ),
    },
    "hml": {
        "summary": "Higher Mass Limits (HML) – increased axle group limits for eligible vehicles on authorised routes.",
        "requirement": (
            "Vehicles or combinations running at HML on triaxle groups must be accredited under NHVAS Mass Management, "
            "be fitted with certified road-friendly suspension, and travel on an authorised route"
        ),
        "tandem_axle_group": "17.0 t",
        "tri_axle_group": "22.5 t",
        "single_drive_axle_bus": "10.0 t",
        "six_tyred_tandem_axle_group": "14.0 t",
        "note": "Combination mass still depends on axle spacing, manufacturer limits, and notice or permit conditions",
    },
}

DIMENSION_LIMITS = {
    "section_reference": None,
    "height": (
        "4.3 m generally. Exceptions include livestock vehicles, vehicles built "
        "with at least 2 decks for carrying vehicles, and specified "
        "semitrailers at up to 4.6 m, plus double-decker buses at up to 4.4 m"
    ),
    "width": (
        "2.5 m generally. 2.55 m only applies to Safer Freight Vehicles "
        "(certain new rigid or cab chassis trucks and prime movers) and combinations that include them"
    ),
    "length": {
        "other_vehicle": "12.5 m",
        "combination_other_than_b_double_road_train_or_vehicle_carrier": "19.0 m",
        "b_double": (
            "25.0 m generally; up to 26.0 m if the additional prime mover and "
            "articulation-point conditions are met"
        ),
        "road_train": "53.5 m",
        "vehicle_carrier": "25.0 m",
        "articulated_bus": "18.0 m",
        "bus_other_than_articulated": "14.5 m",
    },
    "rear_overhang": {
        "general": (
            "Rear overhang is often the lesser of 3.7 m or 60% of the wheelbase or 'S' dimension, "
            "depending on the vehicle type"
        ),
        "note": "Pig trailers and vehicle carriers have specific alternative rear overhang rules",
    },
    "front_overhang": (
        "Front and side projection limits depend on the vehicle and load "
        "configuration. Check the NHVR size and projection guidance for "
        "measurements."
    ),
    "ground_clearance": (
        "Ground clearance is a prescribed MDL dimension requirement. Check the "
        "current NHVR guidance for the relevant vehicle or trailer type."
    ),
}

BREACH_CATEGORIES = {
    "section_reference": None,
    "categories": ["Minor", "Substantial", "Severe", "Critical (fatigue only)"],
    "mass": {
        "minor": "Exceeds mass limit by ≤5% (or ≤1 tonne for axle groups)",
        "substantial": "Exceeds mass limit by >5% to ≤20%",
        "severe": "Exceeds mass limit by >20%",
    },
    "dimension": {
        "minor": "Exceeds dimension limit by a small margin (Part 4.3 Div 2 HVNL)",
        "substantial": "Exceeds dimension limit by a moderate margin",
        "severe": "Exceeds dimension limit significantly",
        "night_weather_note": "Dimension breaches at night or in hazardous weather are recategorised one level higher.",
    },
    "loading": {
        "description": "Loading breach categories based on Part 4.4 Division 2 of the HVNL.",
        "reference": "Load Restraint Guide for technical requirements.",
    },
    "fatigue": {
        "minor": "Work/rest breach with low risk",
        "substantial": "Work/rest breach with moderate risk",
        "severe": "Work/rest breach with high risk",
        "critical": "Work/rest breach with extreme risk to safety",
        "reference": "Fatigue Reference Card (PDF) for specific breakpoints per work/rest option.",
    },
    "speed": {
        "description": "Speed breaches are categorised under state/territory road rules and HVNL.",
    },
}

SPEED_LIMITS = {
    "section_reference": None,
    "default": {
        "heavy_vehicle_speed_limit": (
            "Drivers must comply with posted limits and road rules. "
            "NHVR speed compliance materials specifically cover heavy vehicles exceeding 100 km/h"
        ),
        "note": (
            "Speed compliance is primarily governed by road rules and vehicle standards. "
            "NHVR materials also emphasise the safety risk of heavy vehicles travelling above 100 km/h"
        ),
    },
    "speed_limiter": {
        "requirement": (
            "If a heavy vehicle is required to have a speed limiter fitted, it must not be tampered with "
            "and should not be capable of travelling above 100 km/h"
        ),
        "reference": "NHVR illegal engine remapping and speed limiter tampering guidance",
    },
}

COR_DUTIES = {
    "section_reference": "sec.26C",
    "overview": (
        "The Chain of Responsibility (CoR) under the HVNL makes parties other than "
        "drivers responsible for heavy vehicle safety. Everyone involved in the supply "
        "chain is accountable."
    ),
    "primary_duty": {
        "description": (
            "Each party in the CoR must ensure, so far as is reasonably practicable, "
            "the safety of their transport activities."
        ),
        "parties": [
            "Employer",
            "Prime contractor",
            "Operator",
            "Scheduler",
            "Consignor",
            "Consignee",
            "Loader",
            "Packer",
            "Loading manager",
        ],
    },
    "executive_duty": (
        "Executives must exercise due diligence to ensure the business complies "
        "with its primary duty."
    ),
    "driver": (
        "Drivers are NOT parties in the CoR but have other obligations under the HVNL "
        "including fatigue, vehicle defects, and road rule compliance."
    ),
    "operator": (
        "Operators must ensure vehicles are safe, roadworthy, and compliant with mass, "
        "dimension, loading, and fatigue requirements."
    ),
    "prohibited_requests": (
        "Any person or business using heavy vehicle services commits an offence if they "
        "make a prohibited request or contract that would cause a driver to speed or "
        "drive fatigued. Maximum penalty over $10,000."
    ),
}

ACCREDITATION_INFO = {
    "section_reference": None,
    "overview": (
        "The NHVAS is a national formal process for recognising operators with "
        "robust safety management systems. From mid-2026, NHVAS will be "
        "progressively replaced by the HVA scheme, with the NHVR working "
        "towards implementation readiness by 1 July 2026."
    ),
    "mass": {
        "summary": "NHVAS Mass Management module.",
        "benefit": (
            "Access to Concessional Mass Limits (CML) and, where other "
            "conditions are met, Higher Mass Limits (HML)."
        ),
        "requirement": "Audited mass management system.",
    },
    "maintenance": {
        "summary": "NHVAS Maintenance Management module.",
        "benefit": "Demonstrates roadworthiness management to regulators.",
        "requirement": "Audited vehicle maintenance management system.",
    },
    "fatigue": {
        "summary": "NHVAS Fatigue Management module (BFM/AFM).",
        "benefit": "Access to flexible work/rest hours under BFM or tailored hours under AFM.",
        "requirement": "Audited fatigue risk management system.",
    },
}

PERMIT_TYPES = {
    "section_reference": None,
    "overview": (
        "Restricted access vehicles may operate under notices or require "
        "permits depending on the vehicle class, network, and route."
    ),
    "class_1": {
        "summary": (
            "Class 1 heavy vehicles commonly include agricultural vehicles, "
            "oversize overmass vehicles, and special purpose vehicles."
        ),
        "note": (
            "Conditions set by the permit; may include route restrictions, "
            "time-of-travel, and escort requirements."
        ),
    },
    "class_2": {
        "summary": (
            "Class 2 heavy vehicles commonly include B-doubles, B-triples, road trains, controlled access buses, "
            "livestock vehicles, vehicle carriers, and PBS vehicles"
        ),
        "note": (
            "Class 2 vehicles typically operate under notices on approved "
            "networks and need permits when travelling outside those networks."
        ),
    },
    "class_3": {
        "summary": (
            "A Class 3 heavy vehicle is one that, together with its load, does "
            "not comply with prescribed mass or dimension requirements and is "
            "not a Class 1 heavy vehicle"
        ),
        "note": (
            "Route-specific permits are common. Examples include certain "
            "overmass rigid truck and dog combinations, wide B-doubles or road "
            "trains, tow trucks, and some dolly combinations."
        ),
    },
    "hml": {
        "summary": (
            "HML permits are used to access roads beyond authorised HML routes "
            "or to operate an HML configuration not covered by a notice."
        ),
        "requirement": "Road manager consent is required before the NHVR can issue the permit.",
    },
    "oversize": {
        "summary": (
            "Oversize/overmass permits usually fall under Class 1 access where "
            "the vehicle or load does not comply with relevant notices or "
            "leaves the approved network."
        ),
        "requirement": (
            "Permit applications are assessed against the relevant vehicle "
            "standards, route, and operating conditions."
        ),
    },
}

HML_INFO = {
    "section_reference": None,
    "eligibility": {
        "summary": (
            "Vehicles or combinations running at HML on triaxle groups must be accredited under NHVAS Mass Management, "
            "be fitted with certified road-friendly suspension, and travel on an authorised route"
        ),
        "approved_routes": "Only on routes approved by road managers for HML operations.",
        "vehicle_requirements": (
            "Certified road-friendly suspension and compliance with the "
            "relevant notice or permit conditions."
        ),
    },
    "limits": {
        "tandem_axle_group": "17.0 t",
        "tri_axle_group": "22.5 t",
        "single_drive_axles_on_buses": "10.0 t",
        "six_tyred_tandem_axle_groups": "14.0 t",
    },
    "application": (
        "Apply for an HML permit if you need access beyond authorised HML "
        "routes or want to use an HML vehicle configuration that is not "
        "covered by a notice"
    ),
}

LAW_AND_REGULATIONS_INFO = {
    "section_reference": None,
    "summary": (
        "The Heavy Vehicle National Law and associated regulations set the legal "
        "framework for heavy vehicle operations in participating jurisdictions."
    ),
    "what_you_can_find": [
        "Heavy Vehicle National Law and regulations",
        "National gazette notices and operator guides",
        "Official NHVR policy and legislative references",
    ],
    "best_starting_point": (
        "Start with the NHVR Heavy Vehicle National Law and regulations page, "
        "then follow the current notices and operator guides relevant to the task."
    ),
}

PBS_INFO = {
    "section_reference": None,
    "summary": (
        "Performance Based Standards (PBS) vehicles are Class 2 heavy vehicles "
        "designed to meet safety and infrastructure performance standards rather "
        "than relying only on prescriptive dimensions."
    ),
    "what_you_can_find": [
        "PBS vehicle overview and network access",
        "PBS levels and standards",
        "Operator guides and access pathways",
    ],
    "best_starting_point": (
        "Start with the NHVR Performance Based Standards page, then check the "
        "relevant network and notice guidance for the specific vehicle."
    ),
}

UNOFFICIAL_WARNING = "This is an unofficial summary. Verify requirements against current NHVR and HVNL sources."

KNOWLEDGE_PROVENANCE = {
    "fatigue_rules": {
        "source_title": "NHVR work and rest requirements",
        "source_url": "https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/work-and-rest-requirements",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "mass_limits": {
        "source_title": "NHVR mass limits",
        "source_url": "https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "dimension_limits": {
        "source_title": "NHVR dimension requirements",
        "source_url": "https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "breach_categories": {
        "source_title": "NHVR breach categorisation",
        "source_url": "https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/breach-categorisation",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "speed_limits": {
        "source_title": "NHVR speeding and speed compliance",
        "source_url": "https://www.nhvr.gov.au/safety-accreditation-compliance/on-road-compliance-and-enforcement/speeding",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "cor_duties": {
        "source_title": "NHVR chain of responsibility guidance",
        "source_url": "https://www.nhvr.gov.au/safety-accreditation-compliance/chain-of-responsibility",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "accreditation_info": {
        "source_title": "NHVR National Heavy Vehicle Accreditation Scheme",
        "source_url": "https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "permit_types": {
        "source_title": "NHVR access permits",
        "source_url": "https://www.nhvr.gov.au/road-access/access-permits",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "hml_info": {
        "source_title": "NHVR higher mass limits guidance",
        "source_url": "https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "law_and_regulations_info": {
        "source_title": "NHVR Heavy Vehicle National Law and regulations",
        "source_url": "https://www.nhvr.gov.au/law-policies/heavy-vehicle-national-law-and-regulations",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
    "pbs_info": {
        "source_title": "NHVR Performance Based Standards",
        "source_url": "https://www.nhvr.gov.au/road-access/performance-based-standards",
        "last_verified": "2026-04-11",
        "unofficial_warning": UNOFFICIAL_WARNING,
    },
}


def attach_provenance(data: dict, knowledge_key: str) -> dict:
    response = deepcopy(data)
    section_reference = response.pop("section_reference", None)

    provenance = deepcopy(KNOWLEDGE_PROVENANCE[knowledge_key])
    if section_reference:
        provenance["section_reference"] = section_reference
        provenance["deep_link_url"] = f"{LEGISLATION_BASE_URL}#{section_reference}"

    response["provenance"] = provenance
    return response
