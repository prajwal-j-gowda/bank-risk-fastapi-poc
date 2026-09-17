from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ultra Simple POC APIs - V2")

# ==========================================
# 1. Registry API - Simple List Check
# ==========================================
REGISTERED_COMPANIES = [
    "acme corp",
    "stark industries",
    "wayne enterprises",
    "wonka industries",
    "oscorp",
    "globex",
]


@app.get("/companies/search", tags=["Registry"])
def search_company(name: str):
    """Checks if a company name exists in our predefined list."""
    if name.strip().lower() in REGISTERED_COMPANIES:
        return {
            "status": "exists",
            "message": f"'{name}' is a registered company.",
        }

    return {
        "status": "not exist",
        "message": f"'{name}' was not found in the registry.",
    }


# ==========================================
# 2. Fraud & Risk API - Onboarding Risk Check
# ==========================================
FRAUD_BLACKLIST = [
    "john doe",
    "jane hacker",
    "scammer123",
]

# Two-character country code -> accepted country names
HIGH_RISK_COUNTRIES = {
    "AF": ["afghanistan"],
    "MM": ["burma", "myanmar", "burma (myanmar)"],
    "BI": ["burundi"],
    "TD": ["chad"],
    "CG": ["republic of the congo"],
    "CU": ["cuba"],
    "GQ": ["equatorial guinea"],
    "ER": ["eritrea"],
    "HT": ["haiti"],
    "IR": ["iran"],
    "LA": ["laos"],
    "LY": ["libya"],
    "SL": ["sierra leone"],
    "SO": ["somalia"],
    "SD": ["sudan"],
    "TG": ["togo"],
    "TM": ["turkmenistan"],
    "VE": ["venezuela"],
    "YE": ["yemen"],
}

DISPOSABLE_EMAILS = [
    "tempmail.com",
    "10minutemail.com",
    "throwaway.com",
]


class AccountRequest(BaseModel):
    user_name: str
    email_address: str
    country_code: str
    is_using_vpn: bool


def is_high_risk_country(country: str) -> bool:
    """
    Checks whether the provided country is a high-risk country.
    Accepts either a two-character country code or a full country name.
    Matching is case-insensitive and ignores surrounding whitespace.
    """
    normalized_country = country.strip().lower()

    for country_code, country_names in HIGH_RISK_COUNTRIES.items():
        if normalized_country.upper() == country_code:
            return True

        if normalized_country in country_names:
            return True

    return False


@app.post("/evaluate/risk", tags=["Risk Engine"])
def evaluate_risk(request: AccountRequest):
    """Evaluates customer onboarding risk based on multiple factors."""

    # Rule 1: Name Blacklist
    if request.user_name.strip().lower() in FRAUD_BLACKLIST:
        return {
            "decision": "REJECT",
            "reason": "User is on the fraud blacklist.",
        }

    # Rule 2: Disposable Email check
    email_domain = request.email_address.split("@")[-1].strip().lower()

    if email_domain in DISPOSABLE_EMAILS:
        return {
            "decision": "REJECT",
            "reason": "Disposable email addresses are not allowed.",
        }

    # Rule 3: Country Risk check
    if is_high_risk_country(request.country_code):
        return {
            "decision": "MANUAL_REVIEW",
            "reason": "Account originating from a high-risk country.",
        }

    # Rule 4: VPN check
    if request.is_using_vpn:
        return {
            "decision": "MANUAL_REVIEW",
            "reason": "VPN usage detected.",
        }

    # Default: Approve everyone else
    return {
        "decision": "APPROVE",
        "reason": "No risk factors found.",
    }
