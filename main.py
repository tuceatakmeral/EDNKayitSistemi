# -*- coding: utf-8 -*-
"""
Created on Dec 2 22:40:29 2020

@author: USER
"""



#----------------------KÜTÜPHANE--------------------------#
#---------------------------------------------------------#
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *
from HakkindaUI import *
#----------------------UYGULAMA OLUŞTUR-------------------#
#---------------------------------------------------------#
Uygulama=QApplication(sys.argv)
penAna=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(penAna)
penAna.show()

penHakkinda=QDialog()
ui2=Ui_Dialog()
ui2.setupUi(penHakkinda)




#----------------------VERİTABANI OLUŞTUR-----------------#
#---------------------------------------------------------#
import sqlite3
global curs
global conn

conn=sqlite3.connect('veritabani.db')
curs=conn.cursor()
sorguCreTblOgr=("CREATE TABLE IF NOT EXISTS ogr(                 \
                 Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,    \
                 TCNo TEXT NOT NULL UNIQUE,                        \
                 OgrAdi TEXT NOT NULL,                          \
                 OgrSoyadi TEXT NOT NULL,                       \
                 OgrOkulu TEXT NOT NULL,                           \
                 Grvl TEXT NOT NULL,                              \
                 Cinsiyet TEXT NOT NULL,                           \
                 Gun TEXT NOT NULL,                            \
                 dvmszlk TEXT NOT NULL,                               \
                 ogrSnf TEXT NOT NULL)")
curs.execute(sorguCreTblOgr)
conn.commit()

#----------------------KAYDET-----------------------------#
#---------------------------------------------------------#
def EKLE():
    _lneTCK=ui.lneTCK.text()
    _lneOgrAdi=ui.lneOgrAdi.text()
    _lneOgrSoyadi=ui.lneOgrSoyadi.text()
    _cmbOgrOkulu=ui.cmbOgrOkulu.currentText()
    _lwGrvl=ui.lwGrvl.currentItem().text()
    _cmbCinsiyet=ui.cmbCinsiyet.currentText()
    _cwGun=ui.cwGun.selectedDate().toString(QtCore.Qt.ISODate)
        
    if ui.chkdvmszlk.isChecked():
        _dvmszlk="Geldi"
    else:
        _dvmszlk="Gelmedi"
    _spnogrSnf=ui.spnogrSnf.value()
    
            
    curs.execute("INSERT INTO ogr \
                     (TCNo,OgrAdi,OgrSoyadi,OgrOkulu,Grvl,Cinsiyet,Gun,dvmszlk,ogrSnf) \
                      VALUES (?,?,?,?,?,?,?,?,?)", \
                      (_lneTCK,_lneOgrAdi,_lneOgrSoyadi,_cmbOgrOkulu,_lwGrvl,_cmbCinsiyet, \
                       _cwGun,_dvmszlk,_spnogrSnf))
    conn.commit()
    
    
    LISTELE()
#----------------------LİSTELE-----------------------------#
#---------------------------------------------------------#  
def LISTELE():
    
    ui.tblwOgrBilgi.clear()
    
    ui.tblwOgrBilgi.setHorizontalHeaderLabels(('No','TC Kimlik No','Oğrenci Adı','Öğrenci Soyadı', \
                                                  'Öğrenci Okulu', 'Öğrenci Sınıf', 'Cinsiyet', 'Geldiği Gün', \
                                                  'dvmszlk', 'Ort'))
    
    ui.tblwOgrBilgi.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    curs.execute("SELECT * FROM ogr")
    
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tblwOgrBilgi.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
    ui.lneTCK.clear()
    ui.lneOgrSoyadi.clear()
    ui.lneOgrAdi.clear()
    ui.cmbOgrOkulu.setCurrentIndex(-1)
    ui.spnogrSnf.setValue(55)
    
    curs.execute("SELECT COUNT(*) FROM ogr")
    kayitSayisi=curs.fetchone()
    ui.lblKayitSayisi.setText(str(kayitSayisi[0]))
    
    curs.execute("SELECT AVG(ogrSnf) FROM ogr")
    ort=curs.fetchone()
    ui.lblOrt.setText(str(ort[0]))
    
   
    

LISTELE()

#----------------------ÇIKIŞ-----------------------------#
#---------------------------------------------------------#  
def CIKIS():
    cevap=QMessageBox.question(penAna,"ÇIKIŞ","Programdan çıkmak istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        conn.close()
        sys.exit(Uygulama.exec_())
    else:
        penAna.show()
        

#----------------------SİL-----------------------------#
#---------------------------------------------------------# 
def SIL():
    cevap=QMessageBox.question(penAna,"KAYIT SİL","Kaydı silmek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        secili=ui.tblwOgrBilgi.selectedItems()
        silinecek=secili[1].text()
        try:
            curs.execute("DELETE FROM ogr WHERE TCNo='%s'" %(silinecek))
            conn.commit()
            
            LISTELE()
            
            ui.statusbar.showMessage("KAYIT SİLME İŞLEMİ BAŞARIYLA GERÇEKLEŞTİ...",10000)
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata ile karşılaşıldı:"+str(Hata))
    else:
        ui.statusbar.showMessage("Silme işlemi iptal edildi...",10000)
        
#----------------------ARAMA-----------------------------#
#---------------------------------------------------------# 

def ARA():
    aranan1=ui.lneTCK.text()
    aranan2=ui.lneOgrAdi.text()
    aranan3=ui.lneOgrSoyadi.text()
    curs.execute("SELECT * FROM ogr WHERE TCNo=? OR OgrAdi=? OR OgrSoyadi=? OR (OgrAdi=? AND OgrSoyadi=?)",  \
                 (aranan1,aranan2,aranan3,aranan2,aranan3))
    conn.commit()
    ui.tblwOgrBilgi.clear()
    for satirIndeks, satirVeri in enumerate(curs):
        for sutunIndeks, sutunVeri in enumerate (satirVeri):
            ui.tblwOgrBilgi.setItem(satirIndeks,sutunIndeks,QTableWidgetItem(str(sutunVeri)))
#----------------------DOLDUR-----------------------------#
#---------------------------------------------------------#
def DOLDUR():
    secili=ui.tblwOgrBilgi.selectedItems()
    ui.lneTCK.setText(secili[1].text())
    ui.lneOgrAdi.setText(secili[2].text())
    ui.lneOgrSoyadi.setText(secili[3].text())
    ui.cmbOgrOkulu.setCurrentText(secili[4].text())
    if secili[5].text()=="Tuçe ATAK MERAL":
        ui.lwGrvl.item(0).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(0))
    if secili[5].text()=="Adem ÜNLÜ":
        ui.lwGrvl.item(1).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(1))
    if secili[5].text()=="Hasan AYBAK":
        ui.lwGrvl.item(2).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(2))
    if secili[5].text()=="Tolga AKGÜL":
        ui.lwGrvl.item(3).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(3))
    if secili[5].text()=="Yavuz TARHAN":
        ui.lwGrvl.item(4).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(4))
    if secili[5].text()=="Yasemin ÇETİNKAYA":
        ui.lwGrvl.item(5).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(5))
    if secili[5].text()=="Murat ÇELEBİ":
        ui.lwGrvl.item(6).setSelected(True)
        ui.lwGrvl.setCurrentItem(ui.lwGrvl.item(6))
    
    ui.cmbCinsiyet.setCurrentText(secili[6].text())
    
    yil=int(secili[7].text()[0:4])
    ay=int(secili[7].text()[5:7])
    gun=int(secili[7].text()[8:10])
    ui.cwGun.setSelectedDate(QtCore.QDate(yil,ay,gun))
    
    if secili[8].text()=="Geldi":
        ui.chkdvmszlk.setChecked(True)
    else:
        ui.chkdvmszlk.setChecked(False)
    
    ui.spnogrSnf.setValue(int(secili[9].text()))
    
#----------------------GÜNCELLE-----------------------------#
#---------------------------------------------------------#
def GUNCELLE():
    cevap=QMessageBox.question(penAna,"KAYIT GÜNCELLE","Kaydı güncellemek istediğinize emin misiniz?",\
                         QMessageBox.Yes | QMessageBox.No)
    if cevap==QMessageBox.Yes:
        try:
            secili=ui.tblwOgrBilgi.selectedItems()
            _Id=int(secili[0].text())
            _lneTCK=ui.lneTCK.text()
            _lneOgrAdi=ui.lneOgrAdi.text()
            _lneOgrSoyadi=ui.lneOgrSoyadi.text()
            _cmbOgrOkulu=ui.cmbOgrOkulu.currentText()
            _lwGrvl=ui.lwGrvl.currentItem().text()
            _cmbCinsiyet=ui.cmbCinsiyet.currentText()
            _cwGun=ui.cwGun.selectedDate().toString(QtCore.Qt.ISODate)
        
            if ui.chkdvmszlk.isChecked():
                _dvmszlk="Geldi"
            else:
                _dvmszlk="Gelmedi"
            _spnogrSnf=ui.spnogrSnf.value()
            
            curs.execute("UPDATE ogr SET TCNo=?, OgrAdi=?, OgrSoyadi=?, ogrSnf=?,   \
                         OgrOkulu=?, Grvl=?, Cinsiyet=?, Gun=?, dvmszlk=? WHERE Id=?", \
                         (_lneTCK,_lneOgrAdi,_lneOgrSoyadi,_spnogrSnf,\
                          _cmbOgrOkulu,_lwGrvl,_cmbCinsiyet,_cwGun,_dvmszlk,_Id))
            conn.commit()
            
            LISTELE()
            
        except Exception as Hata:
            ui.statusbar.showMessage("Şöyle bir hata meydana geldi"+str(Hata))
    else:
        ui.statusbar.showMessage("Güncellme iptal edildi",10000)


#----------------------HAKKINDA-----------------------------#
#---------------------------------------------------------#
def HAKKINDA():
    penHakkinda.show()


#----------------------SİNYAL-SLOT-----------------------------#
#---------------------------------------------------------#
ui.btnEkle.clicked.connect(EKLE)
ui.btnListele.clicked.connect(LISTELE)
ui.btnCikis.clicked.connect(CIKIS)
ui.btnSil.clicked.connect(SIL)
ui.btnAra.clicked.connect(ARA)
ui.tblwOgrBilgi.itemSelectionChanged.connect(DOLDUR)
ui.btnGuncelle.clicked.connect(GUNCELLE)
ui.menuHakkinda.triggered.connect(HAKKINDA)



sys.exit(Uygulama.exec_())
