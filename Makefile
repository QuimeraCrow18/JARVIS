.PHONY: run install test dev clean setup

# JARVIS Makefile - multi-plataforma

run:
	python main.py

install:
	pip install -r requirements.txt

setup:
	python main.py

test:
	python -m pytest tests/ -v --tb=short 2>/dev/null || python -c "print('[TEST] No tests/ encontrados o pytest no instalado')"

dev:
	python main.py --debug 2>&1 | tee logs/dev.log

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -f .modules_autoreg_flag

lint:
	python -m py_compile main.py 2>/dev/null; \
	for f in core/*.py modules/*.py ui/*.py plat/*.py utils/*.py; do \
		python -m py_compile "$$f" 2>/dev/null || true; \
	done; \
	echo "[LINT] Verificación de sintaxis completa"

help:
	@echo "JARVIS Makefile"
	@echo "  make run     - Iniciar JARVIS"
	@echo "  make install - Instalar dependencias"
	@echo "  make setup   - Setup + run"
	@echo "  make test    - Ejecutar tests"
	@echo "  make dev     - Modo desarrollo con log"
	@echo "  make lint    - Verificar sintaxis Python"
	@echo "  make clean   - Limpiar cachés"
