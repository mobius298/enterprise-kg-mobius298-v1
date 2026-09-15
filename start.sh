#!/bin/bash

echo "================================================"
echo "   企业知识图谱平台 - 一键启动"
echo "================================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.9+"
    exit 1
fi

# 检查 .env
if [ ! -f ".env" ]; then
    echo "[提示] 未找到 .env 文件，正在从模板创建..."
    cp .env.example .env
    echo "[重要] 请编辑 .env 文件填写配置，然后重新运行"
    exit 1
fi

# 检查依赖
echo "[1/2] 检查并安装依赖..."
python3 -c "import streamlit, pandas, neo4j, networkx, pyvis" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "      首次运行，正在安装依赖..."
    pip3 install -r requirements.txt -q
fi

# 启动
echo "[2/2] 启动应用..."
echo ""
echo "   访问地址: http://localhost:8501"
echo ""

python3 -m streamlit run main.py