import sys
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout
)
from PyQt6.QtCore import QTimer, QTime


class ShutdownTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Таймер выключения")

        self.time_label = QLabel("00:00:00", self)
        self.time_label.setStyleSheet("font-size: 24px;")


        self.hours_input = QLineEdit(self)
        self.hours_input.setPlaceholderText("Часы")

        self.minutes_input = QLineEdit(self)
        self.minutes_input.setPlaceholderText("Минуты")

        self.seconds_input = QLineEdit(self)
        self.seconds_input.setPlaceholderText("Секунды")

        self.start_button = QPushButton("Запустить таймер", self)
        self.start_button.clicked.connect(self.start_timer)

        self.stop_button = QPushButton("Остановить таймер", self)
        self.stop_button.clicked.connect(self.stop_timer)
        self.stop_button.setEnabled(False)

        # Разметка
        layout = QVBoxLayout()
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.hours_input)
        time_layout.addWidget(self.minutes_input)
        time_layout.addWidget(self.seconds_input)

        layout.addLayout(time_layout)
        layout.addWidget(self.time_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = 0

    def start_timer(self):
        try:
            hours = int(self.hours_input.text()) if self.hours_input.text() else 0
            minutes = int(self.minutes_input.text()) if self.minutes_input.text() else 0
            seconds = int(self.seconds_input.text()) if self.seconds_input.text() else 0

            self.remaining_time = hours * 3600 + minutes * 60 + seconds

            if self.remaining_time <= 0:
                raise ValueError("Время должно быть больше 0")
            self.timer.start(1000)
            self.hours_input.setEnabled(False)
            self.minutes_input.setEnabled(False)
            self.seconds_input.setEnabled(False)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except ValueError as e:
            print(f"Ошибка: {e}")

    def update_timer(self):
        self.remaining_time -= 1
        time_str = QTime.fromMSecsSinceStartOfDay(self.remaining_time * 1000).toString("hh:mm:ss")
        self.time_label.setText(time_str)

        if self.remaining_time == 0:
            self.timer.stop()
            self.execute_shutdown()
            self.close()

    def stop_timer(self):
        self.timer.stop()
        self.hours_input.setEnabled(True)
        self.minutes_input.setEnabled(True)
        self.seconds_input.setEnabled(True)
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.time_label.setText("00:00:00")

    def execute_shutdown(self):
        try:
            subprocess.Popen(['cmd.exe', '/c', 'shutdown -s -t 0'], creationflags=subprocess.CREATE_NEW_CONSOLE)
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ShutdownTimer()
    window.show()
    sys.exit(app.exec())