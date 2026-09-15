# 🏢 企业知识图谱平台

基于 **大语言模型（LLM）** 和 **Neo4j 图数据库** 的智能知识图谱构建与应用平台。

从非结构化文档中自动抽取实体关系三元组，构建可视化知识网络，支持关键词检索与图谱探索。

## ✨ 功能特性

- 📄 **多格式文档解析**：支持 TXT、PDF、DOCX
- 🤖 **AI 知识抽取**：基于通义千问自动抽取（实体1, 关系, 实体2）
- 📊 **CSV 中间层**：数据审查、备份、编辑，生成 Neo4j 导入脚本
- 💾 **Neo4j 存储**：幂等写入，支持增量更新
- 🗺️ **交互式可视化**：PyVis 动态图谱，支持拖拽/缩放/高亮
- 🔍 **关键词检索**：参数化查询，安全高效
- ⚡ **缓存机制**：数据哈希比对，避免重复渲染

## ⚡ 三种启动方式

**方式一：Windows 一键启动** → 双击 `start.bat`

**方式二：Docker 一键部署** → `docker-compose up -d`

**方式三：手动安装** → 见下方详细步骤

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/你的用户名/enterprise-kg.git
cd enterprise-kg
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env      # Linux/Mac
copy .env.example .env    # Windows
```

编辑 `.env`，填入你的配置。**没有 API Key 也能用**：设置 `USE_MOCK_LLM=true`。

### 4. 启动 Neo4j（可选）

```bash
docker run -d --name neo4j -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:5.26
```

访问 `http://localhost:7474` 完成初始密码设置。

### 5. 运行应用

```bash
streamlit run main.py
```

浏览器打开 `http://localhost:8501`。

## 📖 使用流程

```
上传文档 → 解析文本 → AI抽取三元组 → 保存CSV
    → 生成CQL脚本 → 导入Neo4j → 图谱可视化/知识检索
```

## 🏗️ 项目结构

```
enterprise-kg/
├── main.py              # 应用入口
├── pages.py             # 各功能页面
├── config.py            # 配置中心
├── logger.py            # 日志系统
├── file_parser.py       # 文件解析
├── nlp_processor.py     # LLM 知识抽取
├── csv_manager.py       # CSV 管理与 CQL 生成
├── neo4j_ops.py         # Neo4j 服务封装
├── visualizer.py        # 交互式可视化
├── requirements.txt
├── .env.example
└── .gitignore
```

## 🛠️ 技术栈

| 层次 | 技术 |
|------|------|
| 前端 | Streamlit |
| 图数据库 | Neo4j 5.x |
| 大语言模型 | 通义千问 (DashScope) |
| LLM 编排 | LangChain |
| 可视化 | NetworkX + PyVis |
| 文档解析 | PyPDF2, python-docx |

## 📝 License

MIT License