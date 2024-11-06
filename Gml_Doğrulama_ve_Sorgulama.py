
"""

TKGM 3 BOYUTLU YAPI MODELİ DOĞRULAMA VE SORGULAMA İŞLEMLERİ

- Gml Doğrulama
- Gml Sorgulama
- Sorgulanan Gml'in Pdf ve Gml Dosyalarını İndirme

Not: TKGM Otomatik Doğrulama Web Sitesinde Yer Alan Servisler Kullanılmıştır.

"""

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,simpledialog, messagebox
import os
import json
import requests
import base64
import threading
import re
# Pencereyi oluştur
# Pencereyi ekranın ortasında açma

# TKGM Sisteminde Gml Yüklerken Gerekli Olan Form Bilgilerinin Alınması
def kullanici_bilgi_kontrol():
    dosya_yol="kullanici_bilgi.txt"
    if os.path.exists(dosya_yol):
        with open(dosya_yol,"r") as file:
            metin=file.read()
        kullanici_bilgi={}
        satirlar=metin.splitlines()
        for satir in satirlar:
            anahtar,deger=satir.split(":",1)
            kullanici_bilgi[anahtar.strip()]=deger.strip()
        kullanici_bilgi=json.dumps(kullanici_bilgi,indent=4)
        return kullanici_bilgi
    else:
        # Ana pencereyi oluştur
        root = tk.Tk()
        root.withdraw()  # Ana pencereyi gizle
        screen_width = root.winfo_screenwidth()  # Ekranın genişliği
        screen_height = root.winfo_screenheight()  # Ekranın yüksekliği
        window_width = 400  # Pencere genişliği
        window_height = 200  # Pencere yüksekliği
        position_top = int((screen_height - window_height) / 2)
        position_right = int((screen_width - window_width) / 2)
        root.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")
        # Uyarı mesajı
        messagebox.showwarning(
            "UYARI",
            "GML Yüklemek İçin Gerekli Kullanıcı Bilgileri Bulunamadı. Tamam Diyerek Bilgilerinizi Tamamlayın.\n *Bilgileriniz Uygulama Klasörüne Kaydedilecek ve Sonraki İşlemlerde Kullanılacaktır."
        )
        
        user_info = {}

        root.deiconify()  # Pencereyi tekrar görünür yap
        root.title("Başvuran Türü")

        # Zorunlu alanlar
        kurum_tip = tk.StringVar(value="none")

        secenek1 = tk.Radiobutton(root, text="Şahıs", variable=kurum_tip, value="Person")
        secenek2 = tk.Radiobutton(root, text="Kurum/Şirket", variable=kurum_tip, value="Corporation")
        
        secenek1.pack()
        secenek2.pack()

        # Seçimi tamamlama fonksiyonu
        def secimi_tamamla():
            user_info["type"] = kurum_tip.get()
            root.destroy()  # Ana pencereyi kapat

        submit_button = tk.Button(root, text="Seçimi Tamamla", command=secimi_tamamla)
        submit_button.pack()

        root.mainloop()  # Ana döngüye gir ve pencereyi açWWW
        if kurum_tip.get()=="none":
            messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
            return None
        
        # Kullanıcı bilgilerini al
        user_info["name"] = simpledialog.askstring("Bilgi", "Adınızı girin:")
        if user_info["name"]==None:
            messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
            return None
        
        user_info["eMail"] = simpledialog.askstring("Bilgi", "Mail Adresinizi Giriniz:")
        if user_info["eMail"]==None:
            messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
            return None
        
        if user_info["type"]=="Person":
            user_info["identificationNumber"] = simpledialog.askstring("Bilgi", "TC numaranızı girin:")
            if user_info["identificationNumber"]==None:
                messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
                return None
            elif user_info["identificationNumber"].isdigit() and len(user_info["identificationNumber"])==11:
                print("")
            else:
                messagebox.showwarning(
                        "UYARI",
                        "TC Kimlik No Hatalı("+user_info["identificationNumber"]+"). İşlemler Tekrardan Başlayacak"
                    )
                return kullanici_bilgi_kontrol()
        elif user_info["type"]=="Corporation":
            user_info["identificationNumber"] = simpledialog.askstring("Bilgi", "Vergi numaranızı girin:")
            if user_info["identificationNumber"]==None:
                messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
                return None
            
            elif user_info["identificationNumber"].isdigit() and len(user_info["identificationNumber"])==10:
                print("")
            else:
                messagebox.showwarning(
                        "UYARI",
                        "Vergi Kimlik No Hatalı("+user_info["identificationNumber"]+"). İşlemler Tekrardan Başlayacak"
                    )
                return kullanici_bilgi_kontrol()
                

        # Zorunlu olmayan alanlar
        user_info["phoneNumber"] = "+90"+simpledialog.askstring("Bilgi", "Telefon numaranızı girin (isteğe bağlı) +90:")
        if user_info["phoneNumber"]=="+90":
            user_info["phoneNumber"]=""
        
        user_info["mobilePhoneNumber"] = "+90"+simpledialog.askstring("Bilgi", "Cep telefon numaranızı girin +90:")
        if user_info["mobilePhoneNumber"]==None:
                messagebox.showwarning(
            "UYARI",
            "Giriş yapılmadı. Program sonlandı."
        )
        if len(user_info["mobilePhoneNumber"])!=13:
            messagebox.showwarning(
                "UYARI",
                "Hatalı Giriş Yaptınız. Girilen Bilgi:"+user_info["mobilePhoneNumber"]
            )
            return kullanici_bilgi_kontrol()
        with open("kullanici_bilgi.txt","w") as file:
            for key,value in user_info.items():
                file.write(f"{key}:{value}\n")
        return kullanici_bilgi_kontrol()
        
isteksahibi=kullanici_bilgi_kontrol()

def start_upload_thread():
    # Dosya yükleme işlemini bir iş parçacığında çalıştır
    threading.Thread(target=soldaki_buton_tikla, daemon=True).start()
def soldaki_buton_tikla():
    text_box.delete(1.0, tk.END)
    gonderilecekveri= {"sender":json.loads(isteksahibi)}    #Kullanıcı Bilgileri Json Formatında Çekilir
    url = 'https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/ArchitecturalBuildingControlCreate'   #Post URL
    response=requests.post(url,json=gonderilecekveri)   #Kondol ID' si alınır
    responseid=response.json()["id"]    #Kontrol ID' si
    
    # Birden fazla dosya seçmek için dosya diyalogu aç
    gml_dosyalari = filedialog.askopenfilenames(    
        title="GML Dosyalarını Seçin",
        filetypes=[("GML Dosyaları", "*.gml")],  # Yalnızca .gml dosyalarını göster
    )
    
    if gml_dosyalari:
        # Seçilen dosyaların yolunu metin kutusuna ekle
        text_box.delete(1.0, tk.END)  # Önceden yazılmış olanları temizle
    #gml isim kontrolü
        isimlendirme_dogru_mu=bool
        dosyaboyutu=0
        deseni=r"^M-\d+-[A-Za-z]\.gml$"
        sayisal_kisim=None
        for dosya in gml_dosyalari:
            dosyaboyutu+=os.path.getsize(dosya)
        # Her bir dosya adının desene uyup uymadığını kontrol et
            dosya=dosya.split('/')[-1]
            if re.match(deseni, dosya):
                # Sayısal kısmı ayıklıyoruz (dosya adı "M-24619331-A.gml" şeklinde olduğunda, 24619331 kısmını alacağız)
                sayisal = dosya.split('-')[1]  # Sayısal kısmı ayıklıyoruz
                if sayisal_kisim is None:
                    # İlk dosyanın sayısal kısmını alıyoruz
                    sayisal_kisim = sayisal
                elif sayisal_kisim != sayisal:
                    # Sayısal kısımlar eşleşmiyor
                    isimlendirme_dogru_mu=False
                    break
            else:
                
                # Geçersiz dosya adı formatı
                isimlendirme_dogru_mu=False
                break
            isimlendirme_dogru_mu=True 
                  # Döngüyü sonlandırıyoruz, çünkü geçersiz bir dosya bulundu
        if (isimlendirme_dogru_mu):     #Gml isimleri doğruysa kontrole gider
            text_box.insert(tk.END,"Dosya Boyutu:"+str(round(dosyaboyutu/1024/1024,3))+" Mb\n"+"Dosya Gönderiliyor"+"\n") #Bilgi Kutusuna dosya boyutu Yazma
            for gml_file_path in gml_dosyalari: #Seçilen Gml ler teker teker servise gönderilir
                with open(gml_file_path,"rb") as file:  #gmller iki byte formatında okunur
                    gml_file_content = file.read(-1)  #okuma
                
                base64_encoded = str(base64.b64encode(gml_file_content)) #ikili byte
                veri1=str(base64_encoded).replace("b'","")
                veri2=veri1.replace("'","")
                request_data = {    #post edilecek data
                'architecturalBuildingControlId': responseid,
                # UUID oluştur
                'gmlFileContent': veri2,
                'gmlFileName': gml_file_path.split('/')[-1]# Base64 içerik  M-*****-A/B/C 
                }
                # Dosya adı
                response2=requests.post('https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/ArchitecturalBuildingControlAddFile',json=request_data) #Gml gönderilir
                if response2.status_code==200:
                    text_box.insert(tk.END, gml_file_path.split('/')[-1]+"  dosyası yüklendi.\n")   #200 kodu ile birlikte gml sisteme yüklenmiştir.
                else:
                    messagebox.showwarning(
                "UYARI",
                "GML Yükleme Aşamasında Sorun Oluştu. Gml isimlendirmesini ve dosya uygunluğunu kontrol ediniz."
            )
            dogrulama_baslat=requests.post("https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/ArchitecturalBuildingControlStartControl",json={"architecturalBuildingControlId":responseid}) #Gml yüklendikten sonra doğrulamanın başlatılması için istek yapılır
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END,f"Doğrulama Başlatıldı. {gonderilecekveri['sender']['eMail']} Mail adresinizi kontrol ediniz.")
        else:
            messagebox.showwarning("HATA","GML İSİMLERİNİ KONTROL EDİNİZ.")

    else:
        text_box.insert(tk.END, "Dosya seçilmedi.\n")

# Sağ butonun tıklama fonksiyonu
def sagdaki_buton_tikla():
    girilen_metni = entry.get()  # Giriş alanındaki metni al
    if len(girilen_metni)==6:   # Validasyon Kodu 6 hanelidir
        response=requests.post("https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/ArchitecturalBuildingControlStateControl",json={"validationCode":girilen_metni}) # Durum Bilgisi Alma
        if response.status_code==200:
            result=response.json()
            durumbilgi=f"{result['stateDescription']}, Açıklama: {result['stateDefinition']}" 
            label_info.config(text=f"Bilgi: {durumbilgi}")  # Bilgi kutusunu güncelle
            create_buttons(girilen_metni)
        else:
            messagebox.showinfo("HATA","Hata Oluştu. Tekrar Deneyin")
    else:
        messagebox.showwarning(
            "UYARI",
            "Girilen doğrulama kodu hatalı."
        )
    
    # 3 yeni buton ekle
   

# 3 yeni buton eklemek için fonksiyon
def create_buttons(girilen_metni):
    # Eğer butonlar zaten eklenmişse, tekrar eklememek için bir kontrol yapalım
    def pdfindir():
        pdfindir=requests.post(url="https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/GetArchitecturalBuildingControlDetail",json={"validationCode":girilen_metni}) #Mimari detaylarını alma
        mimariidleri=pdfindir.json()["architecturalBuildingList"] # Validasyonda Yer Alan Mimari Modelleri Alma
        for i in mimariidleri: #Birden Fazla Mimari Modelde Modelleri Teker Teker Alma
            pdfindir=requests.post(url="https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/DownloadArchitecturalBuildingReportPdf",json={"architecturalBuildingId":i["id"]}) #Pdf İçerik Alma
            pdfisim=(i["gmlFileName"]).replace(".gml",".pdf") #İsimlendirme
            with open(pdfisim,"wb") as f:
                f.write(pdfindir.content) #Yerel Klasöre Kaydetme
        messagebox.showinfo("BİLGİ","Doğrulama Kodunda Yer Alan Tüm Raporlar, Program klasörüne İndirilmiştir.")
    def gmlindir():
        gmlindir=requests.post(url="https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/GetArchitecturalBuildingControlDetail",json={"validationCode":girilen_metni}) #Mimari detaylarını alma
        mimariidleri=gmlindir.json()["architecturalBuildingList"]   # Validasyonda Yer Alan Mimari Modelleri Alma
        for i in mimariidleri:  #Birden Fazla Mimari Modelde Modelleri Teker Teker Alma
            gmlindir=requests.post(url="https://3dbinadogrulaservis.tkgm.gov.tr/api/ArchitecturalBuilding/DownloadArchitecturalBuildingCityGml",json={"architecturalBuildingId":i["id"]}) #Gml İçerik Alma
            gmlisim=(i["gmlFileName"])  #İsimlendirme
            with open(gmlisim,"wb") as f:
                f.write(gmlindir.content)   #Yerel Klasöre Kaydetme
        messagebox.showinfo("BİLGİ","Doğrulama Kodunda Yer Alan Tüm Gml Dosyaları, Program klasörüne İndirilmiştir.")      
    if not hasattr(create_buttons, "buttons_created") or not create_buttons.buttons_created:
        # Yeni butonları içerecek bir çerçeve (frame) oluştur
        button_frame = tk.Frame(frame_sag)
        button_frame.pack(pady=20)  # Bilgi kutusunun altına yerleştirildi
        
        # 3 tane buton ekle
        button1 = tk.Button(button_frame, text="Pdf İndir", command=pdfindir)
        button1.grid(row=0, column=0, padx=10)

        button2 = tk.Button(button_frame, text="GML İndir", command=gmlindir)
        button2.grid(row=0, column=1, padx=10)
        
        # Butonlar eklenmiş olduğu bilgisini sakla
        create_buttons.buttons_created = True

if isteksahibi!=None:
    root = tk.Tk()
    root.title("GML Yükleme-Sorgulama")
    root.geometry("700x600")  # Pencere boyutu (genişlik x yükseklik)
# Sol butonun tıklama fonksiyonu

# Sol taraf için bir çerçeve (frame)
frame_sol = tk.Frame(root)
frame_sol.pack(side="left", padx=20, pady=30, fill=tk.Y)  # Sol tarafı dikey olarak dolduracak şekilde yerleştiriyoruz
# İlerleme çubuğu (Progress Bar)
progress_bar = ttk.Progressbar(frame_sol, length=200, mode='determinate')
progress_bar.pack(side="top", pady=10)
# Sol buton
button_sol = tk.Button(frame_sol, text="GML YÜKLE", command=start_upload_thread)
button_sol.pack(side="top", pady=10)



# Metin kutusu (Text Box)
text_box = tk.Text(frame_sol, height=5, width=40)
text_box.pack(side="top", pady=10)

# Sağ taraf için bir çerçeve (frame)
frame_sag = tk.Frame(root)
frame_sag.pack(side="right", padx=20, pady=30)

# Giriş alanı (Input)
entry = tk.Entry(frame_sag, width=30)
entry.pack(pady=10)
entry.insert(0,"Doğrulama Kodu")

# Sağ buton
button_sag = tk.Button(frame_sag, text="SORGULA", command=sagdaki_buton_tikla)
button_sag.pack(pady=10)

# Bilgi kutusu (Label)
label_info = tk.Label(frame_sag, text="Sonuç: ",wraplength=300)
label_info.pack(pady=10)

# Pencereyi sürekli açık tut
root.mainloop()
