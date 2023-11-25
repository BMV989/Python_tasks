import sys
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QTimer, QTime, QUrl, Qt
import os
import urllib.request
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QHBoxLayout, QLineEdit, QPushButton, QLabel


class Timer(QWidget):
    def __init__(self):
        super().__init__()
        self.init_window()
        self.init_audio()
        self.init_timer_label()
        self.init_hours_field()
        self.init_minutes_field()
        self.init_seconds_field()
        self.init_buttons()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.remaining_time = QTime(0, 0, 0)

    def start_timer(self):
        if self.remaining_time != QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(1)
            self.timer.start(1000)
            return

        if self.hours_input.text():
            h = int(self.hours_input.text())
        else:
            h = 0
        if self.minutes_input.text():
            min = int(self.minutes_input.text())
        else:
            min = 0
        if self.seconds_input.text():
            sec = int(self.seconds_input.text())
        else:
            sec = 0

        self.remaining_time = QTime(h, min, sec)
        self.timer.start(1000)

    def pause_timer(self):
        if self.timer.isActive():
            self.timer.stop()
            self.remaining_time = self.remaining_time.addSecs(
                self.timer.remainingTime() // 1000)

    def stop_timer(self):
        self.timer.stop()
        self.remaining_time = QTime(0, 0, 0)
        self.timer_label.setText('00:00:00')

    def update_timer(self):
        if self.remaining_time > QTime(0, 0, 0):
            self.remaining_time = self.remaining_time.addSecs(-1)
            self.timer_label.setText(self.remaining_time.toString('hh:mm:ss'))
        else:
            self.timer.stop()
            self.play_ring()

    def play_ring(self):
        self.player.play()

    @staticmethod
    def download_ring():
        if not os.path.exists('./ring.mp3'):
            content = urllib.request.urlopen(
                "https://ringtonedownloadmp3.net/dowload?id=1257&type=mp3"
            ).read()
            with open('./ring.mp3', 'wb') as ring:
                ring.write(content)
        return 'ring.mp3'

    def init_window(self):
        self.setWindowTitle('Big_Tymer')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet("background-color: #593E67;")

    def init_audio(self):
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.player.setSource(QUrl.fromLocalFile(self.download_ring()))
        self.audio_output.setVolume(0.50)

    def init_timer_label(self):
        self.timer_label = QLabel('00:00:00', self)
        self.timer_label.setStyleSheet("font-size: 30px;")
        self.timer_label.setAlignment(
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

    def init_hours_field(self):
        self.hours_input = QLineEdit(self)
        self.hours_input.setPlaceholderText("Hours")
        self.hours_input.setStyleSheet("""
                                           QLineEdit {
                                               background-color: #273746;
                                               color: #fffffe;
                                               border: 2px solid #eaecee;
                                               padding: 8px;
                                               border-radius: 5px;
                                           }
                                       """)

    def init_minutes_field(self):
        self.minutes_input = QLineEdit(self)
        self.minutes_input.setPlaceholderText("Minutes")
        self.minutes_input.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #273746;
                                                color: #fffffe;
                                                border: 2px solid #eaecee;
                                                padding: 8px;
                                                border-radius: 5px;
                                            }
                                        """)

    def init_seconds_field(self):
        self.seconds_input = QLineEdit(self)
        self.seconds_input.setPlaceholderText("Seconds")
        self.seconds_input.setStyleSheet("""
                                            QLineEdit {
                                                background-color: #273746;
                                                color: #fffffe;
                                                border: 2px solid #eaecee;
                                                padding: 8px;
                                                border-radius: 5px;
                                            }
                                        """)

    def init_buttons(self):
        buttons = [QPushButton('start', self), QPushButton(
            'pause', self), QPushButton('stop', self)]
        self.button_style = """
                                            QPushButton {
                                                background-color: #000000;
                                                color: #fffffe;
                                                border: 2px solid #eaecee;
                                                padding: 10px;
                                                border-radius: 5px;
                                            }
                                            QPushButton:hover {
                                                background-color: #2c3e50;
                                            }
                                        """

        for button in buttons:
            button.setStyleSheet(self.button_style)

        buttons[0].clicked.connect(self.start_timer)
        buttons[1].clicked.connect(self.pause_timer)
        buttons[2].clicked.connect(self.stop_timer)
        self.add_widgets(buttons[0], buttons[1], buttons[2])

    def add_widgets(self, start_button, pause_button, stop_button):
        lay = QVBoxLayout()
        input_lay = QHBoxLayout()

        input_lay.addWidget(self.hours_input)
        input_lay.addWidget(self.minutes_input)
        input_lay.addWidget(self.seconds_input)

        control_lay = QHBoxLayout()
        control_lay.addWidget(start_button)
        control_lay.addWidget(pause_button)
        control_lay.addWidget(stop_button)

        lay.addWidget(self.timer_label)
        lay.addLayout(input_lay)
        lay.addLayout(control_lay)
        self.setLayout(lay)


def main():
    app = QApplication([])
    timer = Timer()
    timer.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
