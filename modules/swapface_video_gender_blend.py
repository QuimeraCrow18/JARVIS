# ==========================================
# SWAP FACE VIDEO (MULTI-GÉNERO, BLENDING AVANZADO)
# modules/swapface_video_gender_blend.py
# ==========================================

import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
from core.utils import safe_method
import random

class SwapFaceVideoGenderBlendModule:
    def __init__(self):
        print("[SWAPFACE-VIDEO] Multi rostro, género y blending avanzado")
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, max_num_faces=15)
        self.drawing_utils = mp.solutions.drawing_utils
        self.hombres_faces = []
        self.mujeres_faces = []

    @safe_method
    def detect_faces(self, image):
        """Detecta rostros en imagen"""
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)
        return results.multi_face_landmarks if results.multi_face_landmarks else []

    @safe_method
    def extract_face(self, image, landmarks):
        """Extrae región de rostro"""
        h, w, _ = image.shape
        xs = [int(point.x * w) for point in landmarks.landmark]
        ys = [int(point.y * h) for point in landmarks.landmark]
        x_min, x_max = max(min(xs), 0), min(max(xs), w-1)
        y_min, y_max = max(min(ys), 0), min(max(ys), h-1)
        face_roi = image[y_min:y_max, x_min:x_max]
        center = ((x_min + x_max) // 2, (y_min + y_max) // 2)
        return face_roi, (x_min, y_min, x_max, y_max), center

    @safe_method
    def get_gender(self, face_img):
        """Detecta género del rostro"""
        try:
            result = DeepFace.analyze(face_img, actions=['gender'], enforce_detection=False)
            return result[0]['gender']
        except Exception as e:
            print(f"[SWAPFACE] Error analizando género: {e}")
            return 'Unknown'

    @safe_method
    def preprocess_references(self, hombres_photos, mujeres_photos):
        """Preprocesa fotos de referencia"""
        self.hombres_faces = []
        self.mujeres_faces = []
        
        for path in hombres_photos:
            try:
                img = cv2.imread(path)
                faces = self.detect_faces(img)
                if faces:
                    face, _, _ = self.extract_face(img, faces[0])
                    if face is not None and face.shape[0] > 0 and face.shape[1] > 0:
                        self.hombres_faces.append(face)
            except:
                pass
        
        for path in mujeres_photos:
            try:
                img = cv2.imread(path)
                faces = self.detect_faces(img)
                if faces:
                    face, _, _ = self.extract_face(img, faces[0])
                    if face is not None and face.shape[0] > 0 and face.shape[1] > 0:
                        self.mujeres_faces.append(face)
            except:
                pass
        
        print(f"[SWAPFACE] Caras de hombres: {len(self.hombres_faces)}, Caras de mujeres: {len(self.mujeres_faces)}")

    @safe_method
    def create_face_mask(self, face_shape):
        """Crea máscara de blending"""
        mask = np.zeros((face_shape[0], face_shape[1]), dtype=np.uint8)
        axes = (int(face_shape[1] / 2.1), int(face_shape[0] / 2.1))
        center = (face_shape[1] // 2, face_shape[0] // 2)
        cv2.ellipse(mask, center, axes, 0, 0, 360, 255, -1)
        return mask

    @safe_method
    def swap_faces_gender_video_blend(self, hombres_photos, mujeres_photos, video_path, output_path="swapface_blend_video_output.mp4", max_minutes=5):
        """
        Intercambia rostros en video con blending por género
        """
        self.preprocess_references(hombres_photos, mujeres_photos)

        cap = cv2.VideoCapture(video_path)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames_allowed = int(fps * 60 * max_minutes)
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        count = 0
        print(f"[SWAPFACE] Procesando video... (máximo {max_minutes} min)")
        
        while True:
            ret, frame = cap.read()
            if not ret or count >= total_frames_allowed:
                break

            faces = self.detect_faces(frame)
            genders_in_frame = []
            face_positions = []
            face_centers = []

            for landmarks in faces:
                face_img, (x_min, y_min, x_max, y_max), center = self.extract_face(frame, landmarks)
                if face_img is None or face_img.shape[0] == 0 or face_img.shape[1] == 0:
                    genders_in_frame.append('Unknown')
                    face_positions.append((x_min, y_min, x_max, y_max))
                    face_centers.append(center)
                    continue
                gender = self.get_gender(face_img)
                genders_in_frame.append(gender)
                face_positions.append((x_min, y_min, x_max, y_max))
                face_centers.append(center)

            hombres_idxs = [i for i, g in enumerate(genders_in_frame) if g == 'Man']
            mujeres_idxs = [i for i, g in enumerate(genders_in_frame) if g == 'Woman']

            hombres_orden = list(range(len(self.hombres_faces)))
            mujeres_orden = list(range(len(self.mujeres_faces)))
            random.shuffle(hombres_orden)
            random.shuffle(mujeres_orden)

            for i, idx in enumerate(hombres_idxs):
                if self.hombres_faces:
                    face = self.hombres_faces[hombres_orden[i % len(self.hombres_faces)]]
                    x_min, y_min, x_max, y_max = face_positions[idx]
                    h_, w_ = y_max - y_min, x_max - x_min
                    if h_ < 5 or w_ < 5: continue
                    face_resized = cv2.resize(face, (w_, h_))
                    mask = self.create_face_mask(face_resized.shape)
                    try:
                        frame[y_min:y_max, x_min:x_max] = cv2.seamlessClone(
                            face_resized, frame[y_min:y_max, x_min:x_max], mask, (w_//2, h_//2), cv2.NORMAL_CLONE
                        )
                    except:
                        frame[y_min:y_max, x_min:x_max] = face_resized

            for i, idx in enumerate(mujeres_idxs):
                if self.mujeres_faces:
                    face = self.mujeres_faces[mujeres_orden[i % len(self.mujeres_faces)]]
                    x_min, y_min, x_max, y_max = face_positions[idx]
                    h_, w_ = y_max - y_min, x_max - x_min
                    if h_ < 5 or w_ < 5: continue
                    face_resized = cv2.resize(face, (w_, h_))
                    mask = self.create_face_mask(face_resized.shape)
                    try:
                        frame[y_min:y_max, x_min:x_max] = cv2.seamlessClone(
                            face_resized, frame[y_min:y_max, x_min:x_max], mask, (w_//2, h_//2), cv2.NORMAL_CLONE
                        )
                    except:
                        frame[y_min:y_max, x_min:x_max] = face_resized

            out.write(frame)
            count += 1
            if count % 50 == 0:
                print(f"   Procesados {count} frames...")

        cap.release()
        out.release()
        print(f"[SWAPFACE] ✓ Video guardado en {output_path}")
        return True