import pandas as pd


def get_evidence_for_entity(
    entity,
    relationships
):

    entity = str(entity)


    # =====================================================
    # DIRECT ENTITY MATCH
    # =====================================================

    evidence = relationships[
        (
            relationships[
                "source"
            ]
            .astype(str)
            == entity
        )
        |
        (
            relationships[
                "target"
            ]
            .astype(str)
            == entity
        )
    ].copy()


    return evidence