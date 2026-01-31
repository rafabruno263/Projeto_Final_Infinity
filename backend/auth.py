from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "troque_essa_chave_em_producao"

def create_token(user_id: int, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=8)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

def get_bearer_token():
    auth = request.headers.get("Authorization", "")
    if auth.startswith("Bearer "):
        return auth.split(" ", 1)[1].strip()
    return None

def require_auth(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        token = get_bearer_token()
        if not token:
            return jsonify({"error": "Não autenticado"}), 401
        try:
            payload = decode_token(token)
        except Exception:
            return jsonify({"error": "Token inválido ou expirado"}), 401

        request.user = {"id": int(payload["sub"]), "role": payload["role"]}
        return fn(*args, **kwargs)
    return wrapper

def require_role(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = get_bearer_token()
            if not token:
                return jsonify({"error": "Não autenticado"}), 401
            try:
                payload = decode_token(token)
            except Exception:
                return jsonify({"error": "Token inválido ou expirado"}), 401

            role = payload.get("role")
            if role not in roles:
                return jsonify({"error": "Acesso negado"}), 403

            request.user = {"id": int(payload["sub"]), "role": role}
            return fn(*args, **kwargs)
        return wrapper
    return decorator