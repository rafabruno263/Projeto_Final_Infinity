from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

from db import init_db, get_conn, now_iso, log_activity
from auth import create_token, require_auth, require_role

app = Flask(__name__)
CORS(app)

@app.get("/health")
def health():
    return {"status": "ok"}

def seed_if_empty():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM users")
    count = cur.fetchone()["c"]

    if count == 0:
        users = [
            ("Funcionario", "funcionario@wayne.com", generate_password_hash("1234"), "employee"),
            ("Gerente", "gerente@wayne.com", generate_password_hash("1234"), "manager"),
            ("Admin Seguranca", "admin@wayne.com", generate_password_hash("1234"), "security_admin"),
        ]
        cur.executemany("INSERT INTO users (nome,email,senha_hash,role) VALUES (?,?,?,?)", users)

        resources = [
            ("equipment", "Servidor Central", "Rack 3 - Sala TI", "ativo", now_iso()),
            ("vehicle", "Batmóvel (Protótipo)", "Garagem - Setor P&D", "em_manutencao", now_iso()),
            ("security_device", "Câmera Corredor A", "Andar 2", "ativo", now_iso()),
        ]
        cur.executemany(
            "INSERT INTO resources (tipo,nome,descricao,status,atualizado_em) VALUES (?,?,?,?,?)",
            resources
        )

    conn.commit()
    conn.close()

@app.post("/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    senha = data.get("senha") or ""

    if not email or not senha:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    conn.close()

    if not user or not check_password_hash(user["senha_hash"], senha):
        return jsonify({"error": "Credenciais inválidas"}), 401

    token = create_token(user["id"], user["role"])
    log_activity(user["id"], "LOGIN", "USER", user["id"])
    return jsonify({
        "token": token,
        "user": {"id": user["id"], "nome": user["nome"], "email": user["email"], "role": user["role"]}
    })

@app.get("/auth/me")
@require_auth
def me():
    uid = request.user["id"]
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,nome,email,role FROM users WHERE id = ?", (uid,))
    user = cur.fetchone()
    conn.close()
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404
    return jsonify(dict(user))

@app.get("/users")
@require_role("security_admin")
def list_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id,nome,email,role FROM users ORDER BY id DESC")
    users = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(users)

@app.post("/users")
@require_role("security_admin")
def create_user():
    data = request.get_json(silent=True) or {}
    nome = (data.get("nome") or "").strip()
    email = (data.get("email") or "").strip().lower()
    senha = data.get("senha") or ""
    role = data.get("role") or ""

    if not nome or not email or not senha or role not in ("employee", "manager", "security_admin"):
        return jsonify({"error": "Dados inválidos"}), 400

    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (nome,email,senha_hash,role) VALUES (?,?,?,?)",
            (nome, email, generate_password_hash(senha), role)
        )
        new_id = cur.lastrowid
        conn.commit()
    except Exception:
        conn.close()
        return jsonify({"error": "Email já existe"}), 409
    conn.close()

    log_activity(request.user["id"], "CREATE_USER", "USER", new_id)
    return jsonify({"id": new_id}), 201

@app.get("/resources")
@require_auth
def list_resources():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM resources ORDER BY id DESC")
    items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return jsonify(items)

@app.post("/resources")
@require_role("security_admin")
def create_resource():
    data = request.get_json(silent=True) or {}
    tipo = data.get("tipo")
    nome = (data.get("nome") or "").strip()
    descricao = (data.get("descricao") or "").strip()
    status = (data.get("status") or "").strip()

    if tipo not in ("equipment", "vehicle", "security_device") or not nome or not status:
        return jsonify({"error": "Dados inválidos"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO resources (tipo,nome,descricao,status,atualizado_em) VALUES (?,?,?,?,?)",
        (tipo, nome, descricao, status, now_iso())
    )
    rid = cur.lastrowid
    conn.commit()
    conn.close()

    log_activity(request.user["id"], "CREATE_RESOURCE", "RESOURCE", rid)
    return jsonify({"id": rid}), 201

@app.put("/resources/<int:rid>")
@require_role("security_admin")
def update_resource(rid: int):
    data = request.get_json(silent=True) or {}
    tipo = data.get("tipo")
    nome = (data.get("nome") or "").strip()
    descricao = (data.get("descricao") or "").strip()
    status = (data.get("status") or "").strip()

    if tipo not in ("equipment", "vehicle", "security_device") or not nome or not status:
        return jsonify({"error": "Dados inválidos"}), 400

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM resources WHERE id = ?", (rid,))
    exists = cur.fetchone()
    if not exists:
        conn.close()
        return jsonify({"error": "Recurso não encontrado"}), 404

    cur.execute(
        "UPDATE resources SET tipo=?, nome=?, descricao=?, status=?, atualizado_em=? WHERE id=?",
        (tipo, nome, descricao, status, now_iso(), rid)
    )
    conn.commit()
    conn.close()

    log_activity(request.user["id"], "UPDATE_RESOURCE", "RESOURCE", rid)
    return jsonify({"ok": True})

@app.delete("/resources/<int:rid>")
@require_role("security_admin")
def delete_resource(rid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id FROM resources WHERE id = ?", (rid,))
    exists = cur.fetchone()
    if not exists:
        conn.close()
        return jsonify({"error": "Recurso não encontrado"}), 404

    cur.execute("DELETE FROM resources WHERE id = ?", (rid,))
    conn.commit()
    conn.close()

    log_activity(request.user["id"], "DELETE_RESOURCE", "RESOURCE", rid)
    return jsonify({"ok": True})

@app.get("/dashboard/summary")
@require_auth
def dashboard_summary():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as total FROM resources")
    total = cur.fetchone()["total"]

    cur.execute("""
      SELECT tipo, COUNT(*) as qtd
      FROM resources
      GROUP BY tipo
    """)
    by_type = {row["tipo"]: row["qtd"] for row in cur.fetchall()}

    cur.execute("""
      SELECT al.id, al.acao, al.entidade, al.entidade_id, al.data_hora, u.nome as usuario
      FROM activity_logs al
      JOIN users u ON u.id = al.user_id
      ORDER BY al.id DESC
      LIMIT 10
    """)
    recent = [dict(r) for r in cur.fetchall()]

    conn.close()
    return jsonify({
        "resources_total": total,
        "resources_by_type": by_type,
        "recent_activity": recent
    })

if __name__ == "__main__":
    init_db()
    seed_if_empty()
    app.run(host="127.0.0.1", port=5000, debug=True)