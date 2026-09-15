# csv_manager.py
import os
import pandas as pd
import config
from logger import logger

def save_to_csv(triples):
    if not triples:
        return 0
    df = pd.DataFrame(triples, columns=["实体1", "关系", "实体2"])
    df.to_csv(config.CSV_FILE, index=False, encoding="utf-8-sig")
    logger.info(f"Saved {len(df)} triples")
    return len(df)

def load_from_csv():
    if not os.path.exists(config.CSV_FILE):
        return []
    df = pd.read_csv(config.CSV_FILE, encoding="utf-8-sig")
    if not all(c in df.columns for c in ["实体1", "关系", "实体2"]):
        return []
    return df[["实体1", "关系", "实体2"]].values.tolist()

def show_csv():
    if not os.path.exists(config.CSV_FILE):
        return None
    return pd.read_csv(config.CSV_FILE, encoding="utf-8-sig")

def clear_csv():
    if os.path.exists(config.CSV_FILE):
        os.remove(config.CSV_FILE)
        logger.info("CSV cleared")
        return True
    return False

def _escape_cypher_string(s):
    s = str(s)
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    return s

def _sanitize_rel_type(rel):
    rel = str(rel).strip()
    if not rel:
        return "关联"
    rel = rel.replace(" ", "_")
    filtered = []
    for c in rel:
        if c.isalnum() or c == "_" or "\u4e00" <= c <= "\u9fff":
            filtered.append(c)
    rel = "".join(filtered)
    if not rel:
        return "关联"
    has_chinese = any("\u4e00" <= c <= "\u9fff" for c in rel)
    if has_chinese or not rel.isidentifier():
        rel = f"`{rel}`"
    return rel

def generate_neo4j_import_cql():
    triples = load_from_csv()
    if not triples:
        return ""
    lines = []
    for e1, rel, e2 in triples:
        e1 = _escape_cypher_string(e1)
        e2 = _escape_cypher_string(e2)
        rel = _sanitize_rel_type(rel)
        cql = f'MERGE (a:Entity {{name:"{e1}"}}) MERGE (b:Entity {{name:"{e2}"}}) MERGE (a)-[:{rel}]->(b);'
        lines.append(cql)
    with open(config.IMPORT_CQL, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    logger.info(f"Generated {len(lines)} CQL statements")
    return "\n".join(lines)