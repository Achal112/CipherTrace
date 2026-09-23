import networkx as nx
import pandas as pd


def detect_patterns(G, relationships):

    patterns = []

    # HIGH CONNECTIVITY
    degree = dict(G.degree())

    for node, count in degree.items():

        if count >= 3:

            patterns.append({
                "pattern_type": "High Connectivity",
                "entity": str(node),
                "entity_id": str(node),
                "source_entity": str(node),
                "target_entity": "",
                "details": f"{count} direct connections",
                "priority": "High"
            })

    # REPEATED CONTACT
    contact_data = relationships[
        relationships["relationship"] == "CONTACTED"
    ]

    contact_counts = (
        contact_data
        .groupby(["source", "target"])
        .size()
        .reset_index(name="count")
    )

    for _, row in contact_counts.iterrows():

        if row["count"] >= 2:

            source = str(row["source"])
            target = str(row["target"])

            patterns.append({
                "pattern_type": "Repeated Contact",
                "entity": f"{source} → {target}",
                "entity_id": source,
                "source_entity": source,
                "target_entity": target,
                "details": f"{row['count']} recorded contacts",
                "priority": "Medium"
            })

    # FINANCIAL TRANSFER
    transfer_data = relationships[
        relationships["relationship"] == "TRANSFERRED_TO"
    ]

    for _, row in transfer_data.iterrows():

        source = str(row["source"])
        target = str(row["target"])

        patterns.append({
            "pattern_type": "Financial Transfer",
            "entity": f"{source} → {target}",
            "entity_id": source,
            "source_entity": source,
            "target_entity": target,
            "details": "Recorded financial relationship",
            "priority": "Medium"
        })

    # CROSS-SOURCE CONNECTION
    pair_sources = {}

    for _, row in relationships.iterrows():

        source = str(row["source"])
        target = str(row["target"])

        pair = tuple(sorted([source, target]))

        pair_sources.setdefault(pair, set()).add(
            row["evidence_source"]
        )

    for pair, sources in pair_sources.items():

        if len(sources) >= 2:

            source = pair[0]
            target = pair[1]

            patterns.append({
                "pattern_type": "Cross-Source Connection",
                "entity": f"{source} ↔ {target}",
                "entity_id": source,
                "source_entity": source,
                "target_entity": target,
                "details": f"Supported by {len(sources)} data sources",
                "priority": "High"
            })

    return pd.DataFrame(patterns)
