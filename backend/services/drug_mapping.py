"""
Indian Drug Brand → INN (International Nonproprietary Name) mapper.
Maps common Indian drug brand names to generic names with SNOMED codes.
"""

# Complete brand → (INN, SNOMED code) mapping
BRAND_TO_INN = {
    "crocin": ("Paracetamol", "387517004"),
    "dolo": ("Paracetamol", "387517004"),
    "combiflam": ("Ibuprofen+Paracetamol", "387207008"),
    "metformin": ("Metformin", "372567009"),
    "glycomet": ("Metformin", "372567009"),
    "amlodipine": ("Amlodipine", "386864001"),
    "amlong": ("Amlodipine", "386864001"),
    "atenolol": ("Atenolol", "387506000"),
    "telmisartan": ("Telmisartan", "387069000"),
    "telma": ("Telmisartan", "387069000"),
    "ecosprin": ("Aspirin", "387458008"),
    "azithromycin": ("Azithromycin", "396001008"),
    "augmentin": ("Amoxicillin+Clavulanate", "96068000"),
    "amoxicillin": ("Amoxicillin", "372687004"),
    "pantoprazole": ("Pantoprazole", "395821003"),
    "pan-d": ("Pantoprazole+Domperidone", "395821003"),
    "atorvastatin": ("Atorvastatin", "373444002"),
    "atorva": ("Atorvastatin", "373444002"),
    "insulin glargine": ("Insulin Glargine", "411529005"),
    "lantus": ("Insulin Glargine", "411529005"),
    "glimepiride": ("Glimepiride", "386966003"),
    "amaryl": ("Glimepiride", "386966003"),
    "losartan": ("Losartan", "373567002"),
    "losar": ("Losartan", "373567002"),
    "cetirizine": ("Cetirizine", "372523007"),
    "allegra": ("Fexofenadine", "372522002"),
}


def resolve_drug(brand_name: str) -> dict:
    """Resolve a drug brand name to INN + SNOMED code."""
    key = brand_name.lower().strip()
    if key in BRAND_TO_INN:
        inn, snomed = BRAND_TO_INN[key]
        return {"brand": brand_name, "inn": inn, "snomed_code": snomed, "matched": True}
    # Try partial match
    for k, (inn, snomed) in BRAND_TO_INN.items():
        if k in key or key in k:
            return {"brand": brand_name, "inn": inn, "snomed_code": snomed, "matched": True}
    return {"brand": brand_name, "inn": None, "snomed_code": None, "matched": False}
