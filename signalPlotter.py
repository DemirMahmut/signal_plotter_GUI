import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox)

class SignalPlotter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Signal Plotter')
        
        layout = QVBoxLayout()
        
        self.combo = QComboBox(self)
        self.combo.addItem("Sine and Cosine Signals")
        self.combo.addItem("Fourier Series Analysis")
        self.combo.currentIndexChanged.connect(self.change_interface)
        layout.addWidget(self.combo)
        
        self.stacked_layout = QVBoxLayout()
        layout.addLayout(self.stacked_layout)
        
        self.setLayout(layout)
        
        self.create_sine_cosine_interface()
        self.create_fourier_series_interface()
        
        self.change_interface(0)
    
    def create_sine_cosine_interface(self):
        self.sine_cosine_widget = QWidget()
        layout = QVBoxLayout()
        
        self.sine_cosine_inputs = []
        for i in range(3):
            hbox = QHBoxLayout()
            
            label_A = QLabel(f'Signal {i+1} - Amplitude (A):')
            self.input_A = QLineEdit(self)
            hbox.addWidget(label_A)
            hbox.addWidget(self.input_A)
            
            label_f = QLabel(f'Frequency (f):')
            self.input_f = QLineEdit(self)
            hbox.addWidget(label_f)
            hbox.addWidget(self.input_f)
            
            label_theta = QLabel(f'Phase (θ):')
            self.input_theta = QLineEdit(self)
            hbox.addWidget(label_theta)
            hbox.addWidget(self.input_theta)
            
            layout.addLayout(hbox)
            self.sine_cosine_inputs.append((self.input_A, self.input_f, self.input_theta))
        
        self.plot_button = QPushButton('Plot Signals', self)
        self.plot_button.clicked.connect(self.plot_sine_cosine_signals)
        layout.addWidget(self.plot_button)
        
        self.figure, self.axs = plt.subplots(5, 1, figsize=(10, 10))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        
        self.sine_cosine_widget.setLayout(layout)
    
    def create_fourier_series_interface(self):
        self.fourier_series_widget = QWidget()
        layout = QVBoxLayout()
        
        # General coefficients input fields
        general_layout = QHBoxLayout()
        
        label_a0 = QLabel('a0:')
        self.input_a0 = QLineEdit(self)
        general_layout.addWidget(label_a0)
        general_layout.addWidget(self.input_a0)
        
        label_w0 = QLabel('w0:')
        self.input_w0 = QLineEdit(self)
        general_layout.addWidget(label_w0)
        general_layout.addWidget(self.input_w0)
        
        label_T = QLabel('T:')
        self.input_T = QLineEdit(self)
        general_layout.addWidget(label_T)
        general_layout.addWidget(self.input_T)
        
        layout.addLayout(general_layout)
        
        self.fourier_inputs = []
        for i in range(3):
            hbox = QHBoxLayout()
            
            label_ak = QLabel(f'ak (k={i+1}):')
            self.input_ak = QLineEdit(self)
            hbox.addWidget(label_ak)
            hbox.addWidget(self.input_ak)
            
            label_bk = QLabel(f'bk (k={i+1}):')
            self.input_bk = QLineEdit(self)
            hbox.addWidget(label_bk)
            hbox.addWidget(self.input_bk)
            
            layout.addLayout(hbox)
            self.fourier_inputs.append((self.input_ak, self.input_bk))
        
        self.plot_button = QPushButton('Plot Signals', self)
        self.plot_button.clicked.connect(self.plot_fourier_signals)
        layout.addWidget(self.plot_button)
        
        self.figure_fourier, self.axs_fourier = plt.subplots(5, 1, figsize=(10, 10))
        self.canvas_fourier = FigureCanvas(self.figure_fourier)
        layout.addWidget(self.canvas_fourier)
        
        self.fourier_series_widget.setLayout(layout)
    
    def change_interface(self, index):
        for i in reversed(range(self.stacked_layout.count())): 
            self.stacked_layout.itemAt(i).widget().setParent(None)
        
        if index == 0:
            self.stacked_layout.addWidget(self.sine_cosine_widget)
        elif index == 1:
            self.stacked_layout.addWidget(self.fourier_series_widget)
    
    def plot_sine_cosine_signals(self):
        t = np.linspace(0, 1, 1000)
        
        total_sin_signal = np.zeros_like(t)
        total_cos_signal = np.zeros_like(t)
        
        for i, (input_A, input_f, input_theta) in enumerate(self.sine_cosine_inputs):
            A = float(input_A.text())
            f = float(input_f.text())
            theta = float(input_theta.text())
            
            theta_rad = np.deg2rad(theta)
            sin_signal = A * np.sin(2 * np.pi * f * t + theta_rad)
            cos_signal = A * np.cos(2 * np.pi * f * t + theta_rad)
            
            total_sin_signal += sin_signal
            total_cos_signal += cos_signal
            
            self.axs[i].clear()
            self.axs[i].plot(t, sin_signal, label=f'Sin {i+1}')
            self.axs[i].plot(t, cos_signal, label=f'Cos {i+1}')
            self.axs[i].set_title(f'Signal {i+1}')
            self.axs[i].legend()
        
        self.axs[3].clear()
        self.axs[3].plot(t, total_sin_signal, label='Total Sin Signal')
        self.axs[3].set_title('Total Sin Signal')
        self.axs[3].legend()
        
        self.axs[4].clear()
        self.axs[4].plot(t, total_cos_signal, label='Total Cos Signal')
        self.axs[4].set_title('Total Cos Signal')
        self.axs[4].legend()
        
        self.canvas.draw()
    
    def plot_fourier_signals(self):
        T = float(self.input_T.text())
        t = np.linspace(0, T, 1000)
        
        a0 = float(self.input_a0.text())
        w0 = float(self.input_w0.text())
        
        total_signal = a0 / 2 * np.ones_like(t)
        total_sin_signal = np.zeros_like(t)
        total_cos_signal = np.zeros_like(t)
        
        for i, (input_ak, input_bk) in enumerate(self.fourier_inputs):
            k = i + 1
            ak = float(input_ak.text())
            bk = float(input_bk.text())
            
            sin_signal = ak * np.cos(k * w0 * t)
            cos_signal = bk * np.sin(k * w0 * t)
            
            total_sin_signal += sin_signal
            total_cos_signal += cos_signal
            
            self.axs_fourier[i].clear()
            self.axs_fourier[i].plot(t, sin_signal, label=f'Sin {i+1}')
            self.axs_fourier[i].plot(t, cos_signal, label=f'Cos {i+1}')
            self.axs_fourier[i].set_title(f'Signal {i+1}')
            self.axs_fourier[i].legend()
        
        total_signal = total_sin_signal + total_cos_signal + a0 / 2
        
        self.axs_fourier[3].clear()
        self.axs_fourier[3].plot(t, total_sin_signal, label='Total Sin Signal')
        self.axs_fourier[3].set_title('Total Sin Signal')
        self.axs_fourier[3].legend()
        
        self.axs_fourier[4].clear()
        self.axs_fourier[4].plot(t, total_cos_signal, label='Total Cos Signal')
        self.axs_fourier[4].set_title('Total Cos Signal')
        self.axs_fourier[4].legend()
        
        self.axs_fourier[4].plot(t, total_signal, label='Total Signal', linestyle='dashed')
        self.axs_fourier[4].legend()
        
        self.canvas_fourier.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SignalPlotter()
    ex.show()
    sys.exit(app.exec_())
