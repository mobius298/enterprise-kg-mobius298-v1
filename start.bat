@echo off
chcp 65001 >nul
title 企业知识图谱平台 - 启动器
color 0A

echo ================================================
echo    企业知识图谱平台 - 一键启动
echo ================================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python，请先安装 Python 3.9 或更高版本
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查 .env 文件
if not exist ".env" (
    echo [提示] 未找到 .env 文件，正在从模板创建...
    copy ".env.example" ".env" >nul
    echo.
    echo [重要] 请编辑 .env 文件，填写 Neo4j 密码和 API Key
    echo        如果暂时没有，可以直接按回车跳过，使用默认模拟模式
    echo.
    pause
)

REM 检查依赖
echo [1/2] 检查并安装依赖...
python -c "import streamlit, pandas, neo4j, networkx, pyvis" >nul 2>&1
if errorlevel 1 (
    echo       首次运行，正在安装依赖，请稍候（约 1-2 分钟）...
    python -m pip install -r requirements.txt -q
    if errorlevel 1 (
        echo [警告] 依赖安装失败，尝试使用清华镜像...
        python -m pip install -r requirements.txt -q -i https://pypi.tuna.tsinghua.edu.cn/simple
    )
) else (
    echo       依赖已安装，跳过
)

REM 启动
echo [2/2] 启动应用...
echo.
echo ================================================
echo    应用即将启动，浏览器将自动打开
echo    如果未自动打开，请手动访问: http://localhost:8501
echo    按 Ctrl+C 可停止应用
echo ================================================
echo.

python -m streamlit run main.py

pause