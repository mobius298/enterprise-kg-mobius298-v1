# pages.py
import streamlit as st
import pandas as pd
from io import StringIO
import config
from logger import logger
from file_parser import parse_file
from nlp_processor import extract_triples
import csv_manager as csv_mgr
from visualizer import plot_interactive_kg_graph, _clear_graph_cache

try:
    from neo4j_ops import kg
except ImportError:
    kg = None

def home_page():
    st.title("🏢 企业知识图谱平台")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📖 项目背景")
        st.markdown("- 信息爆炸：非结构化数据价值沉睡\n- 检索困境：关键词无法发现深层关联\n- 智能互联：知识图谱结构化网络")
    with c2:
        st.subheader("🎯 核心目标")
        st.markdown("- 端到端平台\n- 自动化图谱转换\n- 可视化知识探索\n- 前沿技术融合")
    st.markdown("---")
    if st.button("📤 上传文档"):
        st.session_state["page"] = "📄 文档上传"
        st.rerun()
    if st.button("🔍 知识检索"):
        st.session_state["page"] = "🔍 知识检索"
        st.rerun()
    if st.button("🗺️ 图谱展示"):
        st.session_state["page"] = "🗺️ 图谱展示"
        st.rerun()
    st.markdown("---")
    neo_ok = kg is not None
    st.metric("Neo4j", "✅ 已连接" if neo_ok else "❌ 未连接")
    st.metric("LLM", "模拟模式" if config.USE_MOCK_LLM else "真实API")
    st.metric("CSV数据", "存在" if csv_mgr.show_csv() is not None else "暂无")

def upload_page():
    st.title("📄 文档上传与知识抽取")
    uploaded = st.file_uploader("选择文档", type=config.SUPPORTED_TYPES)
    if uploaded:
        text = parse_file(uploaded)
        if text:
            st.success(f"解析成功，长度 {len(text)}")
            with st.expander("预览"):
                st.text(text[:2000])
            if st.button("🔮 开始知识抽取"):
                triples = extract_triples(text)
                if triples:
                    st.success(f"获得 {len(triples)} 个三元组")
                    df = pd.DataFrame(triples, columns=["实体1","关系","实体2"])
                    st.dataframe(df)
                    if st.button("💾 保存到CSV"):
                        csv_mgr.save_to_csv(triples)
                        st.success("已保存")
                        _clear_graph_cache("full_graph")
                else:
                    st.warning("未抽取到三元组")
        else:
            st.error("解析失败")

def csv_page():
    st.title("📊 CSV中间层管理")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("刷新"): st.rerun()
    with col2:
        if st.button("清空CSV"):
            csv_mgr.clear_csv()
            st.rerun()
    with col3:
        if st.button("生成CQL"):
            cql = csv_mgr.generate_neo4j_import_cql()
            if cql:
                st.success("CQL生成成功")
    with col4:
        df = csv_mgr.show_csv()
        if df is not None:
            csv = StringIO()
            df.to_csv(csv, index=False)
            st.download_button("下载CSV", csv.getvalue(), config.CSV_FILE)
    df = csv_mgr.show_csv()
    if df is not None:
        st.dataframe(df)
    else:
        st.info("暂无数据")

def import_page():
    st.title("💾 Neo4j导入")
    if kg is None:
        st.error("Neo4j未连接")
        return
    import os
    if os.path.exists(config.IMPORT_CQL):
        with open(config.IMPORT_CQL) as f:
            cql = f.read()
        with st.expander("CQL脚本"):
            st.code(cql)
        if st.button("执行导入"):
            statements = [s.strip() for s in cql.split("\n") if s.strip()]
            progress = st.progress(0)
            success = 0
            for i, s in enumerate(statements):
                if kg.run_cql(s):
                    success += 1
                progress.progress((i+1)/len(statements))
            st.success(f"成功 {success}/{len(statements)}")
            _clear_graph_cache("full_graph")
    else:
        st.warning("CQL脚本不存在，请先生成")

def search_page():
    st.title("🔍 知识检索")
    if kg is None:
        st.error("Neo4j未连接")
        return
    kw = st.text_input("关键词")
    if kw:
        res = kg.search(kw)
        if res:
            st.dataframe(pd.DataFrame(res))
            plot_interactive_kg_graph(res, cache_key=f"search_{kw}")
        else:
            st.info("未找到")

def graph_page():
    st.title("🗺️ 全量知识图谱")
    if kg is None:
        st.error("Neo4j未连接")
        return
    if st.button("刷新"):
        _clear_graph_cache("full_graph")
        st.rerun()
    data = kg.get_all()
    if data:
        with st.expander("原始数据"):
            st.dataframe(pd.DataFrame(data))
        plot_interactive_kg_graph(data, cache_key="full_graph", height="750px")
    else:
        st.info("暂无数据")

def admin_page():
    st.title("⚙️ 系统管理")
    tab1, tab2, tab3 = st.tabs(["数据库", "缓存", "配置"])
    with tab1:
        if kg:
            stats = kg.get_statistics()
            st.metric("节点", stats["nodes"])
            st.metric("关系", stats["relationships"])
            if st.button("清空数据库"):
                kg.reset()
                _clear_graph_cache()
                st.rerun()
    with tab2:
        if st.button("清除所有图谱缓存"):
            _clear_graph_cache()
            st.success("已清除")
    with tab3:
        st.json({
            "NEO4J_URI": config.NEO4J_URI,
            "LLM_MODEL": config.LLM_MODEL,
            "USE_MOCK_LLM": config.USE_MOCK_LLM,
            "MAX_TEXT_LENGTH": config.MAX_TEXT_LENGTH
        })