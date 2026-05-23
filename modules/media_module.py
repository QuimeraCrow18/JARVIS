# ==========================================
# MEDIA MODULE
# ==========================================

import os
import cv2
import shutil
import tempfile


class MediaModule:

    def __init__(self):

        self.files = []

        print(
            "[MEDIA] Módulo cargado."
        )

    # ======================================
    # CARGAR ARCHIVOS
    # ======================================

    def load_files(self, files):

        self.files = files

        print(
            f"[MEDIA] {len(files)} archivo(s) cargado(s)"
        )

    # ======================================
    # DETECTAR ROSTROS
    # ======================================

    def detect_faces(self):

        detected_faces = []

        face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        for file in self.files:

            if not os.path.exists(file):

                continue

            image = cv2.imread(file)

            if image is None:

                continue

            gray = cv2.cvtColor(
                image,
                cv2.COLOR_BGR2GRAY
            )

            faces = face_detector.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(40, 40)
            )

            for (x, y, w, h) in faces:

                face_crop = image[
                    y:y+h,
                    x:x+w
                ]

                detected_faces.append({
                    "file": file,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h,
                    "face": face_crop
                })

        print(
            f"[MEDIA] {len(detected_faces)} rostro(s) detectado(s)"
        )

        return detected_faces

    # ======================================
    # FACE SWAP
    # ======================================

    def apply_face_swap(
        self,
        selected_faces,
        replacement_files
    ):

        if not selected_faces:

            print(
                "[FACE SWAP] No hay rostros seleccionados"
            )

            return

        if not replacement_files:

            print(
                "[FACE SWAP] No hay reemplazos"
            )

            return

        print(
            "[FACE SWAP] Iniciando..."
        )

        replacement_images = []

        for replacement in replacement_files:

            image = cv2.imread(
                replacement
            )

            if image is not None:

                replacement_images.append(
                    image
                )

        if not replacement_images:

            print(
                "[FACE SWAP] Imágenes inválidas"
            )

            return

        for index, face_data in enumerate(selected_faces):

            file = face_data["file"]

            x = face_data["x"]

            y = face_data["y"]

            w = face_data["w"]

            h = face_data["h"]

            image = cv2.imread(file)

            if image is None:

                continue

            replacement = replacement_images[
                index % len(replacement_images)
            ]

            resized_face = cv2.resize(
                replacement,
                (w, h)
            )

            image[
                y:y+h,
                x:x+w
            ] = resized_face

            output_file = (
                tempfile.gettempdir()
                + f"/faceswap_{index}.jpg"
            )

            cv2.imwrite(
                output_file,
                image
            )

            print(
                f"[FACE SWAP] Guardado: {output_file}"
            )

        print(
            "[FACE SWAP] Finalizado"
        )

    # ======================================
    # MODIFICAR POSE
    # ======================================

    def apply_pose(
        self,
        files,
        pose_description
    ):

        print(
            "[POSE] Procesando pose..."
        )

        print(
            f"[POSE] {pose_description}"
        )

        for file in files:

            if os.path.exists(file):

                print(
                    f"[POSE] Archivo: {file}"
                )

        print(
            "[POSE] Finalizado"
        )

    # ======================================
    # LIMPIAR
    # ======================================

    def clear(self):

        self.files = []

        print(
            "[MEDIA] Archivos limpiados"
        )