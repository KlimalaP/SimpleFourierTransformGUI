import sys
import os
import csv
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import numpy as np
from scipy.io.wavfile import write
import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QAction, QApplication, QLineEdit, QTableWidget, QTableWidgetItem, \
    QSpinBox, QDoubleSpinBox, QFileDialog, QLabel
from PyQt5.QtGui import QIcon


class Generator():
    def __init__(self, timeRange, timeStep):
        self.timeRange = timeRange
        self.timeStep = timeStep
        self.t = np.linspace(0, timeRange, timeStep)

    def Sinus(self, f, A):
        return A * np.sin(2 * np.pi * f * self.t)

    def Draw(self, t, y, A, n):
        plt.xlim(0, self.timeRange)
        plt.ylim(-1.1 * A, 1.1 * A)
        # plt.plot(takeValue.t, y)
        plt.show()
        scaled = np.int16(y * 32767)
        write(n + '.wav', 44100, scaled)

    def Squere(self, f, A):
        return A * np.sign(np.sin(2 * np.pi * f * self.t))

    def Sawtooth(self, f, A):
        return (2 * A / np.pi) * np.arctan(np.tan(2 * np.pi * f * self.t))

    def Triangle(self, f, A):
        return ((2 * A) / (np.pi)) * (np.arcsin(np.sin(2 * np.pi * f * self.t)))

    def WhiteNoise(self, t, A):
        return A * (2 * np.random.rand(len(self.t)) - 1)

    def DrawTranformataFouriera(self, t, y, n):
        N = len(t)
        dt = t[1] - t[0]
        yf = 2.0 / N * np.abs(fft(y)[0:N // 2])
        xf = np.fft.fftfreq(N, d=dt)[0:N // 2]
        plt.plot(xf, yf)
        plt.xlim(0, 3000) 
        plt.grid()
        plt.show()
        df = pd.DataFrame({"t": xf, "A": yf})
        df.to_csv(n + ".csv", index=False, sep='\t')


class App(QMainWindow, QWidget):
    def __init__(self):
        super().__init__()

        self.setup_application_window()
        self.setup_table_widget()
        self.setup_application_parameter_boxes()
        self.setup_menu_bar()

        self.show()

    def setup_table_widget(self):
        self.table = QTableWidget(self)
        # setup proper position
        self.table.move(100, 200)
        self.table.resize(300, 200)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(['wektor', 'wartosc'])

    def setup_menu_bar(self):
        self.setup_file_options()
        self.setup_calculate_options()

    def setup_calculate_options(self):
        calculate = self.menuBar().addMenu("Calculate")

        # todo implement functions
        sine = QAction("sine", self)
        sine.triggered.connect(lambda: self.calculate_sinus())
        calculate.addAction(sine)

        square = QAction("square", self)
        square.triggered.connect(lambda: self.calculate_square())
        calculate.addAction(square)

        triangle = QAction("triangle", self)
        triangle.triggered.connect(lambda: self.calculate_triangle())
        calculate.addAction(triangle)

        saw_tooth = QAction("sawtooth", self)
        saw_tooth.triggered.connect(lambda: self.calculate_saw_tooth())
        calculate.addAction(saw_tooth)

        white_noise = QAction("white noise", self)
        white_noise.triggered.connect(lambda: self.calculate_white_noise())
        calculate.addAction(white_noise)

    def setup_file_options(self):
        file = self.menuBar().addMenu("File")

        save = QAction("Save", self)
        save.triggered.connect(self.save_to_file)
        file.addAction(save)

        exit = QAction("Exit", self)
        exit.triggered.connect(self.exit_program)
        file.addAction(exit)

    def setup_application_window(self):
        self.left = 100
        self.top = 100
        self.width = 500
        self.height = 500
        self.setGeometry(self.left, self.top, self.width, self.height)

    def setup_application_parameter_boxes(self):
        self.setup_time_range_box()
        self.setup_steps_number_box()
        self.setup_amplitude_box()
        self.setup_frequency_box()

    def setup_time_range_box(self):
        steps_initial_value = 1000000

        labelA = QLabel(self)
        labelA.setText('time range:')
        labelA.move(230, 30)

        self.time_range_box = QDoubleSpinBox(self)
        self.time_range_box.move(350, 30)
        self.time_range_box.setMaximum(1000000000)
        self.time_range_box.setValue(steps_initial_value)

    def setup_steps_number_box(self):
        steps_number_initial_value = 100

        labelA = QLabel(self)
        labelA.setText('steps number:')
        labelA.move(230, 60)

        self.steps_number_box = QSpinBox(self)
        self.steps_number_box.move(350, 60)
        self.steps_number_box.setMaximum(1000000000)
        self.steps_number_box.setValue(steps_number_initial_value)

    def setup_amplitude_box(self):
        amplitude_initial_value = 1

        labelA = QLabel(self)
        labelA.setText('amplitude:')
        labelA.move(230, 90)

        self.amplitude_box = QDoubleSpinBox(self)
        self.amplitude_box.move(350, 90)
        self.amplitude_box.setMaximum(1000000000)
        self.amplitude_box.setValue(amplitude_initial_value)

    def setup_frequency_box(self):
        frequency_initial_value = 440

        labelA = QLabel(self)
        labelA.setText('frequency:')
        labelA.move(230, 120)

        self.frequency_box = QDoubleSpinBox(self)
        self.frequency_box.move(350, 120)
        self.frequency_box.setMaximum(1000000000)
        self.frequency_box.setValue(frequency_initial_value)

    def save_to_file(self):
        options = QFileDialog.Options()
        fileName = QFileDialog.getSaveFileName(self, "QFileDialog.getOpenFileName()", "", options=options)[0]
        print(fileName)
        with open(fileName, "w") as file:
            writer = csv.writer(file)
            writer.writerow(["vector", "value"])
            for row_index in range(0, self.table.rowCount()):
                print("IM in")
                writer.writerow([self.table.item(row_index, 0).text(), self.table.item(row_index, 1).text()])

    def exit_program(self):
        print("info")
        os._exit(0)

    def calculate_sinus(self):
        self.clean_table()

        time_range = self.time_range_box.value()
        steps_number = self.steps_number_box.value()
        amplitude = self.amplitude_box.value()
        frequency = self.frequency_box.value()

        self.table.setRowCount(steps_number)
        generator = Generator(time_range, steps_number)
        values_results = generator.Sinus(frequency, amplitude)
        vector_results = np.linspace(0, time_range, steps_number)
        vector_column_index = 0
        value_column_index = 1
        for row_index in range(0, steps_number):
            self.table.setItem(row_index, vector_column_index, QTableWidgetItem(str(vector_results[row_index])))
            self.table.setItem(row_index, value_column_index, QTableWidgetItem(str(values_results[row_index])))

    def calculate_square(self):
        self.clean_table()

        time_range = self.time_range_box.value()
        steps_number = self.steps_number_box.value()
        amplitude = self.amplitude_box.value()
        frequency = self.frequency_box.value()

        self.table.setRowCount(steps_number)
        generator = Generator(time_range, steps_number)
        values_results = generator.Squere(frequency, amplitude)
        vector_results = np.linspace(0, time_range, steps_number)
        vector_column_index = 0
        value_column_index = 1
        for row_index in range(0, steps_number):
            self.table.setItem(row_index, vector_column_index, QTableWidgetItem(str(vector_results[row_index])))
            self.table.setItem(row_index, value_column_index, QTableWidgetItem(str(values_results[row_index])))

    def calculate_triangle(self):
        self.clean_table()

        time_range = self.time_range_box.value()
        steps_number = self.steps_number_box.value()
        amplitude = self.amplitude_box.value()
        frequency = self.frequency_box.value()

        self.table.setRowCount(steps_number)
        generator = Generator(time_range, steps_number)
        values_results = generator.Triangle(frequency, amplitude)
        vector_results = np.linspace(0, time_range, steps_number)
        vector_column_index = 0
        value_column_index = 1
        for row_index in range(0, steps_number):
            self.table.setItem(row_index, vector_column_index, QTableWidgetItem(str(vector_results[row_index])))
            self.table.setItem(row_index, value_column_index, QTableWidgetItem(str(values_results[row_index])))

    def calculate_saw_tooth(self):
        self.clean_table()

        time_range = self.time_range_box.value()
        steps_number = self.steps_number_box.value()
        amplitude = self.amplitude_box.value()
        frequency = self.frequency_box.value()

        self.table.setRowCount(steps_number)
        generator = Generator(time_range, steps_number)
        values_results = generator.Sawtooth(frequency, amplitude)
        vector_results = np.linspace(0, time_range, steps_number)
        vector_column_index = 0
        value_column_index = 1
        for row_index in range(0, steps_number):
            self.table.setItem(row_index, vector_column_index, QTableWidgetItem(str(vector_results[row_index])))
            self.table.setItem(row_index, value_column_index, QTableWidgetItem(str(values_results[row_index])))

    def calculate_white_noise(self):
        self.clean_table()

        time_range = self.time_range_box.value()
        steps_number = self.steps_number_box.value()
        amplitude = self.amplitude_box.value()
        frequency = self.frequency_box.value()

        self.table.setRowCount(steps_number)
        generator = Generator(time_range, steps_number)
        values_results = generator.WhiteNoise(frequency, amplitude)
        vector_results = np.linspace(0, time_range, steps_number)
        vector_column_index = 0
        value_column_index = 1
        for row_index in range(0, steps_number):
            self.table.setItem(row_index, vector_column_index, QTableWidgetItem(str(vector_results[row_index])))
            self.table.setItem(row_index, value_column_index, QTableWidgetItem(str(values_results[row_index])))

    def clean_table(self):
        self.table.setRowCount(0)


app = QApplication(sys.argv)
ex = App()
app.exec_()
