import tkinter as tk
from tkinter import messagebox
import random
import os

# Kelimeleri dosyadan oku
def kelimeleri_yukle(dosya_adi):
    klasor = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(klasor, dosya_adi)
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return [satir.strip() for satir in f if satir.strip()]

class AdamAsmacaGUI:
    def __init__(self, master):
        self.master = master
        master.title("Adam Asmaca")
        master.resizable(False, False)
        master.configure(bg="#f0f4f8")
        self.kelimeler = kelimeleri_yukle("kelimeler.txt")
        self.yeni_oyun()
        self.oyun_olustur()

    def yeni_oyun(self):
        self.kelime = random.choice(self.kelimeler)
        self.cizgi = ["_" for _ in self.kelime]
        self.tahmin_edilen = set()
        self.hak = len(self.kelime)
        self.ipucu_kullanildi = False
        self.oyun_bitti = False

    def oyun_olustur(self):
        # Başlık
        self.lbl_baslik = tk.Label(self.master, text="Adam Asmaca", font=("Segoe UI", 28, "bold"), bg="#f0f4f8", fg="#2d415a")
        self.lbl_baslik.pack(pady=(20, 10))

        # Kelime
        self.lbl_kelime = tk.Label(self.master, text=" ".join(self.cizgi), font=("Consolas", 32, "bold"), bg="#f0f4f8", fg="#3a7ca5")
        self.lbl_kelime.pack(pady=10)

        # Kalan hak
        self.lbl_hak = tk.Label(self.master, text=f"Kalan hak: {self.hak}", font=("Segoe UI", 16), bg="#f0f4f8", fg="#2d415a")
        self.lbl_hak.pack(pady=5)

        # Giriş kutusu
        self.entry = tk.Entry(self.master, font=("Segoe UI", 16), width=18, justify="center", relief="solid", bd=2)
        self.entry.pack(pady=10)
        self.entry.bind('<Return>', lambda event: self.tahmin_et())

        # Butonlar çerçevesi
        self.btn_frame = tk.Frame(self.master, bg="#f0f4f8")
        self.btn_frame.pack(pady=5)

        self.btn_tahmin = tk.Button(self.btn_frame, text="Tahmin Et", command=self.tahmin_et, font=("Segoe UI", 13, "bold"),
                                    bg="#3a7ca5", fg="white", activebackground="#28527a", activeforeground="white",
                                    relief="flat", padx=18, pady=6, borderwidth=0, cursor="hand2")
        self.btn_tahmin.grid(row=0, column=0, padx=8)

        self.btn_ipucu = tk.Button(self.btn_frame, text="İpucu", command=self.ipucu_ver, font=("Segoe UI", 13, "bold"),
                                   bg="#f7b801", fg="white", activebackground="#f6a801", activeforeground="white",
                                   relief="flat", padx=18, pady=6, borderwidth=0, cursor="hand2")
        self.btn_ipucu.grid(row=0, column=1, padx=8)

        # Mesaj
        self.lbl_mesaj = tk.Label(self.master, text="", font=("Segoe UI", 14, "bold"), bg="#f0f4f8")
        self.lbl_mesaj.pack(pady=10)

        # Yeniden Oyna butonu
        self.btn_yeniden = tk.Button(self.master, text="Yeniden Oyna", command=self.yeniden_oyna, font=("Segoe UI", 13, "bold"),
                                     bg="#2d415a", fg="white", activebackground="#1b2838", activeforeground="white",
                                     relief="flat", padx=18, pady=6, borderwidth=0, cursor="hand2")
        self.btn_yeniden.pack(pady=(10, 20))
        self.btn_yeniden.config(state=tk.DISABLED)

    def tahmin_et(self):
        if self.oyun_bitti:
            return
        inp = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)
        if not inp:
            self.lbl_mesaj.config(text="Lütfen bir harf veya kelime giriniz.", fg="#e63946")
            return
        if inp == "ipucu":
            self.ipucu_ver()
            return
        if len(inp) == 1:
            if inp in self.tahmin_edilen:
                self.lbl_mesaj.config(text="Bu harfi zaten girdiniz!", fg="#e63946")
                return
            self.tahmin_edilen.add(inp)
            if inp in self.kelime:
                for i, harf in enumerate(self.kelime):
                    if harf == inp:
                        self.cizgi[i] = inp
                self.lbl_mesaj.config(text=f"Doğru! '{inp}' harfi var.", fg="#43aa8b")
            else:
                self.hak -= 1
                self.lbl_mesaj.config(text=f"Yanlış! '{inp}' harfi yok.", fg="#e63946")
        elif len(inp) == len(self.kelime):
            if inp == self.kelime:
                self.cizgi = list(self.kelime)
                self.lbl_kelime.config(text=" ".join(self.cizgi))
                self.lbl_mesaj.config(text="Tebrikler, kelimeyi doğru bildiniz!", fg="#43aa8b")
                self.oyunu_bitir(kazandi=True)
                return
            else:
                self.hak -= 1
                self.lbl_mesaj.config(text="Yanlış tahmin! Kelime bu değil.", fg="#e63946")
        else:
            self.lbl_mesaj.config(text="Geçersiz giriş. Tek harf veya kelimenin tamamını giriniz.", fg="#e63946")
            return
        self.lbl_kelime.config(text=" ".join(self.cizgi))
        self.lbl_hak.config(text=f"Kalan hak: {self.hak}")
        if "_" not in self.cizgi:
            self.lbl_mesaj.config(text=f"Tebrikler, kazandınız! Kelime: {self.kelime}", fg="#43aa8b")
            self.oyunu_bitir(kazandi=True)
        elif self.hak <= 0:
            self.lbl_mesaj.config(text=f"Kaybettiniz! Doğru kelime: {self.kelime}", fg="#e63946")
            self.oyunu_bitir(kazandi=False)

    def ipucu_ver(self):
        if self.oyun_bitti:
            return
        if self.ipucu_kullanildi:
            self.lbl_mesaj.config(text="Zaten bir ipucu kullandınız!", fg="#e63946")
            return
        acilmamis = [i for i, harf in enumerate(self.cizgi) if harf == "_"]
        if not acilmamis:
            self.lbl_mesaj.config(text="Açılmamış harf kalmadı!", fg="#e63946")
            return
        secili = random.choice(acilmamis)
        self.cizgi[secili] = self.kelime[secili]
        self.tahmin_edilen.add(self.kelime[secili])
        self.hak -= 1
        self.ipucu_kullanildi = True
        self.lbl_kelime.config(text=" ".join(self.cizgi))
        self.lbl_hak.config(text=f"Kalan hak: {self.hak}")
        self.lbl_mesaj.config(text=f"İpucu: {secili+1}. harf '{self.kelime[secili]}' açıldı!", fg="#f7b801")
        if "_" not in self.cizgi:
            self.lbl_mesaj.config(text=f"Tebrikler, kazandınız! Kelime: {self.kelime}", fg="#43aa8b")
            self.oyunu_bitir(kazandi=True)
        elif self.hak <= 0:
            self.lbl_mesaj.config(text=f"Kaybettiniz! Doğru kelime: {self.kelime}", fg="#e63946")
            self.oyunu_bitir(kazandi=False)

    def oyunu_bitir(self, kazandi):
        self.oyun_bitti = True
        self.btn_tahmin.config(state=tk.DISABLED)
        self.btn_ipucu.config(state=tk.DISABLED)
        self.btn_yeniden.config(state=tk.NORMAL)

    def yeniden_oyna(self):
        self.lbl_baslik.destroy()
        self.lbl_kelime.destroy()
        self.lbl_hak.destroy()
        self.entry.destroy()
        self.btn_tahmin.destroy()
        self.btn_ipucu.destroy()
        self.lbl_mesaj.destroy()
        self.btn_yeniden.destroy()
        self.btn_frame.destroy()
        self.yeni_oyun()
        self.oyun_olustur()

if __name__ == "__main__":
    root = tk.Tk()
    app = AdamAsmacaGUI(root)
    root.mainloop() 