# visualizer.py
import hashlib
import streamlit as st
from typing import List, Dict, Optional
from logger import logger

try:
    import networkx as nx
except ImportError:
    nx = None
try:
    from pyvis.network import Network
except ImportError:
    Network = None

def _get_data_hash(data):
    if not data:
        return "empty"
    content = str(sorted([(d.get("实体1",""), d.get("关系",""), d.get("实体2","")) for d in data]))
    return hashlib.md5(content.encode()).hexdigest()[:16]

def _clear_graph_cache(cache_key=None):
    keys = [k for k in st.session_state if k.startswith("kg_cache_") and (cache_key is None or cache_key in k)]
    for k in keys:
        del st.session_state[k]

def plot_interactive_kg_graph(data: List[Dict], cache_key="default", max_display=200, height="700px"):
    if nx is None or Network is None:
        st.error("Missing networkx or pyvis")
        return False
    if not data:
        st.info("No data")
        return False
    total = len(data)
    if total > max_display:
        st.warning(f"Data large ({total}), showing first {max_display}")
        data = data[:max_display]
    html_key = f"kg_cache_{cache_key}_html"
    hash_key = f"kg_cache_{cache_key}_hash"
    cur_hash = _get_data_hash(data)
    if st.session_state.get(hash_key) == cur_hash and st.session_state.get(html_key):
        st.components.v1.html(st.session_state[html_key], height=height)
        return True
    with st.spinner("Generating graph..."):
        G = nx.DiGraph()
        for item in data:
            e1 = str(item.get("实体1",""))
            e2 = str(item.get("实体2",""))
            rel = str(item.get("关系",""))
            if e1 and e2:
                G.add_edge(e1, e2, relation=rel)
        net = Network(directed=True, height=height, width="100%", bgcolor="#f8f9fa", font_color="#2c3e50", cdn_resources="in_line")
        for node in G.nodes():
            degree = G.degree(node)
            size = 20 + min(degree*3, 40)
            net.add_node(node, label=node, title=node, size=size)
        for edge in G.edges(data=True):
            rel = edge[2].get("relation","关联")
            net.add_edge(edge[0], edge[1], title=rel, label=rel, arrows="to")
        net.set_options("""
{
  "physics": {"stabilization": {"iterations": 50, "fit": true},"forceAtlas2Based": {"gravitationalConstant": -50, "centralGravity": 0.005, "springLength": 100, "springConstant": 0.08, "damping": 0.4}},
  "interaction": {"hover": true, "tooltipDelay": 200},
  "edges": {"smooth": true, "font": {"size": 12}, "color": {"color": "#85929e", "highlight": "#e74c3c"}},
  "nodes": {"font": {"size": 14}, "borderWidth": 2, "color": {"border": "#3498db", "background": "#ecf0f1"}}
}
""")
        html = net.generate_html()
        st.session_state[html_key] = html
        st.session_state[hash_key] = cur_hash
        st.components.v1.html(html, height=height)
        return True