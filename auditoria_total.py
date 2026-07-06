import os

def generar_auditoria():
    nombre_archivo = "estructura_josamic.txt"
    print(f"Generando auditoría en {nombre_archivo}...")
    
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("--- ESTRUCTURA DE JOSAMIC CORE AI ---\n")
        f.write(f"Ruta raíz: {os.getcwd()}\n")
        f.write("-" * 50 + "\n")
        
        # os.walk recorre desde la raíz hacia abajo
        for raiz, carpetas, archivos in os.walk('.'):
            # Ignoramos carpetas de sistema
            if '.git' in carpetas: carpetas.remove('.git')
            if '__pycache__' in carpetas: carpetas.remove('__pycache__')
            
            for archivo in archivos:
                # Omitimos los archivos de este script y el reporte resultante
                if archivo in ['auditoria_total.py', 'estructura_josamic.txt']:
                    continue
                
                ruta_completa = os.path.join(raiz, archivo)
                f.write(f"{ruta_completa}\n")
                
        f.write("-" * 50 + "\n")
        f.write("--- AUDITORÍA FINALIZADA ---\n")
        
    print(f"¡Listo! Ya puedes abrir el archivo '{nombre_archivo}' con el Bloc de Notas.")

if __name__ == "__main__":
    generar_auditoria()