from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QVBoxLayout, QLabel, QSizePolicy
import sys
import pygame
# later call funcs from other file
from joystick import startJoystick

# for plot styling
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Python GUI - plot motor controls

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
        self.DrawAxes()

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
        # updates the joystick position on the plot
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
        
        # init joystick
        self.joystick = startJoystick()
        self.x_val = -999
        self.y_val = -999
        
        title = QLabel("Right Joystick")
        title.setStyleSheet("font-size: 20px; color: #8888cc; padding-bottom: 6px;")

        self.status_label = QLabel(self.joystickStatus())
        self.status_label.setStyleSheet("font-size: 18px; color: #5555aa; padding-bottom: 4px;")

        self.coord_label = QLabel("X: tbd   Y: tbd")
        self.coord_label.setStyleSheet("font-size: 18px; color: #aaaacc; padding-bottom: 8px;")

        # make joystick plot
        self.joystick_plot = JoystickPlot()
        self.joystick_plot.setMinimumSize(480, 480)

        # layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(24, 16, 24, 16)
        main_layout.setSpacing(4)

        # add widgets
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

        # poll joystick at ~60 Hz
        self.timer = QTimer()
        self.timer.timeout.connect(self.pollJoystick)
        self.timer.start(16)

    def joystickStatus(self):
        if self.joystick:
            return f"Controller: {self.joystick.get_name()}"
        return "no controller"

    def pollJoystick(self):
        
        # start processing controls
        pygame.event.pump()

        # reconnect if none
        if self.joystick is None:
            self.joystick = startJoystick()
            self.status_label.setText(self.joystickStatus())

        try:
            # get axes (right joystick only)
            x = self.joystick.get_axis(3)
            y = -self.joystick.get_axis(4)
            print(x,y)

            # dead threshold
            dead_zone = 0.05
            x = x if abs(x) > dead_zone else 0.0
            y = y if abs(y) > dead_zone else 0.0

            # update plot position and coordinates
            self.joystick_plot.UpdatePosition(x, y)
            self.coord_label.setText(f"X: {x:+.3f}   Y: {y:+.3f}")

        # disconnect if any errors
        except Exception:
            self.joystick = None
            self.status_label.setText("Controller: Disconnected")
        
# run the app
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainInterface()
    window.show()

    app.exec()


        
        
        
