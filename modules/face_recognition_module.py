import os
import json

from core.utils import safe_method


class FaceRecognitionModule:

    def __init__(self):

        self.known_faces_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "known_faces"
        )
        os.makedirs(self.known_faces_dir, exist_ok=True)

        self._deepface = None
        self._deepface_available = False

        self._init_deepface()

        print("[FACE-RECOG] Módulo de reconocimiento facial iniciado.")

    def _init_deepface(self):

        try:
            from deepface import DeepFace as _df
            self._deepface = _df
            self._deepface_available = True
            print("[FACE-RECOG] DeepFace cargado correctamente.")
        except Exception as e:
            print(f"[FACE-RECOG] DeepFace no disponible: {e}")
            print("[FACE-RECOG] Usando modo sin IA (solo detección básica).")

    @safe_method
    def register_face(self, image_path, name):

        if not os.path.exists(image_path):
            print(f"[FACE-RECOG] Error: {image_path} no existe.")
            return False

        dest_dir = os.path.join(self.known_faces_dir, name)
        os.makedirs(dest_dir, exist_ok=True)

        import shutil
        dest_path = os.path.join(dest_dir, f"{name}_{len(os.listdir(dest_dir))}.jpg")
        shutil.copy2(image_path, dest_path)

        print(f"[FACE-RECOG] Rostro registrado: {name} ({dest_path})")
        return True

    @safe_method
    def list_known_faces(self):

        if not os.path.isdir(self.known_faces_dir):
            return []

        people = []
        for entry in os.listdir(self.known_faces_dir):
            entry_path = os.path.join(self.known_faces_dir, entry)
            if os.path.isdir(entry_path):
                images = [f for f in os.listdir(entry_path)
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
                if images:
                    people.append({
                        "name": entry,
                        "images": len(images),
                        "path": entry_path
                    })

        return people

    @safe_method
    def recognize(self, image_path):

        if not os.path.exists(image_path):
            print(f"[FACE-RECOG] Error: {image_path} no existe.")
            return []

        if not self._deepface_available:
            print("[FACE-RECOG] DeepFace no disponible. No se puede reconocer.")
            return self._detect_only(image_path)

        try:
            dfs = self._deepface.find(
                img_path=image_path,
                db_path=self.known_faces_dir,
                silent=True,
                model_name="Facenet"
            )

            results = []
            if isinstance(dfs, list):
                for df in dfs:
                    if df is not None and not df.empty:
                        for _, row in df.iterrows():
                            identity = row.get("identity", "")
                            name = os.path.basename(os.path.dirname(identity))
                            distance = row.get("distance", 1.0)
                            if distance < 0.4:
                                results.append({
                                    "name": name,
                                    "confidence": round((1 - distance) * 100, 2),
                                    "identity": identity
                                })

            if results:
                print(f"[FACE-RECOG] Reconocido: {results[0]['name']} "
                      f"({results[0]['confidence']}% confianza)")
            else:
                print("[FACE-RECOG] No se reconoció ningún rostro conocido.")

            return results

        except Exception as e:
            print(f"[FACE-RECOG] Error durante reconocimiento: {e}")
            return self._detect_only(image_path)

    @safe_method
    def verify(self, image_path1, image_path2):

        if not os.path.exists(image_path1):
            print(f"[FACE-RECOG] Error: {image_path1} no existe.")
            return None

        if not os.path.exists(image_path2):
            print(f"[FACE-RECOG] Error: {image_path2} no existe.")
            return None

        if not self._deepface_available:
            print("[FACE-RECOG] DeepFace no disponible. Usando OpenCV (básico).")
            return self._verify_opencv(image_path1, image_path2)

        try:
            result = self._deepface.verify(
                img1_path=image_path1,
                img2_path=image_path2,
                model_name="Facenet",
                silent=True
            )

            verified = result.get("verified", False)
            distance = result.get("distance", 1.0)

            output = {
                "verified": verified,
                "distance": round(distance, 4),
                "confidence": round((1 - distance) * 100, 2)
            }

            if verified:
                print(f"[FACE-RECOG] Coinciden ({output['confidence']}% confianza)")
            else:
                print(f"[FACE-RECOG] No coinciden (distancia: {distance:.4f})")

            return output

        except Exception as e:
            print(f"[FACE-RECOG] Error en verificación: {e}")
            return self._verify_opencv(image_path1, image_path2)

    @safe_method
    def detect_faces(self, image_path):

        if not os.path.exists(image_path):
            print(f"[FACE-RECOG] Error: {image_path} no existe.")
            return []

        try:
            import cv2
        except ImportError:
            print("[FACE-RECOG] OpenCV no disponible.")
            return []

        image = cv2.imread(image_path)
        if image is None:
            print(f"[FACE-RECOG] No se pudo leer: {image_path}")
            return []

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

        faces = detector.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )

        results = []
        for (x, y, w, h) in faces:
            face_crop = image[y:y+h, x:x+w]
            results.append({
                "x": int(x), "y": int(y),
                "w": int(w), "h": int(h),
                "face": face_crop
            })

        print(f"[FACE-RECOG] {len(results)} rostro(s) detectado(s)")
        return results

    def _detect_only(self, image_path):

        faces = self.detect_faces(image_path)
        return [{"name": "Desconocido", "confidence": 0.0,
                 "face_rect": {"x": f["x"], "y": f["y"],
                               "w": f["w"], "h": f["h"]}}
                for f in faces] if faces else []

    def _verify_opencv(self, image_path1, image_path2):

        try:
            import cv2
        except ImportError:
            print("[FACE-RECOG] OpenCV no disponible para verificación.")
            return {"verified": False, "distance": 1.0, "confidence": 0.0}

        img1 = cv2.imread(image_path1)
        img2 = cv2.imread(image_path2)

        if img1 is None or img2 is None:
            return {"verified": False, "distance": 1.0, "confidence": 0.0}

        gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

        if gray1.shape != gray2.shape:
            gray2 = cv2.resize(gray2, (gray1.shape[1], gray1.shape[0]))

        diff = cv2.norm(gray1, gray2, cv2.NORM_L2)
        h, w = gray1.shape
        distance = diff / (h * w * 255)

        return {
            "verified": distance < 0.15,
            "distance": round(distance, 4),
            "confidence": round((1 - distance) * 100, 2)
        }
