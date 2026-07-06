"""Test script for Event Bus - Phase 1 validation."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.event_bus import EventBus, get_event_bus, publish_event, subscribe_event, request_response


def test_pubsub():
    """Test basic pub/sub functionality."""
    print("=== Test 1: Pub/Sub ===")
    bus = EventBus()
    
    received = []
    
    def callback(event):
        received.append(event)
        print(f"  Recibido: {event['type']} - {event['data']}")
    
    sub_id = bus.subscribe("test.event", callback)
    print(f"  Suscrito con ID: {sub_id}")
    
    bus.publish("test.event", {"message": "Hola Mundo"}, "test_source")
    
    assert len(received) == 1
    assert received[0]["data"]["message"] == "Hola Mundo"
    assert received[0]["source"] == "test_source"
    print("  [OK] Pub/Sub funciona correctamente")
    
    bus.unsubscribe("test.event", sub_id)
    bus.publish("test.event", {"message": "No deberia llegar"}, "test_source")
    assert len(received) == 1
    print("  [OK] Unsubscribe funciona correctamente")
    print()


def test_request_response():
    """Test request/response functionality."""
    print("=== Test 2: Request/Response ===")
    bus = EventBus()
    
    def handler(request):
        return {
            "status": "success",
            "result": f"Procesado: {request['payload'].get('input', 'vacio')}"
        }
    
    bus.register_handler("test.request", handler)
    print("  Handler registrado")
    
    response = bus.request("test.request", {"input": "datos de prueba"}, "test_client")
    print(f"  Respuesta: {response}")
    
    assert response["status"] == "success"
    assert "Procesado" in response["result"]
    print("  [OK] Request/Response funciona correctamente")
    
    # Test non-existent handler
    response = bus.request("inexistente", {}, "test_client")
    assert response["status"] == "not_found"
    print("  [OK] Manejo de handler inexistente funciona")
    print()


def test_global_instance():
    """Test global convenience functions."""
    print("=== Test 3: Funciones Globales ===")
    
    received = []
    
    def global_callback(event):
        received.append(event)
    
    sub_id = subscribe_event("global.test", global_callback)
    publish_event("global.test", {"global": True}, "global_test")
    
    assert len(received) == 1
    assert received[0]["data"]["global"] is True
    print("  [OK] Funciones globales funcionan correctamente")
    print()


def test_history():
    """Test event history."""
    print("=== Test 4: Historial ===")
    bus = EventBus()
    
    bus.publish("history.test", {"num": 1}, "test")
    bus.publish("history.test", {"num": 2}, "test")
    bus.publish("other.event", {"num": 3}, "test")
    
    history = bus.get_history("history.test", limit=10)
    assert len(history) == 2
    assert history[0]["data"]["num"] == 1
    assert history[1]["data"]["num"] == 2
    print("  [OK] Historial funciona correctamente")
    print()


def test_multiple_subscribers():
    """Test multiple subscribers for same event."""
    print("=== Test 5: Múltiples Suscriptores ===")
    bus = EventBus()
    
    results = []
    
    def make_callback(name):
        def cb(event):
            results.append(name)
        return cb
    
    bus.subscribe("multi.test", make_callback("sub1"))
    bus.subscribe("multi.test", make_callback("sub2"))
    bus.subscribe("multi.test", make_callback("sub3"))
    
    bus.publish("multi.test", {"data": "test"}, "test")
    
    assert len(results) == 3
    assert "sub1" in results and "sub2" in results and "sub3" in results
    print("  [OK] Múltiples suscriptores notificados correctamente")
    print()


if __name__ == "__main__":
    print("Iniciando pruebas del Event Bus (FASE 1)...\n")
    
    test_pubsub()
    test_request_response()
    test_global_instance()
    test_history()
    test_multiple_subscribers()
    
    print("=" * 40)
    print("[OK] TODAS LAS PRUEBAS PASARON - FASE 1 VALIDADA")
    print("=" * 40)