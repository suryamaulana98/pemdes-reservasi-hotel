# main.py
import sys
import sqlite3
from PyQt6.QtCore import QSize
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QPushButton,
    QTableView,
    QVBoxLayout,
    QMainWindow,
    QWidget,
    QLineEdit,
    QLabel
)

# =======================================================
# AUTO CREATE DATABASE + TABLE + DATA DUMMY
# =======================================================
def init_database():
    conn = sqlite3.connect("reservasi-hotel.sqlite")
    cursor = conn.cursor()
    

    # TABLE rooms
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rooms (
        room_id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number TEXT NOT NULL,
        room_type TEXT NOT NULL,
        price INTEGER NOT NULL,
        status TEXT DEFAULT 'Available'
    )
    """)

    # TABLE guests
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS guests (
        guest_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT,
        address TEXT
    )
    """)

    # TABLE reservations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reservations (
        reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_id INTEGER NOT NULL,
        room_id INTEGER NOT NULL,
        check_in TEXT NOT NULL,
        check_out TEXT NOT NULL,
        total_price INTEGER NOT NULL,
        created_at TEXT DEFAULT (datetime('now')),
        FOREIGN KEY (guest_id) REFERENCES guests(guest_id),
        FOREIGN KEY (room_id) REFERENCES rooms(room_id)
    )
    """)
    
    # hapus sqlite_sequence supaya autoincrement mulai dari 1 lagi
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='guests'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='rooms'")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='reservations'")


    # Insert rooms dummy (5 data)
    cursor.execute("SELECT COUNT(*) FROM rooms")
    if cursor.fetchone()[0] == 0:
        rooms_dummy = [
            ("101", "Standard", 200000, "Available"),
            ("102", "Deluxe", 350000, "Available"),
            ("201", "Suite", 500000, "Available"),
            ("202", "Standard", 200000, "Available"),
            ("203", "Deluxe", 350000, "Available")
        ]
        cursor.executemany(
            "INSERT INTO rooms (room_number, room_type, price, status) VALUES (?, ?, ?, ?)",
            rooms_dummy
        )

    # Insert guests dummy (5 data)
    cursor.execute("SELECT COUNT(*) FROM guests")
    if cursor.fetchone()[0] == 0:
        guests_dummy = [
            ("Andi", "08123456789", "Surabaya"),
            ("Budi", "082233445566", "Sidoarjo"),
            ("Citra", "08199887766", "Gresik"),
            ("Dewi", "083112233445", "Lamongan"),
            ("Eko", "089911223344", "Malang")
        ]
        cursor.executemany(
            "INSERT INTO guests (name, phone, address) VALUES (?, ?, ?)",
            guests_dummy
        )

    # Insert reservation dummy (5 data)
    cursor.execute("SELECT COUNT(*) FROM reservations")
    if cursor.fetchone()[0] == 0:
        reserv_dummy = [
            (1, 1, "2025-02-01", "2025-02-03", 400000),
            (2, 2, "2025-03-10", "2025-03-12", 700000),
            (3, 3, "2025-04-05", "2025-04-07", 1000000),
            (4, 4, "2025-05-01", "2025-05-04", 600000),
            (5, 5, "2025-06-02", "2025-06-03", 350000)
        ]
        cursor.executemany(
            "INSERT INTO reservations (guest_id, room_id, check_in, check_out, total_price) VALUES (?, ?, ?, ?, ?)",
            reserv_dummy
        )

    conn.commit()
    conn.close()


# =======================================================
# CALL INIT DATABASE
# =======================================================
init_database()


# =======================================================
# IMPORT WINDOWS
# =======================================================
from rooms import RoomsWindow
from guests import GuestsWindow
from reservations import ReservationsWindow


# =======================================================
# PYQT DATABASE CONNECTION
# =======================================================
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName("reservasi-hotel.sqlite")
if not db.open():
    raise RuntimeError("Gagal membuka database 'reservasi-hotel.sqlite'")

# =======================================================
# MAIN WINDOW
# =======================================================
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        container = QWidget()
        layout = QVBoxLayout()

        # ============================
        # FILTER PENCARIAN (2 Kolom)
        # ============================
        filter_layout = QHBoxLayout()

        self.filter_guest = QLineEdit()
        self.filter_guest.setPlaceholderText("Cari Nama Penginap...")
        self.filter_guest.textChanged.connect(self.load_reservation_data)

        self.filter_room = QLineEdit()
        self.filter_room.setPlaceholderText("Cari Nomor Kamar...")
        self.filter_room.textChanged.connect(self.load_reservation_data)

        filter_layout.addWidget(QLabel("Filter:"))
        filter_layout.addWidget(self.filter_guest)
        filter_layout.addWidget(self.filter_room)

        layout.addLayout(filter_layout)

        # ============================
        # TABLE RESERVASI
        # ============================
        self.table = QTableView()
        self.model = QSqlQueryModel()

        self.load_reservation_data()
        layout.addWidget(self.table)

        # ============================
        # BUTTON NAV MENU
        # ============================
        btn_layout = QHBoxLayout()

        btn_rooms = QPushButton("Manage Rooms")
        btn_rooms.clicked.connect(self.open_rooms)

        btn_guests = QPushButton("Manage Guests")
        btn_guests.clicked.connect(self.open_guests)

        btn_res = QPushButton("Manage Reservations")
        btn_res.clicked.connect(self.open_reservations)

        btn_refresh = QPushButton("Refresh Data")
        btn_refresh.clicked.connect(self.refresh_button_clicked)


        btn_layout.addWidget(btn_rooms)
        btn_layout.addWidget(btn_guests)
        btn_layout.addWidget(btn_res)
        btn_layout.addWidget(btn_refresh)

        layout.addLayout(btn_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)
        self.setWindowTitle("Hotel Reservation System - Home")
        self.setMinimumSize(QSize(900, 550))

    # ====================================================================================
    # LOAD TABLE DENGAN FILTER
    # ====================================================================================
    def refresh_button_clicked(self):
        self.filter_guest.clear()
        self.filter_room.clear()
        self.load_reservation_data()

    def load_reservation_data(self):

        guest_filter = self.filter_guest.text()
        room_filter = self.filter_room.text()

        sql = f"""
            SELECT 
                reservations.reservation_id AS 'ID',
                guests.name AS 'Nama Penginap',
                rooms.room_number AS 'No Kamar',
                rooms.room_type AS 'Jenis Kamar',
                reservations.check_in AS 'Check-in',
                reservations.check_out AS 'Check-out',
                reservations.total_price AS 'Total Harga'
            FROM reservations
            INNER JOIN guests ON reservations.guest_id = guests.guest_id
            INNER JOIN rooms ON reservations.room_id = rooms.room_id
            WHERE guests.name LIKE :guest
            AND rooms.room_number LIKE :room
            ORDER BY reservations.reservation_id ASC
        """

        # FIX: reset model dulu supaya refresh benar-benar terjadi
        self.model.clear()
        self.model.setQuery(QSqlQuery())   # flush

        query = QSqlQuery()
        query.prepare(sql)
        query.bindValue(":guest", f"%{guest_filter}%")
        query.bindValue(":room", f"%{room_filter}%")
        query.exec()

        self.model.setQuery(query)

        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()


    def open_rooms(self):
        self.rooms_window = RoomsWindow()
        self.rooms_window.show()

    def open_guests(self):
        self.guests_window = GuestsWindow()
        self.guests_window.show()

    def open_reservations(self):
        self.res_window = ReservationsWindow()
        self.res_window.show()


# =======================================================
# RUN PROGRAM
# =======================================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
