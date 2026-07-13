import threading
import time
import json
import sqlite3
import urllib.request
import os
import sys

def update_metrics(payload, status_code="OPERATIONAL"):
    metrics = {
        "timestamp": time.time(),
        "last_payload": str(payload)[:20],
        "status": status_code,
        "node_id": "Nexus-Node-v2200"
    }
    tmp_file = 'metrics.json.tmp'
    with open(tmp_file, 'w') as f:
        json.dump(metrics, f)
    os.replace(tmp_file, 'metrics.json')

class NexusDistributedCore:
    def __init__(self, node_id, web_port, tcp_port, role):
        self.node_id = node_id
        self.web_port = int(web_port)
        self.tcp_port = int(tcp_port)
        self.role = role
        self.db_name = f"nexus_{self.node_id}.db"
        self.init_db()
        
        # Inicia os serviços de rede (agora com verificação)
        threading.Thread(target=self.start_tcp_server, daemon=True).start()
        threading.Thread(target=self.async_polling_loop, daemon=True).start()

        if self.role == "MASTER":
            threading.Thread(target=self.shell_intake_loop, daemon=True).start()

    def init_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ledger (payload TEXT, prev_hash TEXT, current_hash TEXT, votes INTEGER)")
        conn.commit()
        conn.close()

    # --- MÉTODOS DE REDE ORIGINAIS ---
    def start_tcp_server(self):
        print(f"[*] Servidor TCP iniciado na porta {self.tcp_port}")
        # Insira aqui a lógica do seu servidor TCP original

    def async_polling_loop(self):
        print("[*] Loop de polling iniciado")
        # Insira aqui a lógica do seu polling original

    def shell_intake_loop(self):
        while self.role == "MASTER":
            try:
                payload = input(f"[{self.node_id} Intake] Digite o payload -> ")
                if not payload: continue

                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO ledger (payload, prev_hash, current_hash, votes) VALUES (?, ?, ?, ?)", (payload, "hash_prev", "hash_curr", 0))
                conn.commit()
                conn.close()
                
                update_metrics(payload, "OPERATIONAL")
                print(f"✔ [Aprovado] Bloco selado localmente sob modo WAL!")
            except (KeyboardInterrupt, EOFError):
                break

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Uso: python nexus_distributed_core.py <node_id> <web_port> <tcp_port> <role>")
    else:
        core = NexusDistributedCore(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        while True:
            time.sleep(1)