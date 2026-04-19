"""Basic SDK usage — all sync, no API key needed."""

from nhvrcontrib import NHVR

client = NHVR()

# --- Fatigue rules ---
print("=== Standard Fatigue Rules ===")
rules = client.fatigue_rules(scheme="standard")
print(f"Summary: {rules['summary']}")
for period, rule in rules["solo_driver"].items():
    print(f"  {period}: {rule}")

# --- Mass limits ---
print("\n=== Mass Limits (with HML) ===")
limits = client.mass_limits(include_hml=True)
print(f"Steer axle: {limits['general']['steer_axle']}")
print(f"HML tri-axle group: {limits['hml']['tri_axle_group']}")

# --- Dimension limits ---
print("\n=== Dimension Limits ===")
dims = client.dimension_limits()
print(f"Height: {dims['height']}")
print(f"Width: {dims['width']}")
for vehicle_type, length in dims["length"].items():
    print(f"  {vehicle_type}: {length}")

# --- Breach categories ---
print("\n=== Mass Breach Categories ===")
breaches = client.breach_categories(breach_type="mass")
for severity, desc in breaches["mass"].items():
    print(f"  {severity}: {desc}")

# --- Chain of Responsibility ---
print("\n=== Chain of Responsibility ===")
cor = client.cor_duties()
print(f"Overview: {cor['overview'][:100]}...")
print(f"Parties: {', '.join(cor['primary_duty']['parties'])}")

# --- Quick lookups ---
print("\n=== Other Lookups ===")
print(f"Speed limiter: {client.speed_limits()['speed_limiter']['requirement']}")
print(f"NHVAS mass benefit: {client.accreditation(module='mass')['mass']['benefit']}")
print(f"Class 1 permit: {client.permit_types(permit_type='class_1')['class_1']['summary']}")
print(f"HML tri-axle: {client.hml_info()['limits']['tri_axle_group']}")
