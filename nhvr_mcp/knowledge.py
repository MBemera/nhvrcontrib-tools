"""Built-in NHVR knowledge base.

Authoritative data sourced from the NHVR website and HVNL legislation.
Used as quick-lookup fallback when live scraping is not required.
"""

from __future__ import annotations

from copy import deepcopy

FATIGUE_RULES = {
    "standard": {
        "summary": "Standard hours – default work/rest option for all drivers without BFM/AFM accreditation.",
        "solo_driver": {
            "in_any_5.5_hours": "Max 5 hours 15 min work, then ≥15 min continuous rest",
            "in_any_8_hours": "Max 7 hours 30 min work, then ≥30 min rest in blocks ≥15 min",
            "in_any_11_hours": "Max 10 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 12 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": "Max 72 hours work, then ≥24 continuous hours stationary rest",
            "in_any_14_days": "Max 144 hours work; must have ≥2 night rest breaks and ≥2 night rests in any 14 days",
        },
        "two_up_driver": {
            "in_any_5.5_hours": "Max 5 hours 15 min work, then ≥15 min continuous rest",
            "in_any_8.5_hours": "Max 8 hours work, then ≥30 min rest in blocks ≥15 min",
            "in_any_11_hours": "Max 10 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 12 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": "Max 72 hours work, then ≥24 continuous hours stationary rest",
            "in_any_14_days": "Max 144 hours work; must have night rest requirements met",
        },
        "night_rest": "7 continuous hours stationary rest between 10pm and 8am (base time zone).",
    },
    "bfm": {
        "summary": "Basic Fatigue Management – NHVAS module allowing more flexible work/rest hours.",
        "solo_driver": {
            "in_any_6.25_hours": "Max 6 hours work, then ≥15 min continuous rest",
            "in_any_9.25_hours": "Max 8 hours 45 min work, then ≥30 min rest in blocks ≥15 min",
            "in_any_12.25_hours": "Max 11 hours 15 min work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 14 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": "Max 36 hours long/night work; max 84 hours total work",
            "in_any_14_days": "Max 144 hours work; night rest requirements apply",
        },
        "two_up_driver": {
            "in_any_5.5_hours": "Max 5 hours 15 min work, then ≥15 min continuous rest",
            "in_any_8.5_hours": "Max 8 hours work, then ≥30 min rest in blocks ≥15 min",
            "in_any_12_hours": "Max 11 hours work, then ≥60 min rest in blocks ≥15 min",
            "in_any_24_hours": "Max 14 hours work, then ≥7 continuous hours stationary rest",
            "in_any_7_days": "Max 84 hours work",
            "in_any_14_days": "Max 144 hours work; night rest requirements apply",
        },
        "requirement": "Operator must hold NHVAS BFM accreditation.",
    },
    "afm": {
        "summary": "Advanced Fatigue Management – tailored work/rest hours via risk management.",
        "description": (
            "AFM provides tailored work and rest hours through an accredited fatigue risk "
            "management system. Specific hours are set per operator's AFM accreditation. "
            "Outer limits: max 16 hours work in 24 hours, max 168 hours in 14 days."
        ),
        "requirement": "Operator must hold NHVAS AFM accreditation with approved operating schedules.",
    },
}

MASS_LIMITS = {
    "general": {
        "summary": "General Mass Limits (GML) – basic limits for all heavy vehicles.",
        "steer_axle": "6.0 t (single tyre), 6.5 t (dual tyre)",
        "single_axle_dual_tyres": "9.0 t",
        "tandem_axle_group": "16.5 t",
        "tri_axle_group": "20.0 t",
        "quad_axle_group": "Not available at GML",
        "gross_combination_mass": "Up to 42.5 t for B-double (GML)",
    },
    "cml": {
        "summary": "Concessional Mass Limits (CML) – above GML with NHVAS accreditation.",
        "requirement": "NHVAS Mass Management accreditation and road-friendly suspension.",
        "tandem_axle_group": "17.0 t",
        "tri_axle_group": "21.0 t",
    },
    "hml": {
        "summary": "Higher Mass Limits (HML) – highest limits for eligible vehicles.",
        "requirement": "NHVAS Mass Management accreditation, approved routes, road-friendly suspension.",
        "tandem_axle_group": "18.0 t (drive), 17.0 t (other)",
        "tri_axle_group": "22.5 t (with road-friendly suspension)",
        "b_double_gross": "Up to 62.5 t (on approved routes)",
    },
}

DIMENSION_LIMITS = {
    "height": "4.3 m maximum (4.6 m for double-deck livestock carriers on approved routes).",
    "width": "2.5 m maximum (refrigerated vehicles may have 2.55 m exemption).",
    "length": {
        "rigid_vehicle": "12.5 m",
        "articulated_vehicle": "19.0 m",
        "b_double": "26.0 m",
        "road_train": "36.5 m (Type 1), 53.5 m (Type 2)",
    },
    "rear_overhang": {
        "general": "Rear overhang must not exceed 60% of the wheelbase or 3.7 m (whichever is less).",
        "note": "Specific limits apply for different vehicle configurations.",
    },
    "front_overhang": "Measured from the centre of the front axle. Limits vary by vehicle type.",
    "ground_clearance": "Minimum ground clearance requirements apply to trailers.",
}

BREACH_CATEGORIES = {
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
    "default": {
        "heavy_vehicle_speed_limit": "100 km/h (general maximum for heavy vehicles unless otherwise signed).",
        "school_zones": "40 km/h (during school zone hours).",
        "note": (
            "Speed limits are primarily governed by state/territory road rules. "
            "The HVNL applies to heavy vehicle speed compliance and enforcement."
        ),
    },
    "speed_limiter": {
        "requirement": "Heavy vehicles with a GVM >12 tonnes must have a speed limiter set to 100 km/h.",
        "reference": "HVNL Part 4.5",
    },
}

COR_DUTIES = {
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
    "overview": (
        "The National Heavy Vehicle Accreditation Scheme (NHVAS) recognises operators "
        "with effective safety management systems. Transitioning to HVA scheme from mid-2026."
    ),
    "mass": {
        "summary": "NHVAS Mass Management module.",
        "benefit": "Access to Concessional Mass Limits (CML) and Higher Mass Limits (HML).",
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
    "overview": "Access permits allow vehicles that exceed standard limits to travel on approved routes.",
    "class_1": {
        "summary": "Class 1 heavy vehicle – special-purpose vehicle (e.g. crane, agricultural).",
        "note": (
            "Conditions set by the permit; may include route restrictions, "
            "time-of-travel, and escort requirements."
        ),
    },
    "class_2": {
        "summary": "Class 2 heavy vehicle – a general access vehicle operating under a notice.",
        "note": "Class 2 notices provide blanket access on approved networks.",
    },
    "class_3": {
        "summary": "Class 3 heavy vehicle – restricted access vehicle requiring a specific permit.",
        "note": "Route-specific permits with conditions tailored to the vehicle and journey.",
    },
    "hml": {
        "summary": "HML permit – allows operation at Higher Mass Limits on approved routes.",
        "requirement": "NHVAS Mass Management accreditation, road-friendly suspension.",
    },
    "oversize": {
        "summary": "Oversize/overmass permits for loads exceeding standard dimension or mass limits.",
        "requirement": "Permit application via NHVR Portal specifying vehicle, load, and route details.",
    },
}

HML_INFO = {
    "eligibility": {
        "summary": "Vehicles must be NHVAS Mass Management accredited with road-friendly suspension.",
        "approved_routes": "Only on routes approved by road managers for HML operations.",
        "vehicle_requirements": "Compliant suspension, tyres, and axle configuration.",
    },
    "limits": {
        "tandem_axle_drive": "18.0 t",
        "tandem_axle_other": "17.0 t",
        "tri_axle_group": "22.5 t",
        "b_double_gross": "Up to 62.5 t",
    },
    "application": "Apply via the NHVR Portal (NHVR Go).",
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
}


def attach_provenance(data: dict, knowledge_key: str) -> dict:
    response = deepcopy(data)
    response["provenance"] = deepcopy(KNOWLEDGE_PROVENANCE[knowledge_key])
    return response
