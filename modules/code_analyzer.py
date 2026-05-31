import re
import ast
import json
import os
from core.utils import safe_method

LENGUAJES = {
    "python": {
        "ext": [".py", ".pyw", ".pyx"],
        "comentario": "#",
        "bloque": (None, None),
        "shebang": "python",
        "keywords": {"def", "class", "import", "from", "return", "if", "elif", "else",
                     "for", "while", "try", "except", "finally", "with", "as",
                     "async", "await", "yield", "lambda", "pass", "break", "continue",
                     "and", "or", "not", "in", "is", "True", "False", "None", "raise",
                     "global", "nonlocal", "assert", "del", "print"},
        "extiende": False
    },
    "javascript": {
        "ext": [".js", ".mjs", ".cjs"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": "node",
        "keywords": {"function", "const", "let", "var", "return", "if", "else",
                     "for", "while", "do", "switch", "case", "break", "continue",
                     "class", "extends", "new", "this", "super", "typeof",
                     "import", "export", "from", "async", "await", "yield",
                     "try", "catch", "finally", "throw", "null", "undefined",
                     "true", "false", "of", "in", "instanceof", "delete", "void"},
        "extiende": ["typescript", "jsx", "tsx"]
    },
    "typescript": {
        "ext": [".ts", ".tsx"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"interface", "type", "enum", "implements", "abstract",
                     "readonly", "public", "private", "protected", "static",
                     "declare", "namespace", "module", "as", "any", "void",
                     "never", "unknown", "string", "number", "boolean"},
        "extiende": False
    },
    "java": {
        "ext": [".java"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"class", "interface", "extends", "implements", "public",
                     "private", "protected", "static", "final", "abstract",
                     "synchronized", "volatile", "transient", "native",
                     "package", "import", "new", "super", "this", "void",
                     "int", "long", "double", "float", "boolean", "char",
                     "byte", "short", "String", "return", "if", "else",
                     "for", "while", "do", "switch", "case", "break",
                     "continue", "try", "catch", "finally", "throw",
                     "throws", "null", "true", "false", "instanceof"},
        "extiende": False
    },
    "cpp": {
        "ext": [".cpp", ".cc", ".cxx", ".hpp", ".h", ".hh"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"#include", "#define", "#ifdef", "#ifndef", "#endif",
                     "class", "struct", "union", "enum", "template",
                     "typename", "namespace", "using", "virtual", "override",
                     "public", "private", "protected", "const", "constexpr",
                     "static", "extern", "inline", "friend", "auto",
                     "int", "long", "double", "float", "char", "bool",
                     "void", "size_t", "string", "vector", "map",
                     "return", "if", "else", "for", "while", "do",
                     "switch", "case", "break", "continue", "goto",
                     "new", "delete", "try", "catch", "throw",
                     "nullptr", "true", "false", "this"},
        "extiende": False
    },
    "csharp": {
        "ext": [".cs"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"class", "struct", "interface", "enum", "record",
                     "namespace", "using", "public", "private", "protected",
                     "internal", "static", "readonly", "const", "virtual",
                     "override", "abstract", "sealed", "async", "await",
                     "var", "int", "long", "double", "float", "decimal",
                     "bool", "char", "string", "void", "object", "byte",
                     "return", "if", "else", "for", "foreach", "while",
                     "do", "switch", "case", "break", "continue", "goto",
                     "try", "catch", "finally", "throw", "new", "null",
                     "true", "false", "as", "is", "typeof", "sizeof",
                     "get", "set", "value", "this", "base", "partial",
                     "event", "delegate", "lock", "checked", "unchecked"},
        "extiende": False
    },
    "go": {
        "ext": [".go"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"package", "import", "func", "type", "struct",
                     "interface", "map", "chan", "go", "defer", "select",
                     "range", "return", "if", "else", "for", "switch",
                     "case", "default", "break", "continue", "goto",
                     "var", "const", "nil", "true", "false", "int",
                     "int64", "float64", "string", "bool", "byte",
                     "error", "make", "len", "cap", "append", "copy",
                     "close", "delete", "panic", "recover", "fallthrough"},
        "extiende": False
    },
    "rust": {
        "ext": [".rs"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"fn", "let", "mut", "const", "static", "struct",
                     "enum", "impl", "trait", "pub", "use", "mod", "crate",
                     "self", "super", "return", "if", "else", "for",
                     "while", "loop", "match", "break", "continue",
                     "true", "false", "Some", "None", "Ok", "Err",
                     "as", "in", "ref", "move", "unsafe", "async",
                     "await", "dyn", "where", "type", "macro_rules",
                     "i32", "i64", "u32", "u64", "f32", "f64",
                     "bool", "char", "String", "Vec", "Option", "Result",
                     "println", "unwrap", "expect", "clone", "borrow",
                     "Box", "Rc", "Arc", "Cell", "RefCell"},
        "extiende": False
    },
    "ruby": {
        "ext": [".rb"],
        "comentario": "#",
        "bloque": ("=begin", "=end"),
        "shebang": "ruby",
        "keywords": {"def", "class", "module", "end", "return", "if",
                     "elsif", "else", "unless", "case", "when", "for",
                     "while", "until", "do", "yield", "begin", "rescue",
                     "ensure", "raise", "throw", "catch", "nil", "true",
                     "false", "self", "super", "attr_reader", "attr_writer",
                     "attr_accessor", "require", "include", "extend",
                     "load", "private", "public", "protected", "alias",
                     "and", "or", "not", "defined?", "lambda", "proc"},
        "extiende": False
    },
    "php": {
        "ext": [".php"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"<?php", "function", "class", "interface", "trait",
                     "namespace", "use", "require", "include", "return",
                     "if", "else", "elseif", "for", "foreach", "while",
                     "switch", "case", "break", "continue", "try",
                     "catch", "finally", "throw", "new", "public",
                     "private", "protected", "static", "abstract",
                     "final", "const", "var", "null", "true", "false",
                     "this", "self", "parent", "echo", "print",
                     "array", "string", "int", "float", "bool", "void"},
        "extiende": False
    },
    "swift": {
        "ext": [".swift"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"func", "var", "let", "class", "struct", "enum",
                     "protocol", "extension", "return", "if", "else",
                     "for", "while", "switch", "case", "break",
                     "continue", "guard", "defer", "throw", "throws",
                     "rethrows", "try", "catch", "do", "repeat",
                     "inout", "mutating", "nonmutating", "override",
                     "static", "public", "private", "internal",
                     "fileprivate", "open", "required", "convenience",
                     "init", "deinit", "self", "super", "nil",
                     "true", "false", "import", "typealias", "associatedtype",
                     "where", "some", "any"},
        "extiende": False
    },
    "kotlin": {
        "ext": [".kt", ".kts"],
        "comentario": "//",
        "bloque": ("/*", "*/"),
        "shebang": False,
        "keywords": {"fun", "val", "var", "class", "object", "interface",
                     "enum", "data", "sealed", "open", "abstract",
                     "override", "private", "public", "protected",
                     "internal", "companion", "init", "constructor",
                     "return", "if", "else", "when", "for", "while",
                     "do", "try", "catch", "finally", "throw",
                     "null", "true", "false", "this", "super",
                     "import", "package", "as", "in", "is", "!is",
                     "as?", "?:", "!!", "by", "lazy", "lateinit",
                     "suspend", "tailrec", "operator", "infix"},
        "extiende": False
    }
}


class CodeAnalyzer:

    def __init__(self, knowledge_engine=None, ai_manager=None):
        self.knowledge = knowledge_engine
        self.ai = ai_manager
        self._languaje_cache = {}
        print("[CODE] Analizador multilenguaje iniciado.")

    def detectar_lenguaje(self, codigo, archivo=None):
        if archivo:
            ext = os.path.splitext(archivo)[1].lower()
            for lang, info in LENGUAJES.items():
                if ext in info["ext"]:
                    return lang

        codigo_limpio = codigo.strip()
        if not codigo_limpio:
            return "desconocido"

        if codigo_limpio.startswith("#!"):
            shebang = codigo_limpio.split("\n")[0]
            for lang, info in LENGUAJES.items():
                if info["shebang"] and info["shebang"] in shebang:
                    return lang

        if codigo_limpio.startswith("<?php"):
            return "php"

        scores = {}
        for lang, info in LENGUAJES.items():
            score = 0
            keywords = info["keywords"]
            lines = codigo_limpio.split("\n")
            for line in lines[:50]:
                line_strip = line.strip()
                if info["comentario"] and line_strip.startswith(info["comentario"]):
                    score += 0.5
                if info["bloque"][0] and info["bloque"][0] in line_strip:
                    score += 0.5
                tokens = re.findall(r'\b\w+\b', line_strip)
                for token in tokens:
                    if token in keywords:
                        score += 2
                    if token in ("print", "echo", "console", "puts", "System.out"):
                        if lang == "python" and token == "print":
                            score += 3
                        elif lang == "php" and token == "echo":
                            score += 3
                        elif lang == "javascript" and token == "console":
                            score += 3
                        elif lang == "ruby" and token == "puts":
                            score += 3
                        elif lang == "java" and token == "System.out":
                            score += 3

            if lang == "python":
                if re.search(r'^\s*def\s+\w+\s*\(', codigo_limpio, re.MULTILINE):
                    score += 5
                if re.search(r'^\s*class\s+\w+.*:', codigo_limpio, re.MULTILINE):
                    score += 3
                if re.search(r'^\s*import\s+\w+', codigo_limpio, re.MULTILINE):
                    score += 2
                if re.search(r':\s*$', codigo_limpio, re.MULTILINE):
                    score += 1

            elif lang == "javascript":
                if re.search(r'(function|const|let|var)\s+\w+\s*[=\(]', codigo_limpio):
                    score += 5
                if re.search(r'=>\s*{', codigo_limpio):
                    score += 3
                if re.search(r'document\.|window\.|console\.log', codigo_limpio):
                    score += 3
                if re.search(r'module\.exports|export\s+default', codigo_limpio):
                    score += 3

            elif lang == "typescript":
                if re.search(r':\s*(string|number|boolean|void|any)\b', codigo_limpio):
                    score += 5
                if re.search(r'interface\s+\w+|type\s+\w+\s*=', codigo_limpio):
                    score += 5

            elif lang == "java":
                if re.search(r'public\s+(static\s+)?(void|int|String|boolean)\s+\w+\s*\(', codigo_limpio):
                    score += 5
                if re.search(r'System\.(out|in)\.', codigo_limpio):
                    score += 3
                if re.search(r'@Override|@Deprecated|@SuppressWarnings', codigo_limpio):
                    score += 3

            elif lang == "cpp":
                if re.search(r'#include\s*[<"]', codigo_limpio):
                    score += 5
                if re.search(r'std::|cout|cin', codigo_limpio):
                    score += 3
                if re.search(r'int\s+main\s*\(', codigo_limpio):
                    score += 3

            elif lang == "csharp":
                if re.search(r'using\s+System', codigo_limpio):
                    score += 5
                if re.search(r'namespace\s+\w+', codigo_limpio):
                    score += 3
                if re.search(r'Console\.(WriteLine|ReadLine)', codigo_limpio):
                    score += 3

            elif lang == "go":
                if re.search(r'package\s+main', codigo_limpio):
                    score += 5
                if re.search(r'func\s+\w+\s*\(', codigo_limpio):
                    score += 3
                if re.search(r'fmt\.(Print|Scan)', codigo_limpio):
                    score += 3

            elif lang == "rust":
                if re.search(r'fn\s+\w+\s*\(', codigo_limpio):
                    score += 5
                if re.search(r'let\s+mut\s+\w+', codigo_limpio):
                    score += 3
                if re.search(r'println!|format!|vec!', codigo_limpio):
                    score += 3

            elif lang == "ruby":
                if re.search(r'def\s+\w+', codigo_limpio):
                    score += 5
                if re.search(r'puts\s+|print\s+', codigo_limpio):
                    score += 3
                if re.search(r'attr_accessor|attr_reader|attr_writer', codigo_limpio):
                    score += 3

            elif lang == "php":
                if re.search(r'<\?php', codigo_limpio):
                    score += 10
                if re.search(r'\$\w+', codigo_limpio):
                    score += 3
                if re.search(r'function\s+\w+\s*\(', codigo_limpio):
                    score += 2

            elif lang == "swift":
                if re.search(r'import\s+(UIKit|Foundation|SwiftUI)', codigo_limpio):
                    score += 5
                if re.search(r'var\s+\w+:\s*\w+|let\s+\w+:\s*\w+', codigo_limpio):
                    score += 3

            elif lang == "kotlin":
                if re.search(r'fun\s+\w+\s*\(', codigo_limpio):
                    score += 5
                if re.search(r'val\s+\w+|var\s+\w+', codigo_limpio):
                    score += 2
                if re.search(r'package\s+[\w.]+', codigo_limpio):
                    score += 2

            scores[lang] = score

        if not scores:
            return "desconocido"

        best = max(scores, key=scores.get)
        if scores[best] < 3:
            return "desconocido"

        return best

    @safe_method
    def analizar(self, codigo, lenguaje=None):
        if not lenguaje:
            lenguaje = self.detectar_lenguaje(codigo)
        if lenguaje == "desconocido":
            return {"lenguaje": "desconocido", "error": "No se pudo detectar el lenguaje"}

        resultado = {
            "lenguaje": lenguaje,
            "lineas": len(codigo.strip().split("\n")),
            "caracteres": len(codigo),
            "funciones": [],
            "clases": [],
            "imports": [],
            "estructura": []
        }

        if lenguaje == "python":
            try:
                tree = ast.parse(codigo)
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        resultado["funciones"].append({
                            "nombre": node.name,
                            "linea": node.lineno,
                            "args": [arg.arg for arg in node.args.args]
                        })
                    elif isinstance(node, ast.ClassDef):
                        resultado["clases"].append({
                            "nombre": node.name,
                            "linea": node.lineno,
                            "bases": [b.id for b in node.bases if isinstance(b, ast.Name)]
                        })
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                resultado["imports"].append(alias.name)
                        else:
                            resultado["imports"].append(f"{node.module or ''}.{node.names[0].name}")
            except SyntaxError:
                pass

        for lang, info in LENGUAJES.items():
            if lang == lenguaje:
                if info["comentario"]:
                    resultado["comentarios"] = len([
                        l for l in codigo.split("\n")
                        if l.strip().startswith(info["comentario"])
                    ])

        func_patterns = {
            "python": r'^\s*def\s+(\w+)\s*\(([^)]*)\)',
            "javascript": r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\()',
            "typescript": r'(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?\()',
            "java": r'(?:public|private|protected|static|\s)+(\w+(?:\[\])?)\s+(\w+)\s*\(([^)]*)\)',
            "cpp": r'(\w+(?:\s*\*+)?)\s+(\w+)\s*\(([^)]*)\)\s*\{?',
            "csharp": r'(?:public|private|protected|internal|static|\s)+(\w+(?:\[\])?)\s+(\w+)\s*\(([^)]*)\)',
            "go": r'func\s+(\w+)\s*\(([^)]*)\)\s*(\w+)?',
            "rust": r'fn\s+(\w+)\s*\(([^)]*)\)',
            "ruby": r'def\s+(\w+)\s*\(?([^)]*)\)?',
            "php": r'function\s+(\w+)\s*\(([^)]*)\)',
            "swift": r'func\s+(\w+)\s*\(([^)]*)\)',
            "kotlin": r'fun\s+(\w+)\s*\(([^)]*)\)'
        }

        if lenguaje in func_patterns:
            for match in re.finditer(func_patterns[lenguaje], codigo, re.MULTILINE):
                grupos = [g for g in match.groups() if g]
                if grupos:
                    resultado["funciones"].append({
                        "nombre": grupos[0],
                        "linea": codigo[:match.start()].count("\n") + 1
                    })

        class_patterns = {
            "python": r'^\s*class\s+(\w+)',
            "javascript": r'class\s+(\w+)',
            "typescript": r'class\s+(\w+)',
            "java": r'class\s+(\w+)',
            "cpp": r'class\s+(\w+)',
            "csharp": r'class\s+(\w+)',
            "ruby": r'class\s+(\w+)',
            "php": r'class\s+(\w+)',
            "swift": r'class\s+(\w+)',
            "kotlin": r'class\s+(\w+)'
        }

        if lenguaje in class_patterns:
            for match in re.finditer(class_patterns[lenguaje], codigo, re.MULTILINE):
                resultado["clases"].append({
                    "nombre": match.group(1),
                    "linea": codigo[:match.start()].count("\n") + 1
                })

        resultado["total_funciones"] = len(resultado["funciones"])
        resultado["total_clases"] = len(resultado["clases"])
        resultado["total_imports"] = len(resultado["imports"])

        resultado["estructura"] = self._extraer_estructura(codigo, lenguaje)

        return resultado

    def _extraer_estructura(self, codigo, lenguaje):
        estructura = []
        lines = codigo.split("\n")
        indent_actual = 0
        bloque_actual = None

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or stripped.startswith(("#", "//", "/*", "*", "}")):
                continue

            indent = len(line) - len(line.lstrip())
            lang_info = LENGUAJES.get(lenguaje, {})
            comment = lang_info.get("comentario", "")
            if comment and stripped.startswith(comment):
                continue

            if lenguaje == "python":
                if stripped.endswith(":") and not stripped.startswith("#"):
                    estructura.append({
                        "linea": i + 1,
                        "nivel": indent // 4,
                        "tipo": "bloque",
                        "texto": stripped[:80]
                    })
            elif lenguaje in ("javascript", "typescript", "java", "cpp", "csharp", "go", "rust", "kotlin"):
                if "{" in stripped:
                    estructura.append({
                        "linea": i + 1,
                        "nivel": indent // 4,
                        "tipo": "bloque_apertura",
                        "texto": stripped[:80]
                    })

        return estructura[:30]

    @safe_method
    def traducir(self, codigo, origen=None, destino="python", usar_ia=True):
        if not origen:
            origen = self.detectar_lenguaje(codigo)
        if origen == destino:
            return {"ok": True, "codigo": codigo, "mensaje": "Mismo lenguaje"}

        if usar_ia and self.ai:
            prompt = (
                f"Traduce el siguiente codigo de {origen.upper()} a {destino.upper()}. "
                f"Respeta la funcionalidad exacta. Solo devuelve el codigo traducido, sin explicaciones.\n\n"
                f"--- CODIGO {origen.upper()} ---\n{codigo}\n--- FIN ---"
            )
            response = self.ai.ask(prompt)
            response_clean = response.strip()
            if response_clean and not response_clean.startswith(f"[{origen}"):
                return {"ok": True, "codigo": response_clean, "metodo": "ia", "origen": origen, "destino": destino}

        resultado = {"ok": False, "codigo": codigo, "origen": origen, "destino": destino, "metodo": "regex"}
        return resultado

    @safe_method
    def explicar(self, codigo, lenguaje=None, nivel="simple"):
        if not lenguaje:
            lenguaje = self.detectar_lenguaje(codigo)

        analisis = self.analizar(codigo, lenguaje)

        if self.ai:
            niveles = {
                "simple": "Explica este codigo de forma simple, como si fuera para un principiante:",
                "medio": "Explica este codigo en detalle, cubriendo cada funcion y su proposito:",
                "profundo": "Analiza este codigo profundamente: arquitectura, patrones, posibles mejoras y bugs:"
            }
            prompt = f"{niveles.get(nivel, niveles['simple'])}\n\n```{lenguaje}\n{codigo}\n```"
            explicacion = self.ai.ask(prompt)
            if explicacion and not explicacion.startswith(f"[{lenguaje}"):
                return {
                    "lenguaje": lenguaje,
                    "analisis": analisis,
                    "explicacion": explicacion,
                    "nivel": nivel,
                    "metodo": "ia"
                }

        return {
            "lenguaje": lenguaje,
            "analisis": analisis,
            "explicacion": f"Codigo {lenguaje.upper()} con {analisis['lineas']} lineas, "
                           f"{analisis['total_funciones']} funciones, {analisis['total_clases']} clases.",
            "nivel": nivel,
            "metodo": "estatico"
        }

    @safe_method
    def generar_codigo(self, descripcion, lenguaje="python"):
        if self.ai:
            prompt = (
                f"Genera codigo {lenguaje.upper()} para lo siguiente. "
                f"Solo devuelve el codigo, sin explicaciones ni markdown.\n\n"
                f"Descripcion: {descripcion}"
            )
            response = self.ai.ask(prompt)
            if response and not response.startswith(f"[{lenguaje}"):
                codigo_limpio = re.sub(
                    r'^```\w*\n|```$', '',
                    response.strip(),
                    flags=re.MULTILINE
                ).strip()
                lenguaje_detectado = self.detectar_lenguaje(codigo_limpio)
                return {
                    "ok": True,
                    "codigo": codigo_limpio,
                    "lenguaje": lenguaje_detectado,
                    "descripcion": descripcion,
                    "metodo": "ia"
                }

        return {"ok": False, "error": "No hay backend IA disponible para generar codigo"}

    @safe_method
    def indexar_en_conocimiento(self, codigo, lenguaje=None, fuente="manual"):
        if not lenguaje:
            lenguaje = self.detectar_lenguaje(codigo)
        if not self.knowledge:
            return False, "Knowledge engine no disponible"

        analisis = self.analizar(codigo, lenguaje)
        resumen = (
            f"Codigo {lenguaje.upper()}: {analisis['total_funciones']} funciones, "
            f"{analisis['total_clases']} clases, {analisis['lineas']} lineas."
        )

        topic = f"codigo/{lenguaje}"
        self.knowledge.absorb_text(resumen, source=fuente, topic=topic)
        if analisis["funciones"]:
            for fn in analisis["funciones"][:10]:
                self.knowledge.absorb_text(
                    f"Funcion '{fn['nombre']}' en codigo {lenguaje.upper()} (linea {fn.get('linea', '?')})",
                    source=fuente, topic=f"{topic}/funciones"
                )
        if analisis["clases"]:
            for cls in analisis["clases"][:10]:
                self.knowledge.absorb_text(
                    f"Clase '{cls['nombre']}' en codigo {lenguaje.upper()} (linea {cls.get('linea', '?')})",
                    source=fuente, topic=f"{topic}/clases"
                )

        return True, f"Codigo {lenguaje.upper()} indexado en conocimiento"
