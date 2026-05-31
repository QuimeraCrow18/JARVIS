import os
import json
from datetime import datetime

from core.utils import safe_method


class LearningModule:

    def __init__(self):

        self.data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data"
        )
        os.makedirs(self.data_dir, exist_ok=True)

        self.memory_file = os.path.join(self.data_dir, "memory.json")
        self.max_conversations = 100

        self._memory = self._load()
        self._ensure_structure()

        print("[LEARN] Módulo de aprendizaje iniciado.")

    def _ensure_structure(self):

        if "facts" not in self._memory:
            self._memory["facts"] = {}
        if "preferences" not in self._memory:
            self._memory["preferences"] = {}
        if "conversations" not in self._memory:
            self._memory["conversations"] = []

    def _load(self):

        if not os.path.exists(self.memory_file):
            return {"facts": {}, "preferences": {}, "conversations": []}
        try:
            with open(self.memory_file, "r", encoding="utf-8") as f:
                content = f.read()
                if not content.strip():
                    return {"facts": {}, "preferences": {}, "conversations": []}
                return json.loads(content)
        except (json.JSONDecodeError, IOError):
            return {"facts": {}, "preferences": {}, "conversations": []}

    def _save(self):

        with open(self.memory_file, "w", encoding="utf-8") as f:
            json.dump(self._memory, f, indent=2, ensure_ascii=False)

    @safe_method
    def learn_fact(self, key, value):

        self._memory["facts"][key.lower()] = {
            "value": value,
            "learned_at": datetime.now().isoformat()
        }
        self._save()
        print(f"[LEARN] Aprendido: {key} = {value}")
        return True

    @safe_method
    def recall_fact(self, key):

        data = self._memory["facts"].get(key.lower())
        if data:
            print(f"[LEARN] Recuerdo: {key} = {data['value']}")
            return data["value"]
        print(f"[LEARN] No sé nada sobre '{key}'")
        return None

    @safe_method
    def forget_fact(self, key):

        if key.lower() in self._memory["facts"]:
            del self._memory["facts"][key.lower()]
            self._save()
            print(f"[LEARN] Olvidado: {key}")
            return True
        print(f"[LEARN] No tenía información sobre '{key}'")
        return False

    @safe_method
    def list_all_facts(self):

        facts = self._memory["facts"]
        if not facts:
            print("[LEARN] No tengo conocimientos almacenados aún.")
            return []
        print(f"[LEARN] Conocimientos almacenados ({len(facts)}):")
        for key, data in sorted(facts.items()):
            print(f"  - {key}: {data['value']}")
        return facts

    @safe_method
    def set_preference(self, pref_key, pref_value):

        self._memory["preferences"][pref_key.lower()] = pref_value
        self._save()
        print(f"[LEARN] Preferencia guardada: {pref_key} = {pref_value}")
        return True

    @safe_method
    def get_preference(self, pref_key):

        return self._memory["preferences"].get(pref_key.lower())

    @safe_method
    def record_conversation(self, user_input, response):

        conversations = self._memory["conversations"]
        conversations.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input,
            "jarvis": response
        })
        if len(conversations) > self.max_conversations:
            self._memory["conversations"] = conversations[-self.max_conversations:]
        self._save()

    @safe_method
    def get_recent_conversations(self, limit=5):

        convos = self._memory["conversations"][-limit:]
        if not convos:
            print("[LEARN] No hay conversaciones registradas.")
            return []
        print(f"[LEARN] Últimas {len(convos)} interacciones:")
        for c in convos:
            ts = c.get("timestamp", "")[11:19]
            print(f"  [{ts}] Tú: {c['user']}")
            print(f"  [{ts}] JARVIS: {c['jarvis']}")
        return convos

    @safe_method
    def search_memory(self, query):

        query = query.lower()
        results = []
        for key, data in self._memory["facts"].items():
            if query in key.lower() or query in data["value"].lower():
                results.append({"key": key, "value": data["value"]})
        return results

    @safe_method
    def get_stats(self):

        return {
            "facts": len(self._memory["facts"]),
            "preferences": len(self._memory["preferences"]),
            "conversations": len(self._memory["conversations"])
        }
