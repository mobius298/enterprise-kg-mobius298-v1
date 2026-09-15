# main.py
import streamlit as st
from pages import home_page, upload_page, csv_page, import_page, search_page, graph_page, admin_page

st.set_page_config(page_title="企业知识图谱", layout="wide")

def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "🏠 首页"
    menu = ["🏠 首页", "📄 文档上传", "📊 CSV管理", "💾 导入Neo4j", "🔍 知识检索", "🗺️ 图谱展示", "⚙️ 系统管理"]
    selected = st.sidebar.radio("功能菜单", menu, index=menu.index(st.session_state["page"]))
    if selected != st.session_state["page"]:
        st.session_state["page"] = selected
        st.rerun()
    st.sidebar.markdown("---")
    st.sidebar.caption("企业知识图谱平台 v1.0")
    page = st.session_state["page"]
    if page == "🏠 首页":
        home_page()
    elif page == "📄 文档上传":
        upload_page()
    elif page == "📊 CSV管理":
        csv_page()
    elif page == "💾 导入Neo4j":
        import_page()
    elif page == "🔍 知识检索":
        search_page()
    elif page == "🗺️ 图谱展示":
        graph_page()
    else:
        admin_page()

if __name__ == "__main__":
    main()