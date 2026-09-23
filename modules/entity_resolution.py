import pandas as pd


def build_entity_relationships(persons, cdr, bank, fir, social):
    relationships = []

    # -----------------------------
    # PERSON -> PHONE
    # -----------------------------
    for _, row in persons.iterrows():
        relationships.append({
            "source": row["person_id"],
            "relationship": "HAS_PHONE",
            "target": row["phone"],
            "evidence_source": "Persons",
            "evidence_id": row["person_id"]
        })

    # Phone -> Person mapping
    phone_to_person = dict(
        zip(persons["phone"].astype(str), persons["person_id"])
    )

    # -----------------------------
    # CDR CONNECTIONS
    # -----------------------------
    for _, row in cdr.iterrows():

        caller = phone_to_person.get(str(row["caller"]))
        receiver = phone_to_person.get(str(row["receiver"]))

        if caller and receiver:
            relationships.append({
                "source": caller,
                "relationship": "CONTACTED",
                "target": receiver,
                "evidence_source": "CDR",
                "evidence_id": row["call_id"]
            })

    # -----------------------------
    # BANK TRANSACTIONS
    # -----------------------------
    for _, row in bank.iterrows():

        # Person -> Account
        relationships.append({
            "source": row["from_person"],
            "relationship": "OWNS_ACCOUNT",
            "target": row["from_account"],
            "evidence_source": "Bank",
            "evidence_id": row["transaction_id"]
        })

        relationships.append({
            "source": row["to_person"],
            "relationship": "OWNS_ACCOUNT",
            "target": row["to_account"],
            "evidence_source": "Bank",
            "evidence_id": row["transaction_id"]
        })

        # Money transfer relationship
        relationships.append({
            "source": row["from_person"],
            "relationship": "TRANSFERRED_TO",
            "target": row["to_person"],
            "evidence_source": "Bank",
            "evidence_id": row["transaction_id"]
        })

    # -----------------------------
    # FIR ASSOCIATION
    # -----------------------------
    for _, row in fir.iterrows():

        relationships.append({
            "source": row["person_id"],
            "relationship": "ASSOCIATED_WITH_FIR",
            "target": row["fir_id"],
            "evidence_source": "FIR",
            "evidence_id": row["fir_id"]
        })

    # -----------------------------
    # SOCIAL MEDIA CONNECTION
    # -----------------------------
    for _, row in social.iterrows():

        relationships.append({
            "source": row["person_id"],
            "relationship": "SOCIAL_LINK",
            "target": row["linked_person"],
            "evidence_source": "Social Media",
            "evidence_id": row["record_id"]
        })

    return pd.DataFrame(relationships)