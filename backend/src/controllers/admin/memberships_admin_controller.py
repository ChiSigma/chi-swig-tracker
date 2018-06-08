from flask import Blueprint, request, g
from flask_orator import jsonify
from src.models import PrimaryMembership, EphemeralMembership

memberships_admin = Blueprint('memberships_admin', __name__)