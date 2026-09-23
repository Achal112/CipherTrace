import networkx as nx


def get_node_type(node):
    """
    Identify the entity type from the node ID.
    """

    node = str(node)

    if node.startswith("P"):
        return "Person"

    elif node.startswith("A"):
        return "Bank Account"

    elif node.startswith("F"):
        return "FIR"

    elif node.startswith("T"):
        return "Transaction"

    elif node.startswith("S"):
        return "Social Media"

    elif node.startswith("L"):
        return "Location"

    elif node.startswith("ORG"):
        return "Organization"

    elif node.startswith("TR"):
        return "Travel"

    elif node.isdigit() and len(node) >= 10:
        return "Phone"

    else:
        return "Hidden / Unresolved"


def build_graph(relationships):

    G = nx.Graph()

    for _, row in relationships.iterrows():

        source = str(row["source"])
        target = str(row["target"])

        G.add_node(
            source,
            node_type=get_node_type(source)
        )

        G.add_node(
            target,
            node_type=get_node_type(target)
        )

        G.add_edge(
            source,
            target,
            relationship=str(row["relationship"]),
            evidence_source=str(
                row["evidence_source"]
            ),
            evidence_id=str(
                row["evidence_id"]
            )
        )

    return G