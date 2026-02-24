import serial
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QSizePolicy
import sys
import pyqtgraph as pg
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from joystick import startJoystick, monitorJoystick

# GUI - visualize motor controls


# design the main window
class JoystickPlot(QWidget):
    def __init__(self):
        super().__init__()
        
        # coordinates
        self.x_val = 0.0
        self.y_val = 0.0

        # setup fig
        self.figure = Figure(figsize=(5, 5), facecolor="#1a1a2e")
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.ax = self.figure.add_subplot(111)
        self._setup_axes()

        # dot
        (self.dot,) = self.ax.plot(0, 0, "o", color="#e94560", markersize=14, zorder=5)

        # make dot easier to see
        self.hline = self.ax.axhline(0, color="#e94560", linewidth=0.6, alpha=0.4, zorder=4)
        self.vline = self.ax.axvline(0, color="#e94560", linewidth=0.6, alpha=0.4, zorder=4)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def DrawAxes(self):
        ax = self.ax
        ax.set_facecolor("#0f0f23")
        ax.set_xlim(-1.1, 1.1)
        ax.set_ylim(-1.1, 1.1)
        ax.set_aspect("equal")

        # Grid
        ax.grid(True, color="#2a2a4a", linewidth=0.8, linestyle="--", zorder=1)
        ax.set_xticks([-1, -0.5, 0, 0.5, 1])
        ax.set_yticks([-1, -0.5, 0, 0.5, 1])
        ax.tick_params(colors="#8888aa", labelsize=9)
        for spine in ax.spines.values():
            spine.set_edgecolor("#3a3a5c")

        # Bold axes at 0
        ax.axhline(0, color="#4a4a7a", linewidth=1.2, zorder=2)
        ax.axvline(0, color="#4a4a7a", linewidth=1.2, zorder=2)

        # Labels
        ax.set_xlabel("X", color="#aaaacc", fontsize=11)
        ax.set_ylabel("Y", color="#aaaacc", fontsize=11)

        # Boundary circle
        theta = [i * 2 * 3.14159 / 200 for i in range(201)]
        ax.plot([0.999 * __import__("math").cos(t) for t in theta],
                [0.999 * __import__("math").sin(t) for t in theta],
                color="#3a3a6a", linewidth=1, linestyle=":", zorder=3)

        self.figure.tight_layout()

    def UpdatePosition(self, x, y):
        """Call this with new joystick x/y values in range [-1, 1]."""
        self.x_val = x
        self.y_val = y
        self.dot.set_data([x], [y])
        self.hline.set_ydata([y])
        self.vline.set_xdata([x])
        self.canvas.draw_idle()
        

class MainInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # global gui things
        self.setMinimumSize(QSize(800, 800))
        self.setWindowTitle("Giant Murder Tarantula")
        global_title = QLabel("GMT Hexapod Controls")
        global_title.setStyleSheet("font-size: 40px;")
        
        
        # set central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # joystick
        joystick = startJoystick()
        self.x_val = -999
        self.y_val = -999
        
        title = QLabel("Right Joystick")
        title.setStyleSheet("font-size: 18px; color: #8888cc; padding-bottom: 6px;")

        self.status_label = QLabel(self._joystick_status())
        self.status_label.setStyleSheet("font-size: 13px; color: #5555aa; padding-bottom: 4px;")

        self.coord_label = QLabel("X: 0.000   Y: 0.000")
        self.coord_label.setStyleSheet("font-size: 14px; color: #aaaacc; padding-bottom: 8px;")

        # Joystick plot widget
        self.joystick_plot = JoystickPlot()
        self.joystick_plot.setMinimumSize(480, 480)

        # Layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 16, 24, 16)
        main_layout.setSpacing(4)

        main_layout.addWidget(global_title)
        main_layout.addWidget(title)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.coord_label)
        main_layout.addWidget(self.joystick_plot)
        main_layout.addStretch()
        
        main_layout.addWidget(global_title)
        main_layout.addStretch()
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Poll joystick at ~60 Hz
        self.timer = QTimer()
        self.timer.timeout.connect(self.pollJoystick)
        self.timer.start(16)

    def joystickStatus(self):
        if self.joystick:
            return f"Controller: {self.joystick.get_name()}"
        return "Controller: Not connected — plug in and restart"

    def pollJoystick(self):

        # Try to reconnect if disconnected
        if self.joystick is None:
            self._try_connect_joystick()
            self.status_label.setText(self._joystick_status())
            return

        try:
            # Right joystick is typically axes 2 (X) and 3 (Y) on most gamepads.
            # Adjust axis indices for your specific controller if needed.
            num_axes = self.joystick.get_numaxes()
            x = self.joystick.get_axis(2) if num_axes > 2 else 0.0
            y = -self.joystick.get_axis(3) if num_axes > 3 else 0.0  # invert Y so up = positive

            # # Dead zone
            # dead_zone = 0.05
            # x = x if abs(x) > dead_zone else 0.0
            # y = y if abs(y) > dead_zone else 0.0

            self.joystick_plot.update_position(x, y)
            self.coord_label.setText(f"X: {x:+.3f}   Y: {y:+.3f}")

        except Exception:
            self.joystick = None
            self.status_label.setText("Controller: Disconnected")
        


        



# run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainInterface()
    window.show()

    app.exec()


        
        
        