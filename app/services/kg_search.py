import json
import os
from collections import defaultdict
import dotenv
dotenv.load_dotenv()

class KnowledgeGraphService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.nodes = {}
        self.relationships = defaultdict(list)
        self._load_data()

    def _load_data(self):
        if not os.path.exists(self.db_path):
            raise FileNotFoundError(f"KG DB not found: {self.db_path}")

        with open(self.db_path, "r", encoding="utf-8") as f:
            raw_data = json.load(f)

        # Load nodes
        for node in raw_data.get("nodes", [])[:]:
            self.nodes[node["id"]] = node
        # print(f"✅ Loaded {len(self.nodes)} nodes.")

        # Load relationships
        for rel in raw_data.get("relationships", [])[:]:
            self.relationships[rel["source"]].append(rel)
        # print(f"✅ Loaded {sum(len(v) for v in self.relationships.values())} relationships.")

    async def search(self, entity: str):
        """
        Tìm node có tên khớp với entity
        và trả về node + tất cả neighbors của nó
        """
        # Chia nhỏ query thành các từ
        entities = entity.lower()
        results = []

        # tìm node theo tên (case-insensitive)
        matched_nodes = []
        # print(f"Searching for entity: {self.nodes}")
        for node_name, node_values in self.nodes.items():
            node_name = node_name.lower()
            # print(f"Checking node: {node_name}")
            if (node_name in  entities):
                matched_nodes.append(node_values)
        if not matched_nodes:
            return []
        # print(f"🔍 Found {len(matched_nodes)} matched nodes for entity '{entity}'.")

        for node in matched_nodes:
            node_id = node
            # print(f"Processing node: {node_id}")

            # lấy tất cả quan hệ đi từ node này
            rels = self.relationships.get(node_id['id'], [])
            # print(f"  - Found {len(rels)} relationships.")
            neighbors = []
            for rel in rels:
                target_id = rel["target"]
                target_node = self.nodes.get(target_id)
                if target_node:
                    neighbors.append({
                        "relationship": rel.get("type"),
                        "target": target_node
                    })

            results.append({
                "node": node,
                "neighbors": neighbors
            })

        return results

if __name__ == "__main__":
    import asyncio
    kg_db = os.getenv("KG_DB_PATH", "data/kg_db.json")
    kg = KnowledgeGraphService(kg_db)

    query = "bệnh addison nguyên nhân".lower()
    results =asyncio.run(kg.search(query))

    for r in results:
        if not r['neighbors']:
            continue
        print(f"\n🎯 Node: {r['node']}")
        for n in r["neighbors"]:
            if n['target'] and n['relationship']:
                print(f"  ➡ {n['relationship']} → {n['target']}")
