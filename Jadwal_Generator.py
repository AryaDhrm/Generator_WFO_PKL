import tkinter as tk
from tkinter import messagebox,ttk
# from tkinter import ttk
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont # type: ignore
import textwrap
import copy

anak_magang = []
jadwal_Wfo = defaultdict(list)
jadwal_Wfo_copy = {}


def simpan_jadwal():
    # load_jadwal()
    global anak_magang, jadwal_Wfo_copy
    
    input_anak_magang = input_nama.get()
    min_wfh = input_max.get()
    max_wfo = input_max_wfo.get()
    anak_magang = [name.strip() for name in input_anak_magang.split(",")]

    total_max_magang = len(anak_magang)
    
    days = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu']
    
   
    if not max_wfo.isdigit() or int(max_wfo) < 1:
        messagebox.showerror("Input Error", "Masukkan batas WFO yang valid (lebih dari 0).")
        return

    if not min_wfh.isdigit() or int(min_wfh) < 1:
        messagebox.showerror("Input Error", "Masukkan batas WFH yang valid (lebih dari 0).")
        return

    # Mengecek apakah jumlah anak magang lebih kecil dari kapasitas kantor
    if total_max_magang <= int(max_wfo) * len(days):
        if not input_anak_magang:
            messagebox.showerror("Input Error", "Pastikan Anda memasukkan nama anak magang.")
            return
    else:
        messagebox.showerror("Input Error", "Jumlah anak magang melebihi kapasitas kantor")
        return

    
    min_wfh = int(min_wfh)
    max_wfo = int(max_wfo)
    
    max_wfo_person = len(days) - min_wfh
    
    print (f"ini adalah jumlah WFO setiap minggu {max_wfo_person}")
     
    jumlah_wfh = {name: 0 for name in anak_magang}
    max_jumlah_WFO = {day: max_wfo for day in days}
    
    # print(max_jumlah_WFO)
    total_hari = len(days)
    total_magang = len(anak_magang)
    
    index_hari = 0
    index_anak = 0
    
    # max_loop = 0;
    
    while any(jumlah < max_wfo_person for jumlah in jumlah_wfh.values()) and any(len(jadwal_Wfo[hari]) < max_wfo for hari in days):
        hari = days[index_hari]
        nama = anak_magang[index_anak]

        nama_ditambah = False
        hari_sudah_diganti = False
        # flag = False
        # print(index_anak)
        
        if nama in jadwal_Wfo[hari]:
            if index_anak < total_magang-1:
                index_anak +=1
                nama = anak_magang[index_anak]
            else:
                index_anak = 0
                nama = anak_magang[index_anak]
            
            # ini dirubah 
        if  jumlah_wfh[nama] < max_wfo_person and nama not in jadwal_Wfo[hari]:
            # ini ditambahkan
            if len(jadwal_Wfo[hari]) < int(max_jumlah_WFO[hari]): 
                jadwal_Wfo[hari].append(nama)
                jumlah_wfh[nama] += 1
            else:
                index_hari+=1
                hari_sudah_diganti = True
                jadwal_Wfo[hari].append(nama)
                jumlah_wfh[nama] += 1
            # nama_ditambah = True
        
        if index_anak < total_magang - 1:
            index_anak += 1
        else:
            index_anak = 0
        
        if(index_hari < total_hari-1):
            #  and hari_sudah_diganti == False
            if not hari_sudah_diganti:
                index_hari += 1
        else:
            index_hari = 0
            
    with open("jadwal_WFO.txt", "w") as file: 
        for day, names in jadwal_Wfo.items():
            file.write(f"{day}: {', '.join(names)}\n")
            
    for row in tree.get_children():
        tree.delete(row)  
    
    for day in days:
        # print(day)
        # print(f"ini adalah : {day}")
        names = ', '.join(jadwal_Wfo[day])
        # print(f"ini print  {jadwal_Wfo[day]}" )
        tree.insert("", tk.END, values=(day, names))
    
    print(jumlah_wfh)
    # jadwal_Wfo_copy = copy.deepcopy(jadwal_Wfo)
    copy_jadwal()
    jadwal_Wfo.clear() 
    reset_input()
    
    # update_dropdown()
    # update_tabel(days)
    # for day, names in jadwal_Wfo.items():
    #     print(f"{day} : {names}")
    
    # print(jumlah_wfh)
def copy_jadwal():
    try : 
        with open('jadwal_WFO.txt', 'r') as file:
            for line in file:
                line = line.strip()
                key, value = line.split(":")
                jadwal_Wfo_copy[key] = value.split(",")
    except:
        pass
            
    print(jadwal_Wfo_copy)

def reset_input():
    """Reset input fields to empty."""
    input_nama.delete(0, tk.END)
    input_max.delete(0, tk.END)
    input_max_wfo.delete(0, tk.END)
    
def load_jadwal():
    global jadwal_Wfo, anak_magang
    
    # Menghapus jadwal WFH yang ada
    jadwal_Wfo.clear()
    
    try:
        # Membaca file jadwal WFH
        with open("jadwal_WFO.txt", "r") as file:
            lines = file.readlines()
            
            # Memasukkan nama-nama anak magang dan jadwalnya ke dalam dictionary
            for line in lines:
                # Mengambil nama hari dan nama-nama yang dijadwalkan
                if ":" in line:
                    day, names = line.split(":")
                    names = names.strip()  # Menghapus spasi di awal dan akhir nama
                    jadwal_Wfo[day.strip()] = names.split(", ")  # Memisahkan nama-nama yang dipisah koma

        # Menampilkan kembali jadwal ke dalam Treeview
        for row in tree.get_children():
            tree.delete(row)
        
        for day, names in jadwal_Wfo.items():
            tree.insert("", tk.END, values=(day, ', '.join(names)))

        # Jika jadwal berhasil dimuat, memberikan info kepada user
        messagebox.showinfo("Sukses", "Jadwal WFH berhasil dimuat.")
        input_nama.focus_force()

    except FileNotFoundError:
        messagebox.showwarning("Anda belum punya jadwal", "Buat jadwal sekarang.")
        print("Fokus dikembalikan ke input_nama")
        input_nama.focus_force()
    except Exception as e:
        messagebox.showerror("Error", f"Terjadi kesalahan saat memuat jadwal: {e}")
        input_nama.focus_force()
# Hapus nama
'''
# def hapus_nama():
#     # days = days
#     global jadwal_Wfo
#     hapus_nama = nama_dropdown.get()
    
#     if not hapus_nama:
#         messagebox.showerror("Pilih Nama", "Silakan pilih nama yang ingin dihapus dari dropdown.")
#         return
    
#     for nama in jadwal_Wfo:
#         if(hapus_nama in jadwal_Wfo[nama]):
#             jadwal_Wfo[nama].remove(hapus_nama)
    
#     if hapus_nama in anak_magang:
#         anak_magang.remove(hapus_nama)
    
#     update_dropdown()
#     update_tabel(['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu'])

'''  


def download_jadwal_as_image():
    if not jadwal_Wfo_copy:
        messagebox.showwarning("No Data", "Jadwal WFH belum disimpan. Silakan simpan jadwal terlebih dahulu.")
        return
    
    if not messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin mendownload jadwal sebagai gambar?"):
        return

    days = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu']
    image_width = 1000
    margin = 40
    line_height = 80
    max_text_width = image_width - (2 * margin + 150)  # Width limit for text wrapping
    total_height = margin * 2 + 60  # Initial height for title and top margin
     
    # Calculate required height based on text wrapping
    for day in days:
        names = ', '.join(jadwal_Wfo_copy[day])
        wrapped_text = textwrap.wrap(f": {names}", width=80)
        total_height += line_height + (line_height // 2 * (len(wrapped_text) - 1))

    # Set image height dynamically based on total_height calculated
    image_height = total_height
    # Create a pastel-colored background
    image = Image.new("RGB", (image_width, image_height), (255, 239, 204))  # Light peach background
    draw = ImageDraw.Draw(image)

    try:
        font_title = ImageFont.truetype("arial.ttf", 28)
        font_text = ImageFont.truetype("arial.ttf", 20)
        font_highlight = ImageFont.truetype("arial.ttf", 22)
    except IOError:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()
        font_highlight = ImageFont.load_default()

    # Title
    title_text = "Jadwal WFO Anak PKL"
    draw.text((margin, margin), title_text, fill="#6B4F9E", font=font_title)  # Soft purple for the title

    # Draw a divider line below the title
    draw.line([(margin, margin + 40), (image_width - margin, margin + 40)], fill="#6B4F9E", width=2)

    # Writing schedule to the image
    y_offset = margin + 60
    for day in days:
        names = ', '.join(jadwal_Wfo_copy[day])
        
        # Wrap text to fit within the max width
        wrapped_text = textwrap.wrap(f": {names}", width=80)
        
        
        # print(f"ini adalah wrap {wrapped_text}") for line in wrapped_text
        # print(f"ini adalah wrap : {wrapped_text}")
        # Highlight for the day name with pastel colors
        highlight_color = (173, 216, 230)  # Light blue highlight
        box_height = line_height + (line_height // 2 * (len(wrapped_text) - 1))  # Adjust box height based on wrapped lines
        draw.rounded_rectangle([(margin - 5, y_offset - 5), (image_width - margin + 5, y_offset + box_height - 5)], radius=10, fill=highlight_color)

        # Draw the day name in a larger font
        draw.text((margin + 10, y_offset), day.capitalize(), fill="#2E8B57", font=font_highlight)  # Sea green for the day name

        # Draw each line of wrapped text
        text_y_offset = y_offset
        
        for line in wrapped_text:
            draw.text((margin + 150, text_y_offset), line, fill="#6B4F9E", font=font_text)  # Soft purple for the rest
            text_y_offset += line_height // 2  # Adjust line spacing

        y_offset += box_height
        
    
    # Save the image
    image.save("jadwal_WFO.png")
    messagebox.showinfo("Sukses", "Jadwal WFO berhasil disimpan sebagai gambar (jadwal_WFO.png).")

# function lain
'''
# def update_dropdown():
#     nama_dropdown['values'] = anak_magang
#     nama_dropdown.set("pilih nama")
    
# def update_tabel(days):
#     for row in tree.get_children():
#         tree.delete(row)
        
#     for day in days:
#         # print(day)
#         names = ', '.join(jadwal_WFH[day])
#         tree.insert("", tk.END, values=(day, names))
# # def regenerate_jadwal(){
# #     simpan_jadwal()
# # }
# # simpan_jadwal()

'''

window = tk.Tk()
window.title("Generator WFO")
window.geometry("500x600")

# Input orang
tk.Label(window, text ="Nama anak PKL (pisahkan dengan koma) : ").pack(pady=10)
input_nama = tk.Entry(window, width=50)
input_nama.pack()

tk.Label(window, text="Minimal WFH per-anak : ").pack(pady=10)
input_max = tk.Entry(window, width= 50)
input_max.pack()

tk.Label(window, text="Kapasitas WFO kantor : ").pack(pady=10)
input_max_wfo = tk.Entry(window,width=50)
input_max_wfo.pack()

save_button = tk.Button(window, text="Simpan Jadwal WFO", command=simpan_jadwal)
save_button.pack(pady=20)

# save_button = tk.Button(window, text="Load", command=load_jadwal)
# save_button.pack(pady=20)

download_button = tk.Button(window, text="Download Jadwal sebagai Gambar", command=download_jadwal_as_image)
download_button.pack(pady=10)




tree = ttk.Treeview(window, columns=("Hari", "Nama"), show='headings')
tree.heading("Hari", text="Hari")
tree.heading("Nama", text="Nama WFH")
tree.pack(expand=True, fill='both')

copy_jadwal()
load_jadwal()
window.mainloop()
# window.title("Penjadwalan WFH" )
# window.geometry("400x300")
# name_dropdown = ttk.Combobox(window, values=anak_magang)
# name_dropdown.pack()
# name_dropdown.set("Pilih nama")
# window.mainloop()

# hapus_nama()