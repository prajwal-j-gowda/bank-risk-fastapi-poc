from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Commercial Onboarding POC (Registry & Risk)", version="1.0.0")

# ==========================================
# 1. REGISTRY API MODELS & LOGIC
# ==========================================
class RegistryRequest(BaseModel):
    registrationNumber: str
    jurisdiction: str
    legalName: str

class Address(BaseModel):
    line1: str
    city: str
    postalCode: str
    country: str

class RegistryData(BaseModel):
    legalName: str
    registrationNumber: str
    jurisdiction: str
    entityType: str
    incorporationDate: date
    companyStatus: str
    industryDescription: str 
    registeredAddress: Address

class RegistryResponse(BaseModel):
    matchStatus: str
    registryData: Optional[RegistryData] = None

# Hardcoded mock database of 5 companies
MOCK_REGISTRY = {
    "01234567": {
        "registrationNumber": "01234567", # <-- Added missing field
        "legalName": "ACME GLOBAL SOLUTIONS LTD",
        "jurisdiction": "GB",
        "entityType": "PRIVATE_LIMITED_COMPANY",
        "incorporationDate": "2018-05-12",
        "companyStatus": "ACTIVE",
        "industryDescription": "Information technology consulting activities",
        "registeredAddress": {"line1": "123 Innovation Drive", "city": "London", "postalCode": "E1 6AN", "country": "GB"}
    },
    "11223344": {
        "registrationNumber": "11223344", # <-- Added missing field
        "legalName": "STARK INDUSTRIES LLC",
        "jurisdiction": "US-DE",
        "entityType": "LLC",
        "incorporationDate": "1999-10-01",
        "companyStatus": "ACTIVE",
        "industryDescription": "Defense and aerospace manufacturing",
        "registeredAddress": {"line1": "10880 Malibu Point", "city": "Malibu", "postalCode": "90265", "country": "US"}
    },
    "99887766": {
        "registrationNumber": "99887766", # <-- Added missing field
        "legalName": "WAYNE ENTERPRISES INC",
        "jurisdiction": "US-NY",
        "entityType": "CORPORATION",
        "incorporationDate": "1939-05-27",
        "companyStatus": "ACTIVE",
        "industryDescription": "Conglomerate and advanced technology",
        "registeredAddress": {"line1": "1007 Mountain Drive", "city": "Gotham", "postalCode": "10001", "country": "US"}
    },
    "44556677": {
        "registrationNumber": "44556677", # <-- Added missing field
        "legalName": "INITECH CORP",
        "jurisdiction": "US-TX",
        "entityType": "CORPORATION",
        "incorporationDate": "1994-02-19",
        "companyStatus": "DISSOLVED",
        "industryDescription": "Software and technology services",
        "registeredAddress": {"line1": "4120 Freidrich Lane", "city": "Austin", "postalCode": "78744", "country": "US"}
    },
    "55667788": {
        "registrationNumber": "55667788", # <-- Added missing field
        "legalName": "GLOBEX CORPORATION",
        "jurisdiction": "CY",
        "entityType": "PRIVATE_LIMITED_COMPANY",
        "incorporationDate": "1996-11-03",
        "companyStatus": "SUSPENDED",
        "industryDescription": "High-tech manufacturing and research",
        "registeredAddress": {"line1": "1 Cypress Road", "city": "Nicosia", "postalCode": "1065", "country": "CY"}
    }
}

@app.post("/api/v1/registry/check", response_model=RegistryResponse)
def check_registry(request: RegistryRequest):
    company = MOCK_REGISTRY.get(request.registrationNumber)
    
    # Check if registration number exists and name matches (case-insensitive)
    if company and company["legalName"].lower() == request.legalName.lower():
        return RegistryResponse(matchStatus="EXACT_MATCH", registryData=company)
    
    # If no match found
    return RegistryResponse(matchStatus="NO_MATCH")


# ==========================================
# 2. FRAUD & RISK SCORING API
# ==========================================
class FraudRiskRequest(BaseModel):
    legalName: str
    jurisdiction: str
    registrationNumber: str 
    industryDescription: str
    expectedProducts: List[str]

class RiskMetadata(BaseModel):
    jurisdictionRisk: str
    entityRisk: str      
    productRisk: str

class FraudRiskResponse(BaseModel):
    riskAssessmentId: str
    fraudScore: int
    riskTier: str
    flags: List[str]
    recommendation: str
    metadata: RiskMetadata

@app.post("/api/v1/risk/score", response_model=FraudRiskResponse)
def calculate_risk(request: FraudRiskRequest):
    fraud_score = 10
    flags = []
    
    # Check registration number risk (e.g., flagging specific known bad entities)
    if request.registrationNumber in ["44556677", "55667788"]:
        entity_risk = "HIGH"
        fraud_score += 40
        flags.append("HIGH_RISK_ENTITY")
    else:
        entity_risk = "LOW"

    # Check jurisdiction risk
    if request.jurisdiction in ["CY", "KY", "PA"]:
        jurisdiction_risk = "HIGH"
        fraud_score += 30
        flags.append("HIGH_RISK_JURISDICTION")
    else:
        jurisdiction_risk = "LOW"

    # Check product risk
    product_risk = "HIGH" if "FX_TRADING" in request.expectedProducts else "LOW"
    if product_risk == "HIGH":
        fraud_score += 15

    # Determine final tier and recommendation
    if fraud_score > 60:
        risk_tier, recommendation = "HIGH_RISK", "REQUIRE_HITL"
    elif fraud_score > 30:
        risk_tier, recommendation = "MEDIUM_RISK", "REQUIRE_HITL"
    else:
        risk_tier, recommendation = "LOW_RISK", "PROCEED_STP"

    return FraudRiskResponse(
        riskAssessmentId=f"RSK-{request.registrationNumber}",
        fraudScore=fraud_score,
        riskTier=risk_tier,
        flags=flags,
        recommendation=recommendation,
        metadata=RiskMetadata(
            jurisdictionRisk=jurisdiction_risk, 
            entityRisk=entity_risk, 
            productRisk=product_risk
        )
    )
    
