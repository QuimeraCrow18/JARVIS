# ==========================================
# FACES PANEL UI
# ui/faces_panel.py
# ==========================================

import customtkinter as ctk

from PIL import Image

import threading


class FacesPanelUI:

    def __init__(self):

        # ======================================
        # VENTANA
        # ======================================

        self.root = ctk.CTkToplevel()

        self.root.title(
            "Rostros Detectados"
        )

        self.root.geometry(
            "700x500"
        )

        self.root.resizable(
            False,
            False
        )

        # ======================================
        # LISTAS
        # ======================================

        self.selected_faces = []

        self.face_buttons = []

        self.face_paths = []

        # ======================================
        # SCROLLABLE FRAME
        # ======================================

        self.scroll_frame = ctk.CTkScrollableFrame(
            self.root,
            width=650,
            height=350
        )

        self.scroll_frame.pack(
            pady=10,
            padx=10,
            fill="both",
            expand=True
        )

        # ======================================
        # TEXTO
        # ======================================

        self.info_label = ctk.CTkLabel(
            self.root,
            text="Selecciona los rostros a modificar"
        )

        self.info_label.pack(
            pady=5
        )

        # ======================================
        # BOTONES
        # ======================================

        self.buttons_frame = ctk.CTkFrame(
            self.root
        )

        self.buttons_frame.pack(
            pady=10
        )

        # CONFIRMAR

        self.confirm_button = ctk.CTkButton(
            self.buttons_frame,
            text="Confirmar",
            width=120,
            command=self.confirm_selection
        )

        self.confirm_button.grid(
            row=0,
            column=0,
            padx=10
        )

        # CANCELAR

        self.cancel_button = ctk.CTkButton(
            self.buttons_frame,
            text="Cancelar",
            width=120,
            fg_color="red",
            hover_color="#aa0000",
            command=self.cancel_selection
        )

        self.cancel_button.grid(
            row=0,
            column=1,
            padx=10
        )

        # ======================================
        # ESTADO
        # ======================================

        self.confirmed = False

        self.cancelled = False

        # ======================================
        # HILO GUI
        # ======================================

        threading.Thread(
            target=self.root.mainloop,
            daemon=True
        ).start()

    # ==========================================
    # MOSTRAR ROSTROS
    # ==========================================

    def show_faces(self, faces_list):

        try:

            # Limpiar botones anteriores

            for btn in self.face_buttons:

                btn.destroy()

            self.face_buttons.clear()

            self.selected_faces.clear()

            self.face_paths = faces_list

            # ==================================
            # CREAR MINIATURAS
            # ==================================

            for index, face_path in enumerate(faces_list):

                image = Image.open(face_path)

                image.thumbnail(
                    (120, 120)
                )

                ctk_image = ctk.CTkImage(
                    light_image=image,
                    dark_image=image,
                    size=(120, 120)
                )

                button = ctk.CTkButton(
                    self.scroll_frame,
                    image=ctk_image,
                    text="",
                    width=130,
                    height=130,
                    fg_color="#222222",
                    hover_color="#444444",
                    command=lambda p=face_path:
                    self.toggle_face(p)
                )

                row = index // 4

                column = index % 4

                button.grid(
                    row=row,
                    column=column,
                    padx=10,
                    pady=10
                )

                self.face_buttons.append(
                    button
                )

            self.confirmed = False

            self.cancelled = False

            self.root.deiconify()

            self.root.lift()

        except Exception as e:

            print("[FACES UI ERROR]", e)

    # ==========================================
    # SELECCIONAR / DESELECCIONAR
    # ==========================================

    def toggle_face(self, face_path):

        try:

            if face_path in self.selected_faces:

                self.selected_faces.remove(
                    face_path
                )

                print(
                    f"[FACE] Deseleccionado: {face_path}"
                )

            else:

                self.selected_faces.append(
                    face_path
                )

                print(
                    f"[FACE] Seleccionado: {face_path}"
                )

        except Exception as e:

            print("[TOGGLE ERROR]", e)

    # ==========================================
    # CONFIRMAR
    # ==========================================

    def confirm_selection(self):

        self.confirmed = True

        self.root.withdraw()

    # ==========================================
    # CANCELAR
    # ==========================================

    def cancel_selection(self):

        self.cancelled = True

        self.selected_faces.clear()

        self.root.withdraw()

    # ==========================================
    # OBTENER SELECCIÓN
    # ==========================================

    def get_selected_faces(self):

        return self.selected_faces

    # ==========================================
    # ESPERAR CONFIRMACIÓN
    # ==========================================

    def wait_for_selection(self):

        while True:

            if self.confirmed:

                return self.selected_faces

            if self.cancelled:

                return []

    # ==========================================
    # UPDATE
    # ==========================================

    def update(self):

        try:

            self.root.update()

        except:

            pass