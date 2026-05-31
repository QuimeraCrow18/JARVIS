# ============================================
# JARVIS - ENHANCE MODULE
# Mejora de imagen / filtros / upscale
# ============================================

import os


class EnhanceModule:

    def __init__(self):
        print("[ENHANCE] Modulo cargado")

    def _cv2(self):
        import cv2
        return cv2

    # ============================================
    # MEJORAR CALIDAD
    # ============================================
    def enhance_image(self, image_path):

        if not os.path.exists(image_path):
            print("[ERROR] Imagen no encontrada")
            return None

        image = self._cv2().imread(image_path)

        if image is None:
            print("[ERROR] No se pudo abrir la imagen")
            return None

        # Reducir ruido
        image = self._cv2().fastNlMeansDenoisingColored(
            image,
            None,
            10,
            10,
            7,
            21
        )

        # Sharpen
        kernel = [
            [-1, -1, -1],
            [-1,  9, -1],
            [-1, -1, -1]
        ]

        import numpy as np

        kernel = np.array(kernel)

        image = self._cv2().filter2D(image, -1, kernel)

        output_path = "output/enhanced_image.jpg"

        os.makedirs("output", exist_ok=True)

        self._cv2().imwrite(output_path, image)

        print(f"[ENHANCE] Imagen guardada: {output_path}")

        return output_path

    # ============================================
    # FILTRO 4K SIMULADO
    # ============================================
    def upscale_4k(self, image_path):

        if not os.path.exists(image_path):
            print("[ERROR] Imagen no encontrada")
            return None

        image = self._cv2().imread(image_path)

        if image is None:
            print("[ERROR] No se pudo abrir la imagen")
            return None

        height, width = image.shape[:2]

        upscale = self._cv2().resize(
            image,
            (width * 2, height * 2),
            interpolation=self._cv2().INTER_CUBIC
        )

        output_path = "output/upscale_4k.jpg"

        os.makedirs("output", exist_ok=True)

        self._cv2().imwrite(output_path, upscale)

        print(f"[UPSCALE] Imagen 4K guardada: {output_path}")

        return output_path

    # ============================================
    # AJUSTAR ILUMINACION
    # ============================================
    def improve_light(self, image_path):

        if not os.path.exists(image_path):
            print("[ERROR] Imagen no encontrada")
            return None

        image = self._cv2().imread(image_path)

        if image is None:
            print("[ERROR] No se pudo abrir la imagen")
            return None

        hsv = self._cv2().cvtColor(image, self._cv2().COLOR_BGR2HSV)

        h, s, v = self._cv2().split(hsv)

        v = self._cv2().equalizeHist(v)

        hsv = self._cv2().merge((h, s, v))

        result = self._cv2().cvtColor(hsv, self._cv2().COLOR_HSV2BGR)

        output_path = "output/light_fix.jpg"

        os.makedirs("output", exist_ok=True)

        self._cv2().imwrite(output_path, result)

        print(f"[LIGHT] Imagen mejorada: {output_path}")

        return output_path