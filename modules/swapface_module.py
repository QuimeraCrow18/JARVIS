# ==========================================
# SWAP FACE MODULE
# modules/swapface_module.py
# ==========================================

import cv2
import mediapipe as mp
import numpy as np

from core.utils import safe_method

class SwapFaceModule:
    def __init__(self):
        print("[SWAPFACE] Módulo de intercambio de rostros iniciado.")
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=2)
        self.drawing_utils = mp.solutions.drawing_utils

    @safe_method
    def detect_faces(self, image):
        """
        Detecta hasta dos rostros en una imagen.
        Retorna una lista de landmarks por cara.
        """
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = self.face_mesh.process(rgb)
        if not result.multi_face_landmarks:
            print("[SWAPFACE] No se detectaron rostros.")
            return []
        return result.multi_face_landmarks

    @safe_method
    def extract_face(self, image, landmarks):
        """
        Extrae la región del rostro basada en los landmarks de mediapipe.
        """
        # Ejemplo: solo recorta un rectángulo basándonos en los landmarks extremos
        h, w, _ = image.shape
        xs = [int(point.x * w) for point in landmarks.landmark]
        ys = [int(point.y * h) for point in landmarks.landmark]
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        face_roi = image[y_min:y_max, x_min:x_max]
        return face_roi

    @safe_method
    def swap_faces(self, image_path1, image_path2, output_path="swapface_output.jpg"):
        """
        Carga dos imágenes, detecta rostros, e intenta intercambiarlos.
        (Versión simple: recorte e intercambio sin morphing avanzado)
        """
        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)

        faces1 = self.detect_faces(img1)
        faces2 = self.detect_faces(img2)
        if not faces1 or not faces2:
            print("[SWAPFACE] Debe haber al menos un rostro en ambas imágenes.")
            return False

        # Solo el primer rostro
        face1 = self.extract_face(img1, faces1[0])
        face2 = self.extract_face(img2, faces2[0])

        # Redimensionar face1 al área del rostro de img2
        face1_resized = cv2.resize(face1, (face2.shape[1], face2.shape[0]))
        face2_resized = cv2.resize(face2, (face1.shape[1], face1.shape[0]))

        # Insertar el rostro 1 en la imagen 2 (posición aproximada)
        img2_result = img2.copy()
        h, w = face2.shape[:2]
        img2_result[0:h, 0:w] = face1_resized

        # Insertar el rostro 2 en la imagen 1 (posición aproximada)
        img1_result = img1.copy()
        h, w = face1.shape[:2]
        img1_result[0:h, 0:w] = face2_resized

        # Por simplicidad, guardamos solo uno
        cv2.imwrite(output_path, img2_result)
        print(f"[SWAPFACE] Intercambio simple realizado. Resultado guardado en {output_path}")
        return True

    # Puedes expandir este método usando deepface, dlib o imanip con morphing avanzado y blending si deseas mayor realismo.