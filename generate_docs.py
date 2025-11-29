import os

families = {
    "wayne": {
        "beneficiaries": ["Dick Grayson", "Jason Todd", "Tim Drake", "Damian Wayne"],
        "assets": ["Wayne Manor", "Batmobile"],
        "trustee": "Alfred Pennyworth"
    },
    "lannister": {
        "beneficiaries": ["Cersei Lannister", "Jaime Lannister", "Tyrion Lannister"],
        "assets": ["Casterly Rock", "Iron Throne Claims"],
        "trustee": "Tywin Lannister"
    },
    "stark": {
        "beneficiaries": ["Sansa Stark", "Arya Stark", "Bran Stark", "Rickon Stark"],
        "assets": ["Winterfell", "Ice Sword"],
        "trustee": "Eddard Stark"
    },
    "targaryen": {
        "beneficiaries": ["Daenerys Targaryen", "Aegon Targaryen"],
        "assets": ["Dragon Eggs", "Iron Throne"],
        "trustee": "Tyrion Lannister"
    },
    "baratheon": {
        "beneficiaries": ["Joffrey Baratheon", "Myrcella Baratheon", "Tommen Baratheon"],
        "assets": ["Storm's End", "Warhammer"],
        "trustee": "Stannis Baratheon"
    }
}

doc_types = ["will", "trust_deed", "insurance_policy", "investment_agreement"]

for family, data in families.items():
    base_path = f"data/legal_docs/{family}"
    
    # Will
    with open(f"{base_path}/will.txt", "w") as f:
        f.write(f"LAST WILL AND TESTAMENT OF THE {family.upper()} FAMILY\n\n")
        f.write("I. BENEFICIARIES\n")
        for i, ben in enumerate(data["beneficiaries"], 1):
            f.write(f"{i}. {ben}\n")
        f.write(f"\nII. EXECUTOR\nI appoint {data['trustee']} as the executor.\n")
    
    # Trust Deed
    with open(f"{base_path}/trust_deed.txt", "w") as f:
        f.write(f"THE {family.upper()} FAMILY TRUST\n\n")
        f.write(f"Trustee: {data['trustee']}\n")
        f.write("Assets Held:\n")
        for asset in data["assets"]:
            f.write(f"- {asset}\n")
        f.write("\nPurpose: To maintain the legacy and power of the House.\n")

    # Insurance
    with open(f"{base_path}/insurance_policy.txt", "w") as f:
        f.write(f"INSURANCE POLICY FOR HOUSE {family.upper()}\n\n")
        f.write("Coverage: Comprehensive Castle and Dragon Damage.\n")
        f.write("Premium: 500 Gold Dragons per annum.\n")
        f.write("Exclusions: Acts of War, White Walker Invasions.\n")

    # Investment Agreement
    with open(f"{base_path}/investment_agreement.txt", "w") as f:
        f.write(f"INVESTMENT MANDATE - HOUSE {family.upper()}\n\n")
        f.write("Risk Tolerance: Aggressive.\n")
        f.write("Target Return: 15% per annum.\n")
        f.write("Restrictions: No investment in rival houses.\n")

print("Legal docs generated successfully.")
