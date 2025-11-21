# guests.py
import os
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import (
    QApplication,
    QDataWidgetMapper,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
    QStyledItemDelegate,
    QMessageBox
)

# =======================================================
# KONEKSI DATABASE
# =======================================================
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("reservasi-hotel.sqlite")
if not db.open():
    raise RuntimeError("Gagal membuka database 'reservasi-hotel.sqlite'")

# =======================================================
# CRUD GUESTS WINDOW
# =======================================================
class GuestsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form = QFormLayout()

        # INPUT FIELDS
        self.guest_id = QSpinBox()
        self.guest_id.setRange(0, 999999)
        self.guest_id.setDisabled(True)

        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.address = QLineEdit()

        # FORM
        form.addRow("Guest ID", self.guest_id)
        form.addRow("Name", self.name)
        form.addRow("Phone", self.phone)
        form.addRow("Address", self.address)

        # MODEL
        self.model = QSqlTableModel(db=db)
        self.model.setTable("guests")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()

        # DATA MAPPER
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QStyledItemDelegate())

        # mapping sesuai urutan kolom: guest_id(0), name(1), phone(2), address(3)
        self.mapper.addMapping(self.guest_id, 0)
        self.mapper.addMapping(self.name, 1)
        self.mapper.addMapping(self.phone, 2)
        self.mapper.addMapping(self.address, 3)

        self.mapper.toFirst()

        # BUTTONS
        controls = QHBoxLayout()

        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self.mapper.toPrevious)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.mapper.toNext)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)

        add_btn = QPushButton("Add New Guest")
        add_btn.clicked.connect(self.add_new_guest)

        controls.addWidget(prev_btn)
        controls.addWidget(next_btn)
        controls.addWidget(save_btn)
        controls.addWidget(add_btn)

        layout.addLayout(form)
        layout.addLayout(controls)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("CRUD Guests")
        self.setMinimumSize(QSize(500, 300))

    # SAVE
    def save_data(self):
        # ensure mapper data pushed to model
        if not self.mapper.submit():
            QMessageBox.warning(self, "Warning", "Gagal submit mapper")
            return

        if self.model.submitAll():
            print("Guest saved successfully!")
            self.model.select()
        else:
            QMessageBox.critical(self, "ERROR", self.model.lastError().text())
            self.model.revertAll()

    # ADD NEW GUEST
    def add_new_guest(self):
        row = self.model.rowCount()
        # insert a new row
        if not self.model.insertRow(row):
            QMessageBox.critical(self, "ERROR", "Gagal memasukkan baris baru")
            return

        # set some default values (optional)
        self.model.setData(self.model.index(row, 1), "")  # name
        self.model.setData(self.model.index(row, 2), "")  # phone
        self.model.setData(self.model.index(row, 3), "")  # address

        # commit immediately so autoincrement id is generated and visible
        if not self.model.submitAll():
            QMessageBox.critical(self, "ERROR", f"Gagal menyimpan data baru: {self.model.lastError().text()}")
            self.model.revertAll()
            return

        # refresh and move mapper to last (so ID shows)
        self.model.select()
        self.mapper.setCurrentIndex(row)
        self.mapper.toLast()


# MAIN
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuestsWindow()
    window.show()
    app.exec()
