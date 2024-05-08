import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QMessageBox, QComboBox, QInputDialog
import sqlite3

conn = sqlite3.connect('muzik_enstrumanlari.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS Enstrumanlar (
                    id INTEGER PRIMARY KEY,
                    ad TEXT NOT NULL,
                    stok_miktari INTEGER NOT NULL)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Siparisler (
                    id INTEGER PRIMARY KEY,
                    musteri_id INTEGER NOT NULL,
                    enstruman_ad TEXT NOT NULL,
                    miktar INTEGER NOT NULL)''')

conn.commit()

class AnaPencere(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Muzik Enstrumani Dukkan Yonetimi")
        self.setGeometry(100, 100, 400, 300)
        
        self.enstrumanlar_btn = QPushButton("Enstrumanlar")
        self.siparis_btn = QPushButton("Siparis Kayitlari")
        self.tamam_btn = QPushButton("Rapor Olustur")
        
        self.enstrumanlar_btn.clicked.connect(self.enstrumanlar_ac)
        self.siparis_btn.clicked.connect(self.siparis_ac)
        self.tamam_btn.clicked.connect(self.tamam)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.enstrumanlar_btn)
        vbox.addWidget(self.siparis_btn)
        vbox.addWidget(self.tamam_btn)
        
        self.setLayout(vbox)
        
    def enstrumanlar_ac(self):
        self.enstrumanlar_pencere = Enstrumanlar()
        self.enstrumanlar_pencere.show()
        
    def siparis_ac(self):
        self.siparis_pencere = SiparisPencere()
        self.siparis_pencere.show()
        
    def tamam(self):
        # Enstruman bilgilerini al
        enstrumanlar = ""
        cursor.execute("SELECT ad, stok_miktari FROM Enstrumanlar")
        for row in cursor.fetchall():
            enstrumanlar += f"Enstruman Adi: {row[0]}, \nStok Miktari: {row[1]}\n"

        # Siparis bilgilerini al
        siparisler = ""
        cursor.execute("SELECT id, musteri_id, enstruman_ad, miktar FROM Siparisler")
        for row in cursor.fetchall():
            siparisler += f"Siparis Numarasi: {row[0]}, Musteri ID: {row[1]}, Satilan Enstruman: {row[2]}, Miktar: {row[3]}\n"

        # Enstruman ve siparis bilgilerini goster
        QMessageBox.information(self, "Bilgiler", f"Enstrumanlar:\n{enstrumanlar}\n\nSiparisler:\n{siparisler}")

class Enstrumanlar(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Enstrumanlar")
        self.setGeometry(200, 200, 400, 300)
        
        self.enstruman_ad_label = QLabel("Enstruman Adi:")
        self.enstruman_ad_combo = QComboBox()
        self.enstruman_ad_combo.addItems(["Piyano", "Gitar", "Flut", "Saksafon"])
        
        self.stok_miktari_label = QLabel("Stok Miktari:")
        self.stok_miktari_edit = QLineEdit()
        
        self.stok_sec_btn = QPushButton("Stok Miktari Sec")
        self.stok_sec_btn.clicked.connect(self.stok_miktari_ac)

        self.enstruman_ekle_btn = QPushButton("Enstruman Ekle")
        self.enstruman_ekle_btn.clicked.connect(self.enstruman_ekle)

        self.enstruman_iptal_et_btn = QPushButton("Enstruman Iptal Et")
        self.enstruman_iptal_et_btn.clicked.connect(self.enstruman_iptal_et)

        vbox = QVBoxLayout()
        vbox.addWidget(self.enstruman_ad_label)
        vbox.addWidget(self.enstruman_ad_combo)
        vbox.addWidget(self.stok_miktari_label)
        vbox.addWidget(self.stok_miktari_edit)
        vbox.addWidget(self.stok_sec_btn)
        vbox.addWidget(self.enstruman_ekle_btn)
        vbox.addWidget(self.enstruman_iptal_et_btn)
        
        self.setLayout(vbox)
        
    def stok_miktari_ac(self):
        miktar, ok_pressed = QInputDialog.getInt(self, "Stok Miktari Sec", "Stok Miktari Giriniz (Max 150):", 0, 0, 150)
        if ok_pressed:
           self.stok_miktari_edit.setText(str(miktar))

    def enstruman_ekle(self):
        enstruman_ad = self.enstruman_ad_combo.currentText()
        stok_miktari = int(self.stok_miktari_edit.text())

        cursor.execute("INSERT INTO Enstrumanlar (ad, stok_miktari) VALUES (?, ?)", (enstruman_ad, stok_miktari))
        conn.commit()

        QMessageBox.information(self, "Basarili", "Enstruman kaydedildi.")

    def enstruman_iptal_et(self):
        enstruman_ad = self.enstruman_ad_combo.currentText()

        cursor.execute("DELETE FROM Enstrumanlar WHERE ad = ?", (enstruman_ad,))
        conn.commit()

        QMessageBox.information(self, "Basarili", "Enstruman iptal edildi.")

        self.enstruman_ad_combo.clear()
        self.stok_miktari_edit.clear()

class SiparisPencere(QWidget):
    def __init__(self):
        super().__init__()
        
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Siparis Kayitlari")
        self.setGeometry(400, 400, 400, 300)
        
        self.siparis_no_label = QLabel("Siparis Numarasi:")
        self.siparis_no_edit = QLineEdit()
        
        self.enstrumanlar_label = QLabel("Satin Almak Istediginiz Enstruman:")
        self.enstrumanlar_combo = QComboBox()  
        self.enstrumanlar_combo.addItems(["Piyano", "Gitar", "Flut", "Saksafon"])
        
        self.miktar_btn = QPushButton("Miktar Sec")
        self.miktar_btn.clicked.connect(self.select_quantity)
        
        self.miktar_label = QLabel("Miktar:")
        self.miktar_edit = QLineEdit()
        self.miktar_edit.setReadOnly(True)
        
        self.satis_yap_btn = QPushButton("Satis Yap")
        self.satis_yap_btn.clicked.connect(self.satis_yap)
        
        self.satis_kayitlarini_incele_btn = QPushButton("Siparis Kayitlarini Incele")
        self.satis_iptal_et_btn = QPushButton("Satis Iptal Et")
        
        self.satis_kayitlarini_incele_btn.clicked.connect(self.siparis_kayitlarini_incele)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.siparis_no_label)
        vbox.addWidget(self.siparis_no_edit)
        vbox.addWidget(self.enstrumanlar_label)
        vbox.addWidget(self.enstrumanlar_combo) 
        vbox.addWidget(self.miktar_btn)
        vbox.addWidget(self.miktar_label)
        vbox.addWidget(self.miktar_edit)
        vbox.addWidget(self.satis_yap_btn)
        vbox.addWidget(self.satis_kayitlarini_incele_btn)
        vbox.addWidget(self.satis_iptal_et_btn)
        
        self.setLayout(vbox)

    def satis_yap(self):
        secilen_enstruman = self.enstrumanlar_combo.currentText()
        miktar = int(self.miktar_edit.text())
          
        cursor.execute("INSERT INTO Siparisler (musteri_id, enstruman_ad, miktar) VALUES (?, ?, ?)",
                    (0, secilen_enstruman, miktar))
        
        cursor.execute("UPDATE Enstrumanlar SET stok_miktari = stok_miktari - ? WHERE ad = ?", (miktar, secilen_enstruman))
        
        conn.commit()

        QMessageBox.information(self, "Başarılı", "Satış kaydedildi ve stok güncellendi.")


        
    def select_quantity(self):
        miktar, ok_pressed = QInputDialog.getInt(self, "Miktar Sec", "Miktari Giriniz (Max 150):", 0, 0, 150)
        if ok_pressed:
            self.miktar_edit.setText(str(miktar))

    def siparis_kayitlarini_incele(self):
        secilen_enstruman = self.enstrumanlar_combo.currentText()
        musteri_id, ok_pressed = QInputDialog.getInt(self, "Musteri ID Gir", "Musteri ID'sini Giriniz:", 0)
        if ok_pressed:
            messagebox_text = f"Musteri ID: {musteri_id}\nSatin Alinan Enstruman: {secilen_enstruman}\nMiktar: {self.miktar_edit.text()}"
            QMessageBox.information(self, "Siparis Kayitlari Incele", messagebox_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = AnaPencere()
    pencere.show()
    sys.exit(app.exec_())
