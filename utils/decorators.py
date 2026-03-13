# utils/decorators.py (versión optimizada)
from functools import wraps
from flask import session, redirect, url_for, flash, request

# -------------------------
# Login requerido
# -------------------------
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("⚠️ Debes iniciar sesión primero.", "warning")
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------
# Solo administrador
# -------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("rol") != "ADMIN":
            flash("🚫 No tienes permisos para acceder a esta sección.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

# -------------------------
# Solo director
# -------------------------
def director_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("rol") != "DIRECTOR":
            flash("🚫 Acceso restringido solo para director.", "error")
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

