#!/usr/bin/env python3
"""
Script pour vérifier et enrichir les emails des cliniques médico-esthétiques
des Laurentides via l'API Hunter.io.

Usage: python3 hunter_verify.py
"""

import csv
import json
import time
import urllib.request
import urllib.error
import sys

API_KEY = "6b65a1f40876dbf2d47f28b4dc2b6f99d372ec93"
BASE_URL = "https://api.hunter.io/v2"

INPUT_CSV = "cliniques_medico_esthetiques_laurentides.csv"
OUTPUT_CSV = "cliniques_medico_esthetiques_laurentides_verified.csv"

# Domaines à scanner (domain-search)
DOMAINS = [
    "dermastructure.com",
    "institutbrabant.com",
    "cliniqueleblancsavaria.ca",
    "medisens.ca",
    "hgsantebeaute.ca",
    "cliniquemedicoderma.com",
    "cliniqueaar.com",
    "cliniquemc.com",
    "medinordesthetique.com",
    "cliniquemedinord.com",
    "vkderma.ca",
    "epilationlasermedicspa.com",
    "dermapure.com",
    "epiderma.ca",
]

# Emails existants à vérifier
EMAILS_TO_VERIFY = [
    "dermastructure@gmail.com",
    "info@institutbrabant.com",
    "hgsantebeaute@gmail.com",
    "drtbmacesthetique@gmail.com",
    "cliniqueaar@gmail.com",
    "info@cliniquemedinord.com",
    "info@dermapure.ca",
]

# Propriétaires à chercher (email-finder)
OWNERS_TO_FIND = [
    {"domain": "institutbrabant.com", "first_name": "Nathalie", "last_name": "Brabant"},
    {"domain": "cliniqueleblancsavaria.ca", "first_name": "Marie-Andrée", "last_name": "LeBlanc"},
    {"domain": "cliniquemedicoderma.com", "first_name": "Lydia", "last_name": "Monette"},
    {"domain": "medinordesthetique.com", "first_name": "Poulin", "last_name": ""},
    {"domain": "dermapure.com", "first_name": "Louise", "last_name": "St-Aubin"},
    {"domain": "dermapure.com", "first_name": "Marilyne", "last_name": "Gagné"},
    {"domain": "vkderma.ca", "first_name": "Vicky", "last_name": ""},
    {"domain": "vkderma.ca", "first_name": "Kim", "last_name": ""},
]


def api_call(endpoint, params):
    """Make a Hunter.io API call with rate limiting."""
    params["api_key"] = API_KEY
    query = "&".join(f"{k}={urllib.request.quote(str(v))}" for k, v in params.items() if v)
    url = f"{BASE_URL}/{endpoint}?{query}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"  HTTP {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None
    finally:
        time.sleep(1.5)  # Rate limit


def domain_search(domain):
    """Search for all emails on a domain."""
    print(f"\n{'='*60}")
    print(f"DOMAIN SEARCH: {domain}")
    print(f"{'='*60}")

    result = api_call("domain-search", {"domain": domain})
    if not result or "data" not in result:
        print("  No results.")
        return []

    data = result["data"]
    emails = data.get("emails", [])
    print(f"  Found {len(emails)} email(s):")

    found = []
    for e in emails:
        email = e.get("value", "")
        first = e.get("first_name", "")
        last = e.get("last_name", "")
        position = e.get("position", "")
        confidence = e.get("confidence", 0)
        print(f"  - {email} | {first} {last} | {position} | confidence: {confidence}")
        found.append({
            "email": email,
            "first_name": first,
            "last_name": last,
            "position": position,
            "confidence": confidence,
            "domain": domain,
        })

    return found


def email_finder(domain, first_name, last_name):
    """Find email for a specific person at a domain."""
    print(f"\nEMAIL FINDER: {first_name} {last_name} @ {domain}")

    params = {"domain": domain, "first_name": first_name}
    if last_name:
        params["last_name"] = last_name

    result = api_call("email-finder", params)
    if not result or "data" not in result:
        print("  No result.")
        return None

    data = result["data"]
    email = data.get("email", "")
    confidence = data.get("score", 0)

    if email:
        print(f"  Found: {email} (confidence: {confidence})")
        return {"email": email, "confidence": confidence}
    else:
        print("  Not found.")
        return None


def email_verifier(email):
    """Verify an email address."""
    print(f"\nVERIFY: {email}")

    result = api_call("email-verifier", {"email": email})
    if not result or "data" not in result:
        print("  Verification failed.")
        return None

    data = result["data"]
    status = data.get("status", "unknown")
    score = data.get("score", 0)
    print(f"  Status: {status} | Score: {score}")
    return {"email": email, "status": status, "score": score}


def update_csv(domain_results, finder_results, verify_results):
    """Read existing CSV and add Hunter.io columns."""
    rows = []
    with open(INPUT_CSV, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)
        for row in reader:
            rows.append(row)

    # Add new columns
    new_fields = ["Hunter Email(s)", "Hunter Confidence", "Email Vérifié (status)", "Email Vérifié (score)"]
    for f in new_fields:
        if f not in fieldnames:
            fieldnames.append(f)

    # Build lookup from domain results
    domain_email_map = {}
    for dr in domain_results:
        d = dr["domain"]
        if d not in domain_email_map:
            domain_email_map[d] = []
        domain_email_map[d].append(dr)

    # Build lookup from finder results
    finder_map = {}
    for fr in finder_results:
        if fr:
            finder_map[fr["email"]] = fr

    # Build lookup from verify results
    verify_map = {}
    for vr in verify_results:
        if vr:
            verify_map[vr["email"]] = vr

    for row in rows:
        site = row.get("Site web", "")
        existing_email = row.get("Email", "")

        # Extract domain from site URL
        domain = ""
        if site:
            domain = site.replace("https://", "").replace("http://", "").replace("www.", "").split("/")[0]

        # Hunter emails from domain search
        hunter_emails = []
        hunter_confidences = []
        if domain in domain_email_map:
            for entry in domain_email_map[domain]:
                hunter_emails.append(entry["email"])
                hunter_confidences.append(str(entry["confidence"]))

        row["Hunter Email(s)"] = "; ".join(hunter_emails) if hunter_emails else ""
        row["Hunter Confidence"] = "; ".join(hunter_confidences) if hunter_confidences else ""

        # Verification status
        email_to_check = existing_email or (hunter_emails[0] if hunter_emails else "")
        if email_to_check and email_to_check in verify_map:
            row["Email Vérifié (status)"] = verify_map[email_to_check]["status"]
            row["Email Vérifié (score)"] = str(verify_map[email_to_check]["score"])
        else:
            row["Email Vérifié (status)"] = ""
            row["Email Vérifié (score)"] = ""

    # Write output
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\nUpdated CSV written to: {OUTPUT_CSV}")


def main():
    print("=" * 60)
    print("HUNTER.IO - Cliniques Médico-Esthétiques Laurentides")
    print("=" * 60)

    # Check account status
    print("\nChecking account...")
    account = api_call("account", {})
    if account and "data" in account:
        d = account["data"]
        print(f"  Plan: {d.get('plan_name', '?')}")
        print(f"  Searches: {d.get('requests', {}).get('searches', {})}")
        print(f"  Verifications: {d.get('requests', {}).get('verifications', {})}")
    else:
        print("  Could not check account. Proceeding anyway...")

    # 1. Domain searches
    print("\n\n### PHASE 1: DOMAIN SEARCHES ###")
    all_domain_results = []
    for domain in DOMAINS:
        results = domain_search(domain)
        all_domain_results.extend(results)

    # 2. Email finder for owners
    print("\n\n### PHASE 2: EMAIL FINDER (owners) ###")
    all_finder_results = []
    for owner in OWNERS_TO_FIND:
        result = email_finder(owner["domain"], owner["first_name"], owner["last_name"])
        all_finder_results.append(result)

    # 3. Verify existing emails
    print("\n\n### PHASE 3: EMAIL VERIFICATION ###")
    all_verify_results = []

    # Verify known emails
    for email in EMAILS_TO_VERIFY:
        result = email_verifier(email)
        all_verify_results.append(result)

    # Also verify any new emails found
    new_emails = set()
    for dr in all_domain_results:
        new_emails.add(dr["email"])
    for fr in all_finder_results:
        if fr:
            new_emails.add(fr["email"])

    for email in new_emails:
        if email not in EMAILS_TO_VERIFY:
            result = email_verifier(email)
            all_verify_results.append(result)

    # 4. Update CSV
    print("\n\n### PHASE 4: UPDATE CSV ###")
    update_csv(all_domain_results, all_finder_results, all_verify_results)

    # 5. Print summary
    print("\n\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Domain searches performed: {len(DOMAINS)}")
    print(f"Emails found via domain search: {len(all_domain_results)}")
    print(f"Email finder attempts: {len(OWNERS_TO_FIND)}")
    print(f"Emails verified: {len(all_verify_results)}")
    print(f"\nOutput: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
