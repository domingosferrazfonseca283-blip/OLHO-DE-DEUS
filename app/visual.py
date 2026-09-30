import math
import tkinter as tk


class MotorVisual:
    def __init__(self, root, label):
        self.root = root
        self.label = label

        self.angulo = 0
        self.pulsacao = 0
        self.ativo = False

    def iniciar(self):
        if self.ativo:
            return

        self.ativo = True
        self.animar()

    def parar(self):
        self.ativo = False

    def animar(self):
        if not self.ativo:
            return

        self.angulo += 8
        self.pulsacao += 0.12

        intensidade = int(
            180 + 60 * math.sin(self.pulsacao)
        )

        intensidade = max(
            120,
            min(240, intensidade)
        )

        cor = f"#4de1{intensidade:02x}"

        simbolo = "◉"

        if self.angulo % 32 < 16:
            simbolo = "◉"
        else:
            simbolo = "⊙"

        self.label.configure(
            text=simbolo,
            fg=cor
        )

        self.root.after(
            80,
            self.animar
        )


def criar_motor_visual(root, label):
    motor = MotorVisual(
        root,
        label
    )

    motor.iniciar()

    return motor
