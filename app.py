import streamlit as st
import pandas as pd
import os
import networkx as nx
import plotly.graph_objects as go

from modules.entity_resolution import build_entity_relationships
from modules.pattern_detection import detect_patterns
from modules.risk_engine import calculate_investigation_priority
from modules.evidence_engine import get_evidence_for_entity
from modules.graph_engine import (
    build_graph,
    get_node_type
)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CipherTrace",
    page_icon="🔎",
    layout="wide"
)


# =========================================================
# SESSION STATE
# =========================================================

if "investigation_loaded" not in st.session_state:
    st.session_state.investigation_loaded = False


# =========================================================
# HEADER
# =========================================================

st.title("🔎 CipherTrace")

st.subheader(
    "AI-Powered Criminal Network Analysis System"
)

st.markdown(
    "Connecting fragmented investigation records "
    "into an explainable analysis network."
)

st.markdown("---")

# st.warning(
#     "⚠️ SIMULATED / DE-IDENTIFIED DATA — "
#     "Prototype demonstration only"
# )


# =========================================================
# DATA PATH
# =========================================================

DATA_PATH = "data"


def load_data(filename):

    path = os.path.join(
        DATA_PATH,
        filename
    )

    if not os.path.exists(path):

        st.error(
            f"Dataset not found: {path}"
        )

        return pd.DataFrame()

    return pd.read_csv(path)


# =========================================================
# TOP DASHBOARD
# =========================================================

st.header("📂 Investigation Workspace")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Data Sources",
        "5"
    )

with col2:
    st.metric(
        "Entity Types",
        "6"
    )

with col3:
    st.metric(
        "Investigation Case",
        "CT-2026-001"
    )

with col4:
    st.metric(
        "Status",
        "Ready"
    )

st.markdown("---")


# =========================================================
# LOAD BUTTON
# =========================================================

if st.button(
    "🚀 Load Demo Investigation",
    type="primary"
):

    st.session_state.investigation_loaded = True


# =========================================================
# INVESTIGATION WORKSPACE
# =========================================================

if st.session_state.investigation_loaded:

    # =====================================================
    # LOAD DATASETS
    # =====================================================

    persons = load_data(
        "persons.csv"
    )

    cdr = load_data(
        "cdr.csv"
    )

    bank = load_data(
        "bank_transactions.csv"
    )

    fir = load_data(
        "fir.csv"
    )

    social = load_data(
        "social_media.csv"
    )


    # =====================================================
    # CHECK DATA
    # =====================================================

    if any(
        df.empty
        for df in [
            persons,
            cdr,
            bank,
            fir,
            social
        ]
    ):

        st.error(
            "One or more datasets could not be loaded."
        )

        st.stop()


    st.success(
        "✅ Demo investigation loaded successfully!"
    )


    # =====================================================
    # ENTITY RESOLUTION
    # =====================================================

    relationships = build_entity_relationships(
        persons,
        cdr,
        bank,
        fir,
        social
    )


    # =====================================================
    # KNOWLEDGE GRAPH
    # =====================================================

    G = build_graph(
        relationships
    )


    # =====================================================
    # PATTERN DETECTION
    # =====================================================

    patterns = detect_patterns(
        G,
        relationships
    )


    # =====================================================
    # INVESTIGATION PRIORITY
    # =====================================================

    priority_results = calculate_investigation_priority(
        patterns
    )


    # =====================================================
    # TABS
    # =====================================================

    tabs = st.tabs(
        [
            "📊 Case Overview",
            "🕸️ Network",
            "🔎 Patterns",
            "🎯 Priority",
            "📁 Evidence"
        ]
    )


    # =====================================================
    # TAB 1 — CASE OVERVIEW
    # =====================================================

    with tabs[0]:

        st.header(
            "📊 Investigation Case Overview"
        )

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.metric(
                "Persons",
                len(persons)
            )

        with col2:
            st.metric(
                "CDR Records",
                len(cdr)
            )

        with col3:
            st.metric(
                "Transactions",
                len(bank)
            )

        with col4:
            st.metric(
                "FIR Records",
                len(fir)
            )

        with col5:
            st.metric(
                "Social Records",
                len(social)
            )


        st.divider()


        # CASE INFORMATION

        st.subheader(
            "📌 Case Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                "**Case ID:** CT-2026-001"
            )

            st.write(
                "**Status:** Ready for Analyst Review"
            )

            st.write(
                "**Data Mode:** Simulated / De-identified"
            )

        with col2:

            st.write(
                "**Analysis:** "
                "AI-assisted relationship analysis"
            )

            st.write(
                "**Graph Engine:** NetworkX"
            )

            st.write(
                "**Interface:** Streamlit"
            )


        st.info(
            "CipherTrace assists authorized investigators "
            "by connecting fragmented records and "
            "highlighting relationships for human review."
        )


        # ENTITY RESOLUTION

        st.subheader(
            "🔗 Entity Resolution"
        )

        st.write(
            "The system resolves relationships across "
            "multiple data sources and converts them "
            "into an investigation network."
        )


        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Resolved Relationships",
                len(relationships)
            )

        with col2:

            st.metric(
                "Graph Nodes",
                G.number_of_nodes()
            )

        with col3:

            st.metric(
                "Graph Connections",
                G.number_of_edges()
            )


        with st.expander(
            "View Resolved Relationships"
        ):

            st.dataframe(
                relationships,
                use_container_width=True
            )


        # DATASET PREVIEW

        st.subheader(
            "📚 Source Dataset Preview"
        )

        dataset = st.selectbox(
            "Select a data source",
            [
                "Persons",
                "CDR",
                "Bank Transactions",
                "FIR",
                "Social Media"
            ],
            key="dataset_selector"
        )


        if dataset == "Persons":

            st.dataframe(
                persons,
                use_container_width=True
            )

        elif dataset == "CDR":

            st.dataframe(
                cdr,
                use_container_width=True
            )

        elif dataset == "Bank Transactions":

            st.dataframe(
                bank,
                use_container_width=True
            )

        elif dataset == "FIR":

            st.dataframe(
                fir,
                use_container_width=True
            )

        elif dataset == "Social Media":

            st.dataframe(
                social,
                use_container_width=True
            )


    # =====================================================
    # TAB 2 — NETWORK
    # =====================================================

    with tabs[1]:

        st.header(
            "🕸️ CipherTrace Investigation Network"
        )

        st.write(
            "Interactive investigation graph showing "
            "cross-source relationships, entity types "
            "and detected network clusters."
        )

        # =================================================
        # ENTITY TYPE CONFIGURATION
        # =================================================

        ENTITY_COLORS = {

            "Person": "#8B5CF6",

            "Phone": "#2196F3",

            "Bank Account": "#F59E0B",

            "Transaction": "#EC4899",

            "FIR": "#EF4444",

            "Social Media": "#F97316",

            "Location": "#94A3B8",

            "Organization": "#10B981",

            "Travel": "#06B6D4",

            "Hidden / Unresolved": "#475569"
        }


        ENTITY_SYMBOLS = {

            "Person": "circle",

            "Phone": "square",

            "Bank Account": "diamond",

            "Transaction": "triangle",

            "FIR": "hexagon",

            "Social Media": "star",

            "Location": "circle",

            "Organization": "pentagon",

            "Travel": "cross",

            "Hidden / Unresolved": "x"
        }


        # =================================================
        # GRAPH METRICS
        # =================================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "Graph Nodes",
                G.number_of_nodes()
            )

        with col2:

            st.metric(
                "Graph Connections",
                G.number_of_edges()
            )

        with col3:

            st.metric(
                "Relationships",
                len(relationships)
            )

        with col4:

            st.metric(
                "Data Sources",
                relationships[
                    "evidence_source"
                ].nunique()
            )


        st.markdown("---")


        # =================================================
        # FILTER PANEL
        # =================================================

        filter_col, graph_col = st.columns(
            [1, 4]
        )


        with filter_col:

            st.subheader(
                "🎛️ Graph Filters"
            )


            # ---------------------------------------------
            # RELATIONSHIP FILTER
            # ---------------------------------------------

            relationship_types = sorted(
                relationships[
                    "relationship"
                ]
                .dropna()
                .unique()
                .tolist()
            )


            selected_relationships = st.multiselect(

                "Relationship Type",

                relationship_types,

                default=relationship_types,

                key="network_relationship_filter"
            )


            # ---------------------------------------------
            # ENTITY TYPE FILTER
            # ---------------------------------------------

            available_entity_types = sorted(
                set(
                    get_node_type(node)
                    for node in G.nodes()
                )
            )


            selected_entity_types = st.multiselect(

                "Entity Type",

                available_entity_types,

                default=available_entity_types,

                key="network_entity_type_filter"
            )


            # ---------------------------------------------
            # SEARCH
            # ---------------------------------------------

            search_entity = st.text_input(

                "🔎 Search Entity",

                placeholder=(
                    "Search P001, 9000000001..."
                ),

                key="network_entity_search"
            )


            # ---------------------------------------------
            # HIDDEN ENTITY TOGGLE
            # ---------------------------------------------

            show_hidden = st.checkbox(

                "👁️ Show Hidden / Unresolved",

                value=True,

                key="show_hidden_entities"
            )


            # ---------------------------------------------
            # RESET
            # ---------------------------------------------

            if st.button(
                "🔄 Reset Filters",
                key="reset_network_filters"
            ):

                st.session_state[
                    "network_relationship_filter"
                ] = relationship_types

                st.session_state[
                    "network_entity_type_filter"
                ] = available_entity_types

                st.session_state[
                    "network_entity_search"
                ] = ""

                st.session_state[
                    "show_hidden_entities"
                ] = True

                st.rerun()


            st.markdown("---")


            # ---------------------------------------------
            # LEGEND
            # ---------------------------------------------

            st.subheader(
                "🧩 Entity Legend"
            )


            for entity_type in available_entity_types:

                if (
                    entity_type
                    == "Hidden / Unresolved"
                ):

                    icon = "👁️"

                elif entity_type == "Person":
                    icon = "👤"

                elif entity_type == "Phone":
                    icon = "📱"

                elif entity_type == "Bank Account":
                    icon = "🏦"

                elif entity_type == "Transaction":
                    icon = "💱"

                elif entity_type == "FIR":
                    icon = "📄"

                elif entity_type == "Social Media":
                    icon = "🌐"

                elif entity_type == "Location":
                    icon = "📍"

                elif entity_type == "Organization":
                    icon = "🏢"

                elif entity_type == "Travel":
                    icon = "✈️"

                else:
                    icon = "🔗"


                count = sum(
                    1
                    for node in G.nodes()
                    if get_node_type(node)
                    == entity_type
                )


                st.markdown(
                    f"{icon} **{entity_type}** "
                    f"({count})"
                )


        # =================================================
        # FILTER RELATIONSHIPS
        # =================================================

        filtered_relationships = relationships[
            relationships[
                "relationship"
            ].isin(
                selected_relationships
            )
        ].copy()


        # =================================================
        # BUILD FILTERED GRAPH
        # =================================================

        filtered_graph = build_graph(
            filtered_relationships
        )


        # =================================================
        # FILTER ENTITY TYPES
        # =================================================

        nodes_to_remove = []


        for node in filtered_graph.nodes():

            node_type = get_node_type(
                node
            )


            # Hidden entity filter
            if (
                node_type
                == "Hidden / Unresolved"
                and not show_hidden
            ):

                nodes_to_remove.append(
                    node
                )

                continue


            # Entity type filter
            if (
                node_type
                not in selected_entity_types
            ):

                nodes_to_remove.append(
                    node
                )


        filtered_graph.remove_nodes_from(
            nodes_to_remove
        )


        # =================================================
        # SEARCH ENTITY
        # =================================================

        if search_entity.strip():

            search_text = (
                search_entity
                .strip()
                .lower()
            )


            matching_nodes = [

                node

                for node in filtered_graph.nodes()

                if search_text
                in str(node).lower()
            ]


            if matching_nodes:

                # Keep matching nodes + neighbors

                nodes_to_keep = set(
                    matching_nodes
                )


                for node in matching_nodes:

                    nodes_to_keep.update(
                        filtered_graph.neighbors(
                            node
                        )
                    )


                filtered_graph = (
                    filtered_graph.subgraph(
                        nodes_to_keep
                    ).copy()
                )

                st.success(
                    f"🔎 Found {len(matching_nodes)} "
                    f"matching entity(s)."
                )

            else:

                st.warning(
                    "No matching entity found."
                )


        # =================================================
        # GRAPH AREA
        # =================================================

        with graph_col:

            if (
                filtered_graph.number_of_nodes()
                == 0
            ):

                st.info(
                    "No entities match the selected filters."
                )

            else:

                # -----------------------------------------
                # GRAPH LAYOUT
                # -----------------------------------------

                pos = nx.spring_layout(

                    filtered_graph,

                    seed=42,

                    k=1.6,

                    iterations=100
                )


                # =========================================
                # GRAPH EDGES
                # =========================================

                edge_x = []
                edge_y = []
                edge_hover = []


                for source, target, data in (
                    filtered_graph.edges(
                        data=True
                    )
                ):

                    x0, y0 = pos[
                        source
                    ]

                    x1, y1 = pos[
                        target
                    ]


                    edge_x.extend(
                        [
                            x0,
                            x1,
                            None
                        ]
                    )


                    edge_y.extend(
                        [
                            y0,
                            y1,
                            None
                        ]
                    )


                    edge_hover.append(
                        f"{source} → {target}<br>"
                        f"Relationship: "
                        f"{data.get('relationship', 'Unknown')}<br>"
                        f"Source: "
                        f"{data.get('evidence_source', 'Unknown')}<br>"
                        f"Evidence ID: "
                        f"{data.get('evidence_id', 'Unknown')}"
                    )


                edge_trace = go.Scatter(

                    x=edge_x,

                    y=edge_y,

                    mode="lines",

                    hoverinfo="none",

                    line=dict(
                        width=1.3
                    )
                )


                # =========================================
                # CLUSTER DETECTION
                # =========================================

                try:

                    communities = (
                        nx.community
                        .greedy_modularity_communities(
                            filtered_graph
                        )
                    )

                except Exception:

                    communities = []


                # =========================================
                # CREATE GRAPH FIGURE
                # =========================================

                fig = go.Figure()


                # Add edges first

                fig.add_trace(
                    edge_trace
                )


                # =========================================
                # CLUSTER BOUNDARIES
                # =========================================

                # Relationship → readable cluster category
                RELATIONSHIP_CATEGORY = {

                    "CONTACTED": "Communication Network",

                    "HAS_PHONE": "Communication Network",

                    "TRANSFERRED_TO": "Financial Network",

                    "OWNS_ACCOUNT": "Financial Network",

                    "SOCIAL_LINK": "Social Network",

                    "ASSOCIATED_WITH_FIR": "Investigation Network"
                }


                for index, community in enumerate(communities):

                    community_nodes = [
                        node
                        for node in community
                        if node in filtered_graph.nodes()
                    ]

                    # Ignore extremely small communities
                    if len(community_nodes) < 2:
                        continue


                    # -----------------------------------------
                    # FIND RELATIONSHIPS INSIDE THIS CLUSTER
                    # -----------------------------------------

                    community_set = set(
                        community_nodes
                    )

                    cluster_relationships = (
                        filtered_relationships[
                            filtered_relationships["source"]
                            .astype(str)
                            .isin(community_set)
                            &
                            filtered_relationships["target"]
                            .astype(str)
                            .isin(community_set)
                        ]
                    )


                    # -----------------------------------------
                    # DETERMINE DOMINANT CLUSTER TYPE
                    # -----------------------------------------

                    categories = []

                    for relationship in (
                        cluster_relationships[
                            "relationship"
                        ]
                    ):

                        category = RELATIONSHIP_CATEGORY.get(
                            relationship,
                            "Cross-Source Network"
                        )

                        categories.append(
                            category
                        )


                    if categories:

                        category_counts = (
                            pd.Series(categories)
                            .value_counts()
                        )

                        cluster_name = (
                            category_counts
                            .index[0]
                        )

                    else:

                        cluster_name = (
                            "Cross-Source Network"
                        )


                    # -----------------------------------------
                    # CLUSTER BOUNDARY
                    # -----------------------------------------

                    points = [
                        pos[node]
                        for node in community_nodes
                    ]

                    xs = [
                        point[0]
                        for point in points
                    ]

                    ys = [
                        point[1]
                        for point in points
                    ]

                    min_x = min(xs)
                    max_x = max(xs)

                    min_y = min(ys)
                    max_y = max(ys)


                    # Padding around cluster

                    width = max_x - min_x
                    height = max_y - min_y

                    padding_x = max(
                        width * 0.30,
                        0.08
                    )

                    padding_y = max(
                        height * 0.30,
                        0.08
                    )


                    # -----------------------------------------
                    # CLUSTER COLORS
                    # -----------------------------------------

                    cluster_colors = [
                        "#22D3EE",
                        "#F59E0B",
                        "#EC4899",
                        "#EF4444",
                        "#A3E635",
                        "#8B5CF6"
                    ]

                    color = cluster_colors[
                        index % len(cluster_colors)
                    ]


                    # -----------------------------------------
                    # DASHED CLUSTER BOUNDARY
                    # -----------------------------------------

                    fig.add_shape(

                        type="circle",

                        xref="x",

                        yref="y",

                        x0=min_x - padding_x,

                        x1=max_x + padding_x,

                        y0=min_y - padding_y,

                        y1=max_y + padding_y,

                        line=dict(
                            color=color,
                            width=1.5,
                            dash="dash"
                        ),

                        fillcolor="rgba(0,0,0,0)",

                        layer="below"
                    )


                    # -----------------------------------------
                    # CLUSTER LABEL
                    # -----------------------------------------

                    center_x = (
                        min_x + max_x
                    ) / 2

                    center_y = (
                        max_y + padding_y
                    )


                    fig.add_annotation(

                        x=center_x,

                        y=center_y,

                        xref="x",

                        yref="y",

                        text=(
                            f"<b>Cluster {index + 1}</b><br>"
                            f"{cluster_name}"
                        ),

                        showarrow=False,

                        font=dict(
                            size=10,
                            color=color
                        ),

                        bgcolor=(
                            "rgba(10,20,35,0.80)"
                        ),

                        bordercolor=color,

                        borderwidth=1,

                        borderpad=4
                    )


                # =========================================
                # NODE TRACES BY ENTITY TYPE
                # =========================================

                for entity_type in ENTITY_COLORS:

                    nodes = [

                        node

                        for node
                        in filtered_graph.nodes()

                        if get_node_type(node)
                        == entity_type
                    ]


                    if not nodes:

                        continue


                    node_x = []
                    node_y = []
                    node_text = []
                    node_hover = []
                    node_sizes = []


                    for node in nodes:

                        x, y = pos[node]


                        node_x.append(x)

                        node_y.append(y)


                        degree = (
                            filtered_graph.degree(
                                node
                            )
                        )


                        node_sizes.append(
                            min(
                                24 + degree * 5,
                                50
                            )
                        )


                        node_text.append(
                            str(node)
                        )


                        node_hover.append(

                            f"<b>{node}</b><br>"

                            f"Type: {entity_type}<br>"

                            f"Connections: {degree}"
                        )


                    fig.add_trace(
                        go.Scatter(

                            x=node_x,

                            y=node_y,

                            mode=(
                                "markers+text"
                            ),

                            text=node_text,

                            textposition=(
                                "top center"
                            ),

                            hovertext=node_hover,

                            hoverinfo="text",

                            name=entity_type,

                            marker=dict(

                                size=node_sizes,

                                color=(
                                    ENTITY_COLORS[
                                        entity_type
                                    ]
                                ),

                                symbol=(
                                    ENTITY_SYMBOLS[
                                        entity_type
                                    ]
                                ),

                                line=dict(
                                    width=1.5,
                                    color="white"
                                )
                            )
                        )
                    )


                # =========================================
                # GRAPH LAYOUT
                # =========================================

                fig.update_layout(

                    title=dict(

                        text=(
                            "🕸️ CipherTrace "
                            "Investigation Graph"
                        ),

                        x=0.5
                    ),

                    showlegend=True,

                    legend=dict(

                        title="Entity Types",

                        orientation="v",

                        x=1.02,

                        y=1,

                        bgcolor=(
                            "rgba(15,23,42,0.85)"
                        )
                    ),

                    hovermode="closest",

                    height=720,

                    margin=dict(

                        l=20,

                        r=180,

                        t=70,

                        b=20
                    ),

                    paper_bgcolor=(
                        "rgba(0,0,0,0)"
                    ),

                    plot_bgcolor=(
                        "rgba(0,0,0,0)"
                    ),

                    xaxis=dict(

                        showgrid=False,

                        zeroline=False,

                        showticklabels=False,

                        showline=False
                    ),

                    yaxis=dict(

                        showgrid=False,

                        zeroline=False,

                        showticklabels=False,

                        showline=False
                    )
                )


                st.plotly_chart(

                    fig,

                    use_container_width=True,

                    key="ciphertrace_network_graph"
                )


        # =================================================
        # GRAPH SUMMARY
        # =================================================

        st.markdown("---")

        st.subheader(
            "📊 Visible Graph Summary"
        )


        summary_col1, summary_col2, summary_col3 = (
            st.columns(3)
        )


        with summary_col1:

            st.metric(
                "Visible Entities",
                filtered_graph.number_of_nodes()
            )


        with summary_col2:

            st.metric(
                "Visible Connections",
                filtered_graph.number_of_edges()
            )


        with summary_col3:

            st.metric(
                "Detected Clusters",
                len(communities)
            )


        # =================================================
        # RELATIONSHIP TABLE
        # =================================================

        with st.expander(
            "🔍 View Underlying Relationships"
        ):

            visible_nodes = set(
                filtered_graph.nodes()
            )


            visible_relationships = (
                filtered_relationships[
                    filtered_relationships[
                        "source"
                    ].astype(str).isin(
                        visible_nodes
                    )
                    |
                    filtered_relationships[
                        "target"
                    ].astype(str).isin(
                        visible_nodes
                    )
                ]
            )


            st.dataframe(

                visible_relationships[
                    [
                        "source",
                        "relationship",
                        "target",
                        "evidence_source",
                        "evidence_id"
                    ]
                ],

                use_container_width=True
            )
    


    # =====================================================
    # TAB 3 — PATTERNS
    # =====================================================

    with tabs[2]:

        st.header(
            "🔎 Investigation Pattern Detection"
        )

        st.write(
            "CipherTrace identifies relationship patterns "
            "across the investigation graph."
        )


        if len(patterns) > 0:

            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "Patterns Detected",
                    len(patterns)
                )


            with col2:

                high_count = len(
                    patterns[
                        patterns[
                            "priority"
                        ] == "High"
                    ]
                )

                st.metric(
                    "High Priority Patterns",
                    high_count
                )


            with col3:

                medium_count = len(
                    patterns[
                        patterns[
                            "priority"
                        ] == "Medium"
                    ]
                )

                st.metric(
                    "Medium Priority Patterns",
                    medium_count
                )


            st.markdown("---")


            st.dataframe(
                patterns,
                use_container_width=True
            )


            st.subheader(
                "📌 Pattern Breakdown"
            )


            pattern_counts = (
                patterns[
                    "pattern_type"
                ]
                .value_counts()
                .reset_index()
            )


            pattern_counts.columns = [
                "Pattern Type",
                "Count"
            ]


            st.dataframe(
                pattern_counts,
                use_container_width=True
            )


        else:

            st.info(
                "No investigation patterns detected."
            )


    # =====================================================
    # TAB 4 — PRIORITY
    # =====================================================

    with tabs[3]:

        st.header(
            "🎯 Investigation Priority"
        )

        st.write(
            "The priority engine helps analysts identify "
            "observed entities or relationships that may "
            "require closer review."
        )


        if len(priority_results) > 0:

            high_priority = len(
                priority_results[
                    priority_results[
                        "priority"
                    ] == "High"
                ]
            )


            medium_priority = len(
                priority_results[
                    priority_results[
                        "priority"
                    ] == "Medium"
                ]
            )


            low_priority = len(
                priority_results[
                    priority_results[
                        "priority"
                    ] == "Low"
                ]
            )


            col1, col2, col3 = st.columns(3)


            with col1:

                st.metric(
                    "High",
                    high_priority
                )


            with col2:

                st.metric(
                    "Medium",
                    medium_priority
                )


            with col3:

                st.metric(
                    "Low",
                    low_priority
                )


            st.markdown("---")


            st.subheader(
                "📋 Prioritized Investigation Entities"
            )


            display_priority = (
                priority_results
                .sort_values(
                    "priority_score",
                    ascending=False
                )
            )


            st.dataframe(
                display_priority[
                    [
                        "entity",
                        "priority_score",
                        "priority",
                        "reasons"
                    ]
                ],
                use_container_width=True
            )


            # EXPLAINABLE ALERT

            st.subheader(
                "🚨 Explainable Investigation Alert"
            )


            top_index = (
                priority_results[
                    "priority_score"
                ].idxmax()
            )


            top_entity = (
                priority_results.loc[
                    top_index
                ]
            )


            st.warning(
                "Investigation Priority: "
                f"{top_entity['priority_score']}/100"
            )


            st.write(
                f"**Entity / Relationship:** "
                f"{top_entity['entity']}"
            )


            st.write(
                f"**Priority Level:** "
                f"{top_entity['priority']}"
            )


            st.write(
                "**Why this was highlighted:**"
            )


            reasons = str(
                top_entity["reasons"]
            ).split("; ")


            for reason in reasons:

                st.write(
                    f"• {reason}"
                )


            st.caption(
                "This priority is an analytical aid for "
                "human review. It does not indicate guilt "
                "or criminality."
            )


            st.info(
                "👤 Human-in-the-loop: Final interpretation "
                "and investigative action remain with the "
                "authorized analyst."
            )


        else:

            st.info(
                "No entities are currently available "
                "for prioritization."
            )


        # =====================================================
        # TAB 5 — ENTITY EXPLORER + EVIDENCE
        # =====================================================

        with tabs[4]:

            st.header(
                "🔎 Investigator Entity Explorer"
            )

            st.write(
                "Select an entity to inspect its cross-source "
                "relationships and supporting evidence."
            )

            st.markdown("---")

            # -------------------------------------------------
            # ENTITY LIST
            # -------------------------------------------------

            person_ids = persons[
                "person_id"
            ].astype(str).tolist()

            selected_person = st.selectbox(
                "👤 Select an entity",
                person_ids,
                key="investigator_entity_selector"
            )

            # -------------------------------------------------
            # PERSON INFORMATION
            # -------------------------------------------------

            person_data = persons[
                persons["person_id"].astype(str)
                == selected_person
            ]

            if len(person_data) > 0:

                person = person_data.iloc[0]

                st.subheader(
                    "👤 Entity Profile"
                )

                col1, col2, col3, col4 = st.columns(4)

                with col1:

                    st.metric(
                        "Entity ID",
                        person["person_id"]
                    )

                with col2:

                    st.metric(
                        "Name",
                        person["name"]
                    )

                with col3:

                    st.metric(
                        "Phone",
                        person["phone"]
                    )

                with col4:

                    st.metric(
                        "Location",
                        person["location"]
                    )

            st.markdown("---")

            # -------------------------------------------------
            # FIND DIRECT RELATIONSHIPS
            # -------------------------------------------------

            entity_relationships = relationships[
                (
                    relationships["source"]
                    .astype(str)
                    == selected_person
                )
                |
                (
                    relationships["target"]
                    .astype(str)
                    == selected_person
                )
            ].copy()

            # -------------------------------------------------
            # ENTITY METRICS
            # -------------------------------------------------

            st.subheader(
                "🔗 Relationship Summary"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Direct Relationships",
                    len(entity_relationships)
                )

            with col2:

                connected_entities = set()

                for _, row in entity_relationships.iterrows():

                    if str(row["source"]) == selected_person:
                        connected_entities.add(
                            str(row["target"])
                        )

                    if str(row["target"]) == selected_person:
                        connected_entities.add(
                            str(row["source"])
                        )

                st.metric(
                    "Connected Entities",
                    len(connected_entities)
                )

            with col3:

                evidence_sources = (
                    entity_relationships[
                        "evidence_source"
                    ]
                    .nunique()
                )

                st.metric(
                    "Evidence Sources",
                    evidence_sources
                )

            # -------------------------------------------------
            # RELATIONSHIP TABLE
            # -------------------------------------------------

            st.subheader(
                "🔗 Cross-Source Relationships"
            )

            if len(entity_relationships) > 0:

                st.dataframe(
                    entity_relationships[
                        [
                            "source",
                            "relationship",
                            "target",
                            "evidence_source",
                            "evidence_id"
                        ]
                    ],
                    use_container_width=True
                )

            else:

                st.info(
                    "No direct relationships found."
                )

            # -------------------------------------------------
            # CONNECTION LIST
            # -------------------------------------------------

            st.subheader(
                "🌐 Connected Entities"
            )

            if len(connected_entities) > 0:

                connected_rows = []

                for entity in sorted(
                    connected_entities
                ):

                    entity_type = "Entity"

                    entity_str = str(entity)

                    if entity_str.startswith("P"):
                        entity_type = "Person"

                    elif entity_str.startswith("A"):
                        entity_type = "Bank Account"

                    elif entity_str.startswith("F"):
                        entity_type = "FIR"

                    elif (
                        entity_str.isdigit()
                        and len(entity_str) >= 10
                    ):
                        entity_type = "Phone"

                    connected_rows.append(
                        {
                            "Entity": entity,
                            "Type": entity_type
                        }
                    )

                st.dataframe(
                    pd.DataFrame(
                        connected_rows
                    ),
                    use_container_width=True
                )

            # -------------------------------------------------
            # EVIDENCE TRAIL
            # -------------------------------------------------

            st.markdown("---")

            st.subheader(
                "📁 Source-Linked Evidence Trail"
            )

            if len(entity_relationships) > 0:

                st.success(
                    f"✅ {len(entity_relationships)} "
                    "supporting relationship records found."
                )

                evidence_summary = (
                    entity_relationships[
                        "evidence_source"
                    ]
                    .value_counts()
                    .reset_index()
                )

                evidence_summary.columns = [
                    "Evidence Source",
                    "Records"
                ]

                st.dataframe(
                    evidence_summary,
                    use_container_width=True
                )

                st.markdown(
                    "### 📌 Evidence Records"
                )

                for _, row in entity_relationships.iterrows():

                    with st.expander(
                        f"{row['evidence_source']} — "
                        f"{row['evidence_id']}"
                    ):

                        st.write(
                            f"**Source Entity:** "
                            f"{row['source']}"
                        )

                        st.write(
                            f"**Relationship:** "
                            f"{row['relationship']}"
                        )

                        st.write(
                            f"**Target Entity:** "
                            f"{row['target']}"
                        )

                        st.write(
                            f"**Evidence Source:** "
                            f"{row['evidence_source']}"
                        )

                        st.write(
                            f"**Evidence ID:** "
                            f"{row['evidence_id']}"
                        )

            else:

                st.info(
                    "No source-linked evidence found "
                    "for this entity."
                )

            # -------------------------------------------------
            # ANALYST NOTE
            # -------------------------------------------------

            st.markdown("---")

            st.info(
                "👤 Analyst Review: CipherTrace presents "
                "cross-source relationships and evidence for "
                "authorized human investigation. The system "
                "does not determine guilt or criminality."
            )


# =========================================================
# BEFORE LOADING
# =========================================================

else:

    st.info(
        "👆 Click **Load Demo Investigation** "
        "to start the analysis."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.caption(
    "CipherTrace | SIH 2026 Prototype | "
    "AI-assisted investigation analysis | "
    "Simulated data only"
)