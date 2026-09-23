import pandas as pd


def calculate_investigation_priority(patterns):

    scores = {}

    reasons = {}

    entity_info = {}


    # =====================================================
    # CALCULATE SCORES
    # =====================================================

    for _, row in patterns.iterrows():

        entity_id = str(
            row["entity_id"]
        )

        pattern_type = row[
            "pattern_type"
        ]


        if entity_id not in scores:

            scores[entity_id] = 0

            reasons[entity_id] = []

            entity_info[entity_id] = {
                "entity": row["entity"],
                "source_entity": row[
                    "source_entity"
                ],
                "target_entity": row[
                    "target_entity"
                ]
            }


        # ---------------------------------------------
        # SCORE RULES
        # ---------------------------------------------

        if pattern_type == "High Connectivity":

            points = 25

        elif pattern_type == "Cross-Source Connection":

            points = 25

        elif pattern_type == "Financial Transfer":

            points = 15

        elif pattern_type == "Repeated Contact":

            points = 15

        else:

            points = 5


        scores[entity_id] += points


        reasons[entity_id].append(
            f"{pattern_type} (+{points})"
        )


    # =====================================================
    # CREATE RESULTS
    # =====================================================

    results = []


    for entity_id, score in scores.items():

        score = min(
            score,
            100
        )


        if score >= 70:

            priority = "High"

        elif score >= 40:

            priority = "Medium"

        else:

            priority = "Low"


        results.append({

            "entity_id": entity_id,

            "entity": entity_info[
                entity_id
            ]["entity"],

            "source_entity": entity_info[
                entity_id
            ]["source_entity"],

            "target_entity": entity_info[
                entity_id
            ]["target_entity"],

            "priority_score": score,

            "priority": priority,

            "reasons": "; ".join(
                reasons[entity_id]
            )
        })


    return pd.DataFrame(
        results
    )