from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from banco import get_db
from extensoes import bcrypt

public_bp = Blueprint('public', __name__, url_prefix='/public')

@public_bp.route("/")
def index():
    return render_template("index.html")

@public_bp.get("/cadastro")
def exibir_cadastro():
    return render_template("cadastro.html")

@public_bp.post("/cadastro")
def cadastro():
    conn = None
    cursor = None
    try:
            
        nome = request.form.get("nome").strip()
        cpf = request.form.get("cpf").strip()
        email = request.form.get("email").strip()
        senha = request.form.get["senha",""]

        conn = get_db()
        cursor = conn.cursor()

    
