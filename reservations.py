# reservations.py
import os
import sys
import sqlite3

from PyQt6.QtCore import QSize
from PyQt6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
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
# WINDOW CRUD RESERVATIONS
# =======================================================
class ReservationsWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        form = QFormLayout()

        # FIELDS
        self.reservation_id = QSpinBox()
        self.reservation_id.setRange(0, 9999999)
        self.reservation_id.setDisabled(True)

        # Guest List (ComboBox)
        self.guest_id = QComboBox()
        self.load_guests()

        # Room List (ComboBox)
        self.room_id = QComboBox()
        self.load_rooms()

        # Check-in / Check-out
        self.check_in = QLineEdit()
        self.check_in.setPlaceholderText("YYYY-MM-DD")

        self.check_out = QLineEdit()
        self.check_out.setPlaceholderText("YYYY-MM-DD")

        # Total Price
        self.total_price = QSpinBox()
        self.total_price.setRange(0, 999999999)

        # FORM
        form.addRow("Reservation ID", self.reservation_id)
        form.addRow("Guest", self.guest_id)
        form.addRow("Room", self.room_id)
        form.addRow("Check-in", self.check_in)
        form.addRow("Check-out", self.check_out)
        form.addRow("Total Price", self.total_price)

        # MODEL
        self.model = QSqlTableModel(db=db)
        self.model.setTable("reservations")
        self.model.setEditStrategy(QSqlTableModel.EditStrategy.OnManualSubmit)
        self.model.select()

        # DATA MAPPER
        self.mapper = QDataWidgetMapper()
        self.mapper.setModel(self.model)
        self.mapper.setItemDelegate(QStyledItemDelegate())  # IMPORTANT!

        # Map only widgets that can be filled automatically:
        # reservation_id(0), check_in(3), check_out(4), total_price(5)
        self.mapper.addMapping(self.reservation_id, 0)
        self.mapper.addMapping(self.check_in, 3)
        self.mapper.addMapping(self.check_out, 4)
        self.mapper.addMapping(self.total_price, 5)

        # Do NOT map guest_id/room_id directly; we'll sync them manually
        self.mapper.toFirst()
        self.mapper.currentIndexChanged.connect(self._on_index_changed)
        self._on_index_changed(self.mapper.currentIndex())

        # BUTTONS
        controls = QHBoxLayout()

        prev_btn = QPushButton("Previous")
        prev_btn.clicked.connect(self.mapper.toPrevious)

        next_btn = QPushButton("Next")
        next_btn.clicked.connect(self.mapper.toNext)

        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_data)

        add_btn = QPushButton("Add New Reservation")
        add_btn.clicked.connect(self.add_new_reservation)

        controls.addWidget(prev_btn)
        controls.addWidget(next_btn)
        controls.addWidget(save_btn)
        controls.addWidget(add_btn)

        # FINAL LAYOUT
        layout.addLayout(form)
        layout.addLayout(controls)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.setWindowTitle("CRUD Reservations - Hotel Reservation System")
        self.setMinimumSize(QSize(550, 350))

    # LOAD GUEST LIST
    def load_guests(self):
        self.guest_id.clear()
        query = QSqlQuery("SELECT guest_id, name FROM guests ORDER BY guest_id ASC")
        while query.next():
            guest_id = query.value(0)
            name = query.value(1)
            self.guest_id.addItem(name, guest_id)

    # LOAD ROOM LIST
    def load_rooms(self):
        self.room_id.clear()
        query = QSqlQuery("SELECT room_id, room_number FROM rooms ORDER BY room_id ASC")
        while query.next():
            room_id = query.value(0)
            room_number = query.value(1)
            self.room_id.addItem(room_number, room_id)

    # when mapper moves, sync combo boxes from model values
    def _on_index_changed(self, idx):
        if idx < 0 or idx >= self.model.rowCount():
            return
        # fetch guest_id and room_id from model
        guest_val = self.model.data(self.model.index(idx, 1))
        room_val = self.model.data(self.model.index(idx, 2))

        # set current index of combo by finding itemData
        found_g = -1
        for i in range(self.guest_id.count()):
            if self.guest_id.itemData(i) == guest_val:
                found_g = i
                break
        if found_g >= 0:
            self.guest_id.setCurrentIndex(found_g)

        found_r = -1
        for i in range(self.room_id.count()):
            if self.room_id.itemData(i) == room_val:
                found_r = i
                break
        if found_r >= 0:
            self.room_id.setCurrentIndex(found_r)

        # also ensure check_in/check_out/price displayed via mapper (mapper handles them)

    # SAVE DATA
    def save_data(self):
        # push mapped widgets (check_in, check_out, total_price, etc)
        if not self.mapper.submit():
            QMessageBox.warning(self, "Warning", "Gagal submit mapper")
            return

        cur = self.mapper.currentIndex()
        if cur < 0:
            QMessageBox.warning(self, "Warning", "Tidak ada baris aktif")
            return

        # write combo values into model before submit
        guest_data = self.guest_id.currentData()
        room_data = self.room_id.currentData()
        self.model.setData(self.model.index(cur, 1), guest_data)
        self.model.setData(self.model.index(cur, 2), room_data)

        # attempt to commit
        if self.model.submitAll():
            print("Reservation saved successfully!")
            # refresh guest/room lists (in case they changed)
            self.model.select()
            self.load_guests()
            self.load_rooms()
            # re-sync combo selections
            self._on_index_changed(cur)
        else:
            QMessageBox.critical(self, "ERROR", self.model.lastError().text())
            self.model.revertAll()

    # ADD NEW RESERVATION
    def add_new_reservation(self):
        row = self.model.rowCount()
        if not self.model.insertRow(row):
            QMessageBox.critical(self, "ERROR", "Gagal menambah reservasi")
            return

        # set some sensible defaults: guest -> first, room -> first, checkin today-ish, price 0
        if self.guest_id.count() > 0:
            self.model.setData(self.model.index(row, 1), self.guest_id.itemData(0))
        if self.room_id.count() > 0:
            self.model.setData(self.model.index(row, 2), self.room_id.itemData(0))
        self.model.setData(self.model.index(row, 3), "")  # check_in
        self.model.setData(self.model.index(row, 4), "")  # check_out
        self.model.setData(self.model.index(row, 5), 0)   # total_price

        # commit immediately so autoincrement id is generated
        if not self.model.submitAll():
            QMessageBox.critical(self, "ERROR", f"Gagal menyimpan reservasi baru: {self.model.lastError().text()}")
            self.model.revertAll()
            return

        # refresh and move to last so ID appears
        self.model.select()
        self.mapper.setCurrentIndex(row)
        self.mapper.toLast()
        # reload combo lists and sync
        self.load_guests()
        self.load_rooms()
        self._on_index_changed(row)


# =======================================================
# MAIN PROGRAM
# =======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReservationsWindow()
    window.show()
    app.exec()
