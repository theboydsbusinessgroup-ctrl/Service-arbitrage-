"""Compatibility entrypoint shared by local and hosted deployments."""
from app.main import app

__all__ = ['app']
