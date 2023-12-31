import sys
from PyQt5 import QtWidgets, uic, QtWidgets, QtGui

qtcreator_file  = "./gui/gui_qt.ui" # Enter file here.
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtcreator_file)


class QTCPUDisplay(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

    def init_gui(self, registers: dict, step_function):
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.show()
        self.step_button.clicked.connect(lambda: step_function())
        self.setWindowTitle("CPU debugger")

        self.label_a.setText(f"A\nValue: {registers['A']}")
        self.label_b.setText(f"B\nValue: {registers['B']}")
        self.label_c.setText(f"C\nValue: {registers['C']}")
        self.label_d.setText(f"D\nValue: {registers['D']}")
        self.label_e.setText(f"E\nValue: {registers['E']}")
        self.label_h.setText(f"H\nValue: {registers['H']}")
        self.label_l.setText(f"L\nValue: {registers['L']}")

        self.label_z.setText(f"Z\nValue: {registers['Z']}")
        self.label_s.setText(f"S\nValue: {registers['S']}")
        self.label_hc.setText(f"HC\nValue: {registers['HC']}")
        self.label_carry.setText(f"Cx\nValue: {registers['CR']}")
        self.label_sp.setText(f"SP\nValue: {registers['SP']}")
        self.label_pc.setText(f"PC\nValue: {registers['PC']}")


    def update_registers(self, registers:dict):
        self.label_a.setText(f"A\nValue: {registers['A']}")
        self.label_b.setText(f"B\nValue: {registers['B']}")
        self.label_c.setText(f"C\nValue: {registers['C']}")
        self.label_d.setText(f"D\nValue: {registers['D']}")
        self.label_e.setText(f"E\nValue: {registers['E']}")
        self.label_h.setText(f"H\nValue: {registers['H']}")
        self.label_l.setText(f"L\nValue: {registers['L']}")

        self.label_z.setText(f"Z\nValue: {registers['Z']}")
        self.label_s.setText(f"S\nValue: {registers['S']}")
        self.label_hc.setText(f"HC\nValue: {registers['HC']}")
        self.label_carry.setText(f"Cx\nValue: {registers['CR']}")
        self.label_sp.setText(f"SP\nValue: {registers['SP']}")
        self.label_pc.setText(f"PC\nValue: {registers['PC']}")
        self.update()

    def insert_instruction(self, instruction: str, address: str, opcode: str, isImplemented: bool):
        rowPosition = self.instructions_table.rowCount()
        self.instructions_table.insertRow(rowPosition)

        # Creating columns and setting their color
        if not isImplemented:
            brush = QtGui.QBrush(QtGui.QColor(207, 77, 68))
        else:
            brush = QtGui.QBrush(QtGui.QColor(84, 71, 70))
        instruction_column = QtWidgets.QTableWidgetItem(instruction)
        instruction_column.setForeground(brush)
        address_column = QtWidgets.QTableWidgetItem(address)
        address_column.setForeground(brush)
        opcode_column = QtWidgets.QTableWidgetItem(opcode)
        opcode_column.setForeground(brush)

        self.instructions_table.setItem(rowPosition , 0, instruction_column)
        self.instructions_table.setItem(rowPosition , 1, address_column)
        self.instructions_table.setItem(rowPosition , 2, opcode_column)
        self.instructions_table.scrollToBottom()
        self.update()
