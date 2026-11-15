from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QApplication, QSizePolicy, QSpacerItem
from PyQt5.QtGui import QPainter, QColor, QBrush, QRadialGradient, QPainterPath, QLinearGradient
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, Qt, QMetaObject, Q_ARG
from Class.Launch import Launch
import threading
import sys
import io
import platform
import random


class SignalHandler(QObject):
    """
    Class for managing signals between threads.
    """
    update_status_signal = pyqtSignal(str)
    show_response_signal = pyqtSignal(str)
    turn_off_light_signal = pyqtSignal()
    close_app_signal = pyqtSignal()


class OutputInterceptor(io.StringIO):
    """
    Class for capturing and intercepting standard output while preserving the original output stream.

    :param TextIO original_stdout: The original standard output stream before redirection.
    :param SignalHandler signal_handler: The signal handler for emitting captured output in real time.
    """
    def __init__(self, original_stdout, signal_handler):
        """Initializes the OutputInterceptor class."""
        super().__init__()
        self.original_stdout = original_stdout
        self.signal_handler = signal_handler

    def write(self, message):
        """
        Writes a message to both the original standard output and the internal buffer.

        :param str message: The message to write.
        """
        if hasattr(self.original_stdout, "write"):
            self.original_stdout.write(message)
            self.original_stdout.flush()

        cleaned_message = message.strip()
        if cleaned_message and "[DEBUG]" not in cleaned_message and cleaned_message != "Écoute..." and "http" not in cleaned_message:
            QMetaObject.invokeMethod(self.signal_handler, "show_response_signal", Qt.QueuedConnection, Q_ARG(str, cleaned_message))


class Ball(QWidget):
    """
    A custom widget that draws a circle and handles mouse events.
    """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        """Initializes the Ball class."""
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.moon_phase = "inactive"
        self.is_hovered = False
        self.moon_size = 150
        self.moon_x = (self.width() - self.moon_size) // 2
        self.moon_y = (self.height() - self.moon_size) // 2
    
    def set_moon_phase(self, phase):
        """
        Sets the moon phase.

        :param str phase: "inactive", "listening", or "thinking".
        """
        self.moon_phase = phase
        self.update()

    def enterEvent(self, event):
        """Handles the event when the mouse cursor enters the widget."""
        self.is_hovered = True
        self.update()
    
    def leaveEvent(self, event):
        """Handles the event when the mouse cursor leaves the widget."""
        self.is_hovered = False
        self.update()
    
    def mousePressEvent(self, event):
        """
        Handles mouse click events on the ball.

        :param QMouseEvent event: The mouse event containing the click position.
        """
        if event.button() == Qt.LeftButton:
            self.clicked.emit()
    
    def paintEvent(self, event):
        """Draw the Moon."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        moon_color = QColor(220, 220, 200)

        painter.setBrush(moon_color)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.moon_x, self.moon_y, self.moon_size, self.moon_size)

        if self.moon_phase in ["inactive", "listening"]:
            shadow_x = self.moon_x + self.moon_size // 2

            shadow_path = QPainterPath()
            shadow_path.addEllipse(self.moon_x, self.moon_y, self.moon_size, self.moon_size)
            painter.setClipPath(shadow_path)

            gradient = QLinearGradient(shadow_x - 30, self.moon_y, shadow_x + self.moon_size // 2 + 20, self.moon_y + self.moon_size)

            if self.moon_phase == "inactive":
                gradient.setColorAt(0.0, QColor(40, 40, 50, 30))
                gradient.setColorAt(0.4, QColor(50, 50, 60, 120))
                gradient.setColorAt(1.0, QColor(20, 20, 30, 200))
                painter.setBrush(QBrush(gradient))
                painter.drawEllipse(shadow_x - 50, self.moon_y, self.moon_size // 2 + 60, self.moon_size)

            elif self.moon_phase == "listening":
                gradient.setColorAt(0.0, QColor(60, 60, 70, 80))
                gradient.setColorAt(0.5, QColor(30, 30, 40, 180))
                gradient.setColorAt(1.0, QColor(15, 15, 25, 220))
                painter.setBrush(QBrush(gradient))
                painter.drawEllipse(shadow_x - 25, self.moon_y, self.moon_size // 2 + 35, self.moon_size)

            painter.setClipping(False)

        if self.is_hovered:
            glow_center_x = self.moon_x + self.moon_size // 2
            glow_center_y = self.moon_y + self.moon_size // 2
            glow_radius = self.moon_size * 1.6

            glow_gradient = QRadialGradient(glow_center_x, glow_center_y, glow_radius)
            glow_gradient.setColorAt(0.0, QColor(255, 255, 240, 110))
            glow_gradient.setColorAt(0.3, QColor(200, 200, 255, 60))
            glow_gradient.setColorAt(0.8, QColor(100, 100, 255, 30))
            glow_gradient.setColorAt(1.0, QColor(50, 50, 255, 0))

            painter.setBrush(QBrush(glow_gradient))
            painter.drawEllipse(self.moon_x - 10, self.moon_y - 10, self.moon_size + 20, self.moon_size + 20)

class Widget(QWidget):
    """
    Manages the graphical interface for the Luna voice assistant.

    This class creates a window with buttons and labels for interacting with Luna.

    :param bool debug: Mode of operation ('Normal' or 'Debug'). If not specified, defaults to 'Normal'.
    """
    def __init__(self, debug):
        """Initializes the Widget class."""
        super().__init__()
        self.init_ui()
        self.stars = [(random.randint(0, 1920), random.randint(0, 1080)) for _ in range(200)]
        self.launch = Launch(mode="Vocal", option="Debug" if debug else "Normal")
        self.is_listening = False

        self.signal_handler = SignalHandler()
        self.signal_handler.update_status_signal.connect(self.update_status)
        self.signal_handler.show_response_signal.connect(self.show_response)
        self.signal_handler.turn_off_light_signal.connect(self.turn_off_light)
        self.signal_handler.close_app_signal.connect(self.close_app)

        self.running_timer = QTimer()
        self.running_timer.timeout.connect(self.check_running_status)
        self.running_timer.start(500)

        self.original_stdout = sys.stdout
        self.interceptor = OutputInterceptor(self.original_stdout, self.signal_handler)
        sys.stdout = self.interceptor

        if self.launch.option == "Debug":
            print("[DEBUG] Creating a Widget class variable")


    def init_ui(self):
        """
        Configures the window's user interface.

        This method creates and positions GUI elements, including the window title, status label and listen button.
        """
        self.setWindowTitle("Luna - Voice assistant")
        self.resize(800, 600)
        self.setMinimumSize(400, 300)

        self.setStyleSheet("background-color: #0A0A32;")

        layout = QVBoxLayout()

        self.status_label = QLabel("Luna est prête à écouter", self)
        self.status_label.setStyleSheet("font-size: 16px; font-weight: bold; color: white;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addSpacerItem(QSpacerItem(20, 100, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.ball = Ball(self)
        self.ball.clicked.connect(self.start_listening)
        layout.addWidget(self.ball, alignment=Qt.AlignCenter)

        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.response_label = QLabel("", self)
        self.response_label.setStyleSheet("font-size: 14px; font-weight: bold; color: white;")
        self.response_label.setAlignment(Qt.AlignCenter)
        self.response_label.setWordWrap(True)
        layout.addWidget(self.response_label)

        layout.addSpacerItem(QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(layout)

    def start_listening(self):
        """Start listening to the voice."""
        if not self.is_listening:
            self.is_listening = True
            self.ball.set_moon_phase("listening")
            self.update()
            self.signal_handler.update_status_signal.emit("Écoute en cours...")
            threading.Thread(target=self.listen_to_voice).start()
    
    def listen_to_voice(self):
        """Captures and processes the user's voice."""
        sentence = self.launch.input.input_sentence()
        if sentence:
            self.process_command(sentence)
        self.is_listening = False
        self.signal_handler.turn_off_light_signal.emit()
    
    def process_command(self, command):
        """
        Processes voice commands.
        
        :param str command: sentence that has been detected.
        """
        self.signal_handler.update_status_signal.emit(f"Vous avez dit : {command}")
        
        if not self.banned_cmd(command):
            self.ball.set_moon_phase("thinking")
            self.update()
            try:
                self.launch.chatbot.get_response(self.launch, command, self.launch.audio)
            finally:
                self.signal_handler.turn_off_light_signal.emit()
    
    def banned_cmd(self, cmd):
        """
        Checks whether a command is forbidden and displays a message if necessary.

        :param str cmd: Voice command to check.
        :return: True if the command is forbidden, False otherwise.
        """
        system_os = platform.system().lower()

        banned_phrases = {
            "windows": [("audio", "active"), ("voix",)],
            "general": [("pause",), ("repos",), ("repose",)],
            "input_mode": [("change", "mode"), ("switch", "mode"), ("input",)]
        }

        if system_os == "windows" and any(all(word in cmd for word in pair) for pair in banned_phrases["windows"]):
            self.show_response("L'audio n'est pas pris en charge par l'interface graphique sur Windows.")
            return True
        elif any(all(word in cmd for word in pair) for pair in banned_phrases["general"]):
            self.show_response("La commande de \"Pause\" n'est pas implémentée sur l'interface graphique.")
            return True
        elif self.launch.input.mode == "Vocal" and any(all(word in cmd for word in pair) for pair in banned_phrases["input_mode"]):
            self.show_response("Le mode \"Input\" n'est pas pris en charge par l'interface graphique de Luna.")
            return True
        else:
            return False

    def turn_off_light(self):
        """Turns off the light ball."""
        QTimer.singleShot(500, self._turn_off_light_callback)

    def _turn_off_light_callback(self):
        """Callback to switch off the light ball."""
        self.ball.set_moon_phase("inactive")
    
    def update_status(self, status):
        """
        Updates the status label.
        
        :param str status: status that has been updated.
        """
        self.status_label.setText(status)

    def show_response(self, response):
        """
        Displays Luna's answer.
        
        :param str response: sentence that has been responsed.
        """
        if self.launch.option == "Debug":
            print(f"[DEBUG] Received response signal: {response}")
        self.response_label.setText(response)

    def check_running_status(self):
        """Checks if launch.running is False and closes the application if necessary."""
        if not self.launch.running:
            self.signal_handler.close_app_signal.emit()

    def close_app(self):
        """Closes the PyQt application."""
        self.running_timer.stop()
        self.close()
        QApplication.quit()
    
    def paintEvent(self, event):
        """Draw the stars"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setPen(QColor(255, 255, 255))
        for x, y in self.stars:
            painter.drawPoint(x, y)