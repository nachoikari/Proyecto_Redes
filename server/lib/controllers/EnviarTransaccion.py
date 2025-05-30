from flask import Blueprint, request, jsonify
import mysql.connector
from lib.config.db_config import db_config  

login_bp = Blueprint('enviarSinpe', __name__)

@app.route