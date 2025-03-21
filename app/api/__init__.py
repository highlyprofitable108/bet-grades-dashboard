"""API package for API endpoints."""

from flask import Blueprint

bp = Blueprint('api', __name__, url_prefix='/api')

from app.api import api_routes
