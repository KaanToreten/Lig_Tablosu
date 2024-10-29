import  os
class Takım:
    def __init__(self,kısa_isim, uzun_isim):
        self.kısa_isim = kısa_isim
        self.uzun_isim = uzun_isim
        self.oyun = 0
        self.galibiyet = 0
        self.beraberlik = 0
        self.mağlubiyet = 0
        self.atılan_gol = 0
        self.yenilen_gol = 0
        self.puan = 0
    def istatistikler(self,atılan_gol,yenilen_gol,sonuç_puan):
        self.oyun += 1
        self.atılan_gol += atılan_gol
        self.yenilen_gol += yenilen_gol
        self.puan += sonuç_puan
        if sonuç_puan == galibiyet_puan:
            self.galibiyet += 1
        elif sonuç_puan == beraberlik_puan:
            self.beraberlik += 1
        elif sonuç_puan == kaybedilen_puan:
            self.mağlubiyet += 1
def ayarlar_f():
    global takım_sayısı, galibiyet_puan, beraberlik_puan,kaybedilen_puan
    with open("ayarlar.txt") as f:
        ayarlar = f.readlines()
        takım_sayısı = int(ayarlar[0].strip())
        galibiyet_puan = int(ayarlar[1].strip())
        beraberlik_puan = int(ayarlar[2].strip())
        kaybedilen_puan = int(ayarlar[3].strip())

def takım_f():
    takımlar = {}
    with open("takimlar.txt", encoding="utf-8") as f:
        for satır in f:
            kısa_isim, uzun_isim = satır.strip().split()
            takımlar[kısa_isim] = Takım(kısa_isim,uzun_isim)
    return takımlar

def yapılan_maçlar(ev,ev_gol,deplasman,deplasman_gol):
    if(ev,deplasman) in oynan_maçlar:
        print(f"DİKKAT {ev} ve {deplasman} DAHA ÖNCE MAÇ OYNADILAR." )
        return
    oynan_maçlar.add((ev,deplasman))

    ev_gol = int(ev_gol)
    deplasman_gol = int(deplasman_gol)

    if ev_gol > deplasman_gol :
        ev_sonuç, deplasman_sonuç = galibiyet_puan, kaybedilen_puan
    elif ev_gol < deplasman_gol :
        ev_sonuç, deplasman_sonuç = kaybedilen_puan, galibiyet_puan
    else:
        ev_sonuç, deplasman_sonuç = beraberlik_puan, beraberlik_puan

    takımlar[ev].istatistikler(ev_gol,deplasman_gol,ev_sonuç)
    takımlar[deplasman].istatistikler(deplasman_gol,ev_gol,deplasman_sonuç)

def oynanacak_maçlar(dosya_adı="maclar.txt"):
    with open(dosya_adı) as f:
        for satır in f:
            maç_verisi = satır.strip().split()
            if len(maç_verisi) == 4:
                yapılan_maçlar(*maç_verisi)
            else:
                print("DOSYADA GEÇERSİZ BİÇİM.")
def puan_durumları(order="puanlar",büyük_harf=False):
    sıralamalar = sorted(takımlar.values(),key=lambda x: (-x.puan, x.kısa_isim))
    print("Team | O | G | B | M | AG | YG | A | Puan")
    for takım in sıralamalar:
        isim = takım.uzun_isim.upper() if büyük_harf else takım.uzun_isim
        print(f"{isim} | {takım.oyun} | {takım.galibiyet} | {takım.beraberlik} | {takım.mağlubiyet} | "
              f"{takım.atılan_gol} | {takım.yenilen_gol} | {takım.atılan_gol - takım.yenilen_gol} | {takım.puan}")


if __name__ == "__main__":
    ayarlar_f()
    takımlar = takım_f()
    oynan_maçlar = set()

    oynanacak_maçlar("maclar.txt")

    puan_durumları()



