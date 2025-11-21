# rooms.py
import os
import sys
import sqlite3

from PyQt6.QtCore import QSize
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel
from PyQt6.QtWidgets import (
    QApplication,
    QComboBox,
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
# WINDOW CRUD ROOMS
# =======================================================
class RoomsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form = QFormLayout()

        # Widgets
        self.room_id = QSpinBox()
        self.room_id.setRange(0, 999999)
        self.room_id.setDisabled(True)

        self.room_number = QLineEdit()
        self.room_type = QComboBox()
        self.room_type.addItems(["Standard", "Deluxe", "Suite"])

        self.price = QSpinBox()
        self.price.setRange(0, 999999999)

        self.status = QComboBox()
        self.status.addItems(["Available", "Occupied"])

        # Form
        form.addRow(QLabel("Room ID"), self.room_id)
        form.addRow(QLabel("Room Number"), self.room_number)
        form.addRow(QLabel("Room Type"), self.room_type)
        form.addRow(QLabel("Price Per Night"), self.price)
        form.addRow(QLabel("Status"), self.status)

        # Model
        self.model = QSqlTableModel(db=db)
        self.model.setTable("rooms")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()

        # Data Mapper
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QStyledItemDelegate())

        # mapping sesuai urutan kolom: room_id(0), room_number(1), room_type(2), price(3), status(4)
        self.mapper.addMapping(self.room_id, 0)
        self.mapper.addMapping(self.room_number, 1)
        # For combo boxes (room_type and status) mapping to index is okay if values are text,
        # but better to use setCurrentText when mapper index changes.
        self.mapper.addMapping(self.price, 3)
        # we will manage room_type and status separately in slot
        self.mapper.toFirst()
        self.mapper.currentIndexChanged.connect(self._on_mapper_index_changed)
        self._on_mapper_index_changed(self.mapper.currentIndex())

        # Controls
        controls = QHBoxLayout()

        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self.mapper.toPrevious)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.mapper.toNext)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)

        add_btn = QPushButton("Add New Room")
        add_btn.clicked.connect(self.add_new_room)

        controls.addWidget(prev_btn)
        controls.addWidget(next_btn)
        controls.addWidget(save_btn)
        controls.addWidget(add_btn)

        layout.addLayout(form)
        layout.addLayout(controls)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("CRUD Rooms - Hotel Reservation")
        self.setMinimumSize(QSize(500, 350))

    # when mapper index changes, update combo boxes from model
    def _on_mapper_index_changed(self, idx):
        if idx < 0 or idx >= self.model.rowCount():
            return
        room_type_val = self.model.data(self.model.index(idx, 2))  # room_type column
        status_val = self.model.data(self.model.index(idx, 4))     # status column
        if room_type_val is not None:
            self.room_type.setCurrentText(str(room_type_val))
        if status_val is not None:
            self.status.setCurrentText(str(status_val))

    # =============================
    # SIMPAN PERUBAHAN
    # =============================
    def save_data(self):
        # push mapper fields to model
        if not self.mapper.submit():
            QMessageBox.warning(self, "Warning", "Gagal submit mapper")
            return

        # write combo fields into model
        cur = self.mapper.currentIndex()
        if cur >= 0:
            self.model.setData(self.model.index(cur, 2), self.room_type.currentText())
            self.model.setData(self.model.index(cur, 4), self.status.currentText())

        if self.model.submitAll():
            print("Room saved successfully!")
            self.model.select()
        else:
            QMessageBox.critical(self, "ERROR", self.model.lastError().text())
            self.model.revertAll()

    # =============================
    # TAMBAH ROOM BARU
    # =============================
    def add_new_room(self):
        row = self.model.rowCount()
        if not self.model.insertRow(row):
            QMessageBox.critical(self, "ERROR", "Gagal menambah baris")
            return

        # default values
        self.model.setData(self.model.index(row, 1), "")  # room_number
        self.model.setData(self.model.index(row, 2), "Standard")
        self.model.setData(self.model.index(row, 3), 0)
        self.model.setData(self.model.index(row, 4), "Available")

        # commit immediately so id generates
        if not self.model.submitAll():
            QMessageBox.critical(self, "ERROR", f"Gagal menyimpan data baru: {self.model.lastError().text()}")
            self.model.revertAll()
            return

        self.model.select()
        self.mapper.setCurrentIndex(row)
        self.mapper.toLast()


# =======================================================
# MAIN
# =======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RoomsWindow()
    window.show()
    app.exec()
