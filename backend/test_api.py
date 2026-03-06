"""Unit tests for Futures-War API"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

from main import app

client = TestClient(app)


def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


def test_moderation_safe_content():
    """Test moderation with safe content"""
    response = client.post("/moderate?text=I%20love%20Marseille")
    assert response.status_code == 200
    data = response.json()
    assert data["is_safe"] == True


def test_moderation_unsafe_content():
    """Test moderation with unsafe content"""
    response = client.post("/moderate?text=We%20need%20to%20kill%20tuer%20this")
    assert response.status_code == 200
    data = response.json()
    assert data["is_safe"] == False


def test_enrichment():
    """Test prompt enrichment"""
    response = client.post("/enrich?text=futuristic%20city&style=cyberpunk")
    assert response.status_code == 200
    data = response.json()
    assert "enriched" in data
    assert isinstance(data["enriched"], str)
    assert len(data["enriched"]) > 0


def test_generate_image():
    """Test image generation endpoint"""
    response = client.post("/generate", json={
        "prompt": "neon cyberpunk Marseille",
        "style": "futuristic"
    })
    assert response.status_code == 200
    data = response.json()
    assert "images" in data or "image_url" in data
