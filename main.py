import sys
from PyQt6 import QtWidgets, QtGui, QtCore
import ctypes

class SystemTrayIcon(QtWidgets.QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip(f'My System Tray Icon')
        menu = QtWidgets.QMenu(parent)
        exit_action = menu.addAction("Закрыть приложение")
        exit_action.triggered.connect(self.exit_application)
        self.setContextMenu(menu)

    def update_tooltip(self, tooltip_text):
        self.setToolTip(tooltip_text)

    def exit_application(self):
        QtCore.QCoreApplication.quit()

class App(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'TimeMessage'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 280, 200)

        # Set the application icon
        app_icon = QtGui.QIcon("icon.png")
        self.setWindowIcon(app_icon)

        self.second_label = QtWidgets.QLabel('Интервал (секунды):', self)
        self.second_label.move(20, 20)

        self.second = QtWidgets.QLineEdit(self)
        self.second.move(150, 20)
        self.second.resize(100, 30)
        self.second.setPlaceholderText("Секунды")

        self.message_label = QtWidgets.QLabel('Текст сообщения:', self)
        self.message_label.move(20, 70)

        self.message = QtWidgets.QLineEdit(self)
        self.message.move(150, 70)
        self.message.resize(200, 30)
        self.message.setPlaceholderText("Текст сообщения")

        button = QtWidgets.QPushButton('Запустить таймер', self)
        button.setToolTip('Нажмите эту кнопку, чтобы запустить таймер')
        button.move(20, 120)
        button.clicked.connect(self.on_click)

        self.timer_label = QtWidgets.QLabel(self)
        self.timer_label.move(20, 160)
        self.timer_label.resize(300, 30)

        self.tray_icon = SystemTrayIcon(QtGui.QIcon("icon.png"), self)
        self.tray_icon.activated.connect(self.tray_icon_clicked)
        self.tray_icon.show()

        self.message_timer = QtCore.QTimer(self)
        self.message_timer.timeout.connect(self.show_message)

        self.countdown_timer = QtCore.QTimer(self)
        self.countdown_timer.timeout.connect(self.update_countdown)

        self.show()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def tray_icon_clicked(self, reason):
        if reason == QtWidgets.QSystemTrayIcon.ActivationReason.Trigger:
            self.show()

    def on_click(self):
        second = int(self.second.text()) if self.second.text() else 0
        message_text = self.message.text() if self.message.text() else "Иди гуляй!"
        self.message_timer.start(second * 1000)
        self.countdown_timer.start(1000)
        self.tray_icon.update_tooltip(f"Следующее сообщение через {second} секунд")
        self.tray_icon.setIcon(QtGui.QIcon("icon.png"))

    def show_message(self):
        message_text = self.message.text() if self.message.text() else "Иди гуляй!"
        ctypes.windll.user32.MessageBoxW(0, message_text, "Сообщение", 1)

    def update_countdown(self):
        remaining_time = self.message_timer.remainingTime() // 1000
        self.timer_label.setText(f"Следующее сообщение через {remaining_time} секунд")
        self.tray_icon.update_tooltip(f"Следующее сообщение через {remaining_time} секунд")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    icon_path = "icon.png"
    if not QtGui.QIcon.hasThemeIcon(icon_path):
        icon_path = QtGui.QIcon.fromTheme(icon_path)
    app.setWindowIcon(QtGui.QIcon(icon_path))

    ex = App()
    sys.exit(app.exec())
