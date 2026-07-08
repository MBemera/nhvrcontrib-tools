# Source Verification

Manual verification pass completed on `2026-04-11` against current official NHVR material.

## HVNL 2026 Review (`2026-07-05`)

A follow-up review assessed the amended HVNL against the built-in knowledge base:

- Ministers approved the final amended HVNL package in May 2026. The amended law and
  supporting instruments commence on **1 August 2026** (previous guidance said "working
  towards 1 July 2026").
- The knowledge base intentionally continues to describe the **pre-amendment law**, which
  remains in force until 31 July 2026. Affected entries now carry a `reform_note` field, and
  `ACCREDITATION_INFO` gained an `hva` entry describing the new scheme.

### Overhaul checklist for 1 August 2026

Run the full manual audit and apply these changes when the amended law commences:

- **Accreditation**: make HVA (GSA/ACA) the primary content; describe NHVAS as legacy in
  transition (existing accreditations valid until expiry, up to 3 years).
- **Fatigue**: BFM/AFM close to new applications; document ACA – Fatigue with Alternative
  Compliance Hours (ACH) and templated tables of hours; note the updated written work diary.
  Re-verify all work/rest tables against the post-commencement NHVR pages.
- **Mass limits**: raise GML entries to the levels formerly published as CML; remove the CML
  entry (category removed from the MDL Regulation); re-verify HML interactions.
- **Dimensions**: update the 19.0 m combination length entries to 20.0 m where they apply to
  prime mover and semitrailer, and rigid truck and trailer combinations. Do **not** change the
  4.3 m height limit — the 4.6 m increase is deferred to a future amendment; re-check its
  status.
- **Breach categories / CoR / permits / speed**: re-verify against the post-commencement
  pages; no confirmed structural changes were identified in this review.
- Refresh every `last_verified` date, the deep-link anchors into the Queensland legislation
  view (section numbering may change), and remove the pre-commencement `reform_note` fields.

Sources for this review: NHVR HVNL reform implementation page, NHVR "Mass, Dimension and
Loading changes" fact sheet (commencement 1 August 2026), NHVR HVA transition FAQs, NTC HVNL
reform pages, and industry coverage corroborating commencement and scheme details. Direct
fetches of nhvr.gov.au were blocked from the audit environment, so figures were only recorded
where at least two independent sources agreed; anything less stayed out of the knowledge base.

## Scope

The built-in knowledge base was reviewed against current NHVR guidance for:

- fatigue management and work/rest hours
- mass limits, CML, and HML
- dimension requirements
- speed compliance and speed limiter guidance
- Chain of Responsibility overview
- NHVAS / HVA transition guidance
- vehicle classes and permit guidance

## Key Corrections Made

- Corrected Standard Hours two-up entries:
  - `24 hours` now uses the current `5 continuous hours` major rest rule.
  - `7 days` now uses `60 hours work`.
  - `14 days` now uses `120 hours work`.
- Corrected BFM entries:
  - Solo `9 hours` and `12 hours` thresholds now match NHVR guidance.
  - Two-up rules now use the current `24/82 hours`, `70 hours in 7 days`, and `140 hours in 14 days` structure.
- Corrected HML axle group figures:
  - `tandem axle group` now `17.0 t`
  - `tri-axle group` now `22.5 t`
  - added `single drive axles on buses` and `six-tyred tandem axle groups`
- Corrected dimension summaries:
  - `2.55 m` width now refers to `Safer Freight Vehicles`, not refrigerated vehicles generally
  - height exceptions updated to current NHVR wording
  - B-double length guidance clarified as `25 m generally`, `26 m` when additional conditions are met
- Reworked speed guidance to avoid unsupported blanket claims and anchor it to NHVR speed compliance / speed limiter material.
- Updated accreditation text to reflect the current NHVR transition wording for the HVA scheme.
- Updated permit summaries to align with current NHVR vehicle class and permit guidance.

## Official NHVR Sources Checked

- Work and rest requirements:
  - https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/work-and-rest-requirements
- Advanced Fatigue Management:
  - https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/advanced-fatigue-management
- Counting time:
  - https://www.nhvr.gov.au/safety-accreditation-compliance/fatigue-management/counting-time
- Mass limits:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits
- General Mass Limits:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits/general-mass-limits
- Concessional Mass Limits:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits/concessional-mass-limits
- Higher Mass Limits:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/mass-limits/higher-mass-limits
- Dimension requirements:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements
- Height:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements/height
- Width:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/dimension-requirements/width
- Size and projection of loads:
  - https://www.nhvr.gov.au/road-access/mass-dimension-and-loading/general-mass-and-dimension-limits/rear-overhang
- General access vehicle guidance:
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/general-access-vehicle
- B-double notice/operator guide:
  - https://www.nhvr.gov.au/C2026G00194-national-class-2-b-double-authorisation-notice-2024-no1-operators-guide
- Class definitions:
  - https://www.nhvr.gov.au/road-access/mass-dimension-and-loading/classes-of-heavy-vehicles
  - https://www.nhvr.gov.au/road-access/mass-dimension-and-loading/classes-of-heavy-vehicles/class-2
  - https://www.nhvr.gov.au/road-access/mass-and-dimension/classes-of-heavy-vehicles/class-3
- Permit guidance:
  - https://www.nhvr.gov.au/road-access/access-management/do-i-need-a-permit
- NHVAS and HVA transition:
  - https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme
  - https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme/nhvas-transition-to-hva-scheme
  - https://www.nhvr.gov.au/safety-accreditation-compliance/national-heavy-vehicle-accreditation-scheme/nhvas-transition-to-hva-scheme/transition-options
- Speed limiter / engine remapping guidance:
  - https://www.nhvr.gov.au/engineremapping

## Maintenance

Repeat this manual audit before a release that changes built-in legal summaries, provenance dates, or source mappings.
