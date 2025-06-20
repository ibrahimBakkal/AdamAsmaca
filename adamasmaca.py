import random
import os

def kelimeleri_yukle(dosya_adi):
    klasor = os.path.dirname(os.path.abspath(__file__))
    dosya_yolu = os.path.join(klasor, dosya_adi)
    with open(dosya_yolu, "r", encoding="utf-8") as f:
        return [satir.strip() for satir in f if satir.strip()]

def adam_asmaca():
    kelimeler = kelimeleri_yukle("kelimeler.txt")
    kelime = random.choice(kelimeler)
    cizgi = ["_" for _ in kelime]
    tahmin_edilen = set()
    hak = len(kelime)
    ipucu_kullanildi = False

    while hak > 0:
        print(f"Kalan hak: {hak}")
        print("Kelime: ", " ".join(cizgi))
        inp = input("Harf, kelime veya 'ipucu' yazınız: ").lower()

        if not inp:
            print("Lütfen bir harf, kelime veya 'ipucu' giriniz.")
            continue
        if inp == "ipucu":
            if ipucu_kullanildi:
                print("Zaten bir ipucu kullandınız!")
                continue
            acilmamis = [i for i, harf in enumerate(cizgi) if harf == "_"]
            if not acilmamis:
                print("Açılmamış harf kalmadı!")
                continue
            secili = random.choice(acilmamis)
            cizgi[secili] = kelime[secili]
            tahmin_edilen.add(kelime[secili])
            hak -= 1
            ipucu_kullanildi = True
            print(f"İpucu: {secili+1}. harf '{kelime[secili]}' açıldı!")
        elif len(inp) == 1:
            if inp in tahmin_edilen:
                print("Bu harfi zaten girdiniz!")
                continue
            tahmin_edilen.add(inp)
            if inp in kelime:
                for i, harf in enumerate(kelime):
                    if harf == inp:
                        cizgi[i] = inp
            else:
                hak -= 1
                print(f"Yanlış! {inp} harfi kelimede yok.")
        elif len(inp) == len(kelime):
            if inp == kelime:
                print("Tebrikler, kelimeyi doğru bildiniz! Kelime: ", kelime)
                break
            else:
                hak -= 1
                print("Yanlış tahmin! Kelime bu değil.")
        else:
            print("Geçersiz giriş. Tek harf, kelimenin tamamı veya 'ipucu' yazınız.")

        if "_" not in cizgi:
            print("Tebrikler, kazandınız! Kelime: ", kelime)
            break
    else:
        print(f"Kaybettiniz! Doğru kelime: {kelime}")

if __name__ == "__main__":
    adam_asmaca()
    