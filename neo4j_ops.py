# neo4j_ops.py
from typing import List, Dict
import config
from logger import logger

try:
    from neo4j import GraphDatabase
except ImportError:
    GraphDatabase = None

class Neo4jService:
    def __init__(self):
        if GraphDatabase is None:
            raise ImportError("neo4j driver missing")
        self.uri = config.NEO4J_URI
        self.user = config.NEO4J_USER
        self.password = config.NEO4J_PASSWORD
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
        self.driver.verify_connectivity()
        logger.info("Neo4j connected")
    def close(self):
        if self.driver:
            self.driver.close()
    def reset(self):
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
        logger.info("Database cleared")
        return True
    def run_cql(self, cql: str) -> bool:
        try:
            with self.driver.session() as session:
                session.run(cql)
            return True
        except Exception as e:
            logger.error(f"CQL error: {e}")
            return False
    def get_all(self) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run("MATCH (a)-[r]->(b) RETURN a.name AS entity1, type(r) AS relation, b.name AS entity2")
            return [{"实体1": r["entity1"], "关系": r["relation"], "实体2": r["entity2"]} for r in result]
    def search(self, keyword: str) -> List[Dict]:
        if not keyword.strip():
            return []
        with self.driver.session() as session:
            query = "MATCH (a)-[r]->(b) WHERE a.name CONTAINS $kw OR b.name CONTAINS $kw RETURN a.name AS entity1, type(r) AS relation, b.name AS entity2"
            result = session.run(query, kw=keyword)
            return [{"实体1": r["entity1"], "关系": r["relation"], "实体2": r["entity2"]} for r in result]
    def get_statistics(self) -> Dict:
        with self.driver.session() as session:
            nodes = session.run("MATCH (n) RETURN count(n) AS c").single()["c"]
            rels = session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"]
            return {"nodes": nodes, "relationships": rels}

try:
    kg = Neo4jService()
except Exception as e:
    logger.error(f"Neo4j init failed: {e}")
    kg = None