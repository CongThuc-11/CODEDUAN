from tkinter import *
import os

class Sukien:
    def __init__(self, ngay, gio, mota):
        self.ngay = ngay
        self.gio = gio
        self.mota = mota

root = Tk()
events = []

def nutquaylai():
    back_to_menu_button = Button(root, text="Quay lại menu chính", font=('Arial', 12), command=mainmenu)
    back_to_menu_button.pack(pady=7)

# Hàm show main menu
def mainmenu():
    clear_root()
    o = Frame(root)
    o.pack()
    add_button = Button(o, text="Thêm lịch ngày", font=("arial", 20), command=themsukien)
    add_button.grid(row=0, column=0, padx=40, pady=75)

    delete_button = Button(o, text="Xóa lịch ngày", font=("arial", 20), command=xoalich)
    delete_button.grid(row=0, column=1)

    week_button = Button(o, text="Lập lịch tuần", font=("arial", 20), command=laplichtuan)
    week_button.grid(row=1, column=0)

    thoat_button = Button(o, text="Thoát", font=("arial", 20), command=root.quit)
    thoat_button.grid(row=1, column=1)

# Hàm show giao diện thêm sự kiện
def themsukien():
    clear_root()

    ngay_label = Label(root, text="Ngày (dd-mm-yyyy):", font=('arial', 12))
    ngay_label.pack(pady=10)
    ngay_entry = Entry(root)
    ngay_entry.pack()
    ngay_entry.focus()
    gio_label = Label(root, text="Giờ (HH:MM):", font=('arial', 12))
    gio_label.pack(pady=10)
    gio_entry = Entry(root)
    gio_entry.pack()

    mota_label = Label(root, text="Sự kiện:", font=('arial', 12))
    mota_label.pack(pady=10)
    mota_entry = Entry(root)
    mota_entry.pack()

    save_button = Button(root, text="Lưu sự kiện", font=('arial', 12), command=lambda: luusukien(ngay_entry.get(), gio_entry.get(), mota_entry.get()))
    save_button.pack(pady=10)

    nutquaylai()

# Hàm xóa
def xoalich():
    clear_root()
    event_list = Listbox(root, width=80, height=10)
    event_list.pack(pady=20)
    capnhat(event_list)

    def xoa():
        selected_index = event_list.curselection()
        if selected_index:
            index = selected_index[0]
            events.pop(index)
            capnhat(event_list)
    delete_button = Button(root, text="Xóa", font=('arial', 12), command=xoa)
    delete_button.pack()
    nutquaylai()

# Hàm xóa tất cả các widget ở cửa sổ cũ
def clear_root():
    for widget in root.winfo_children():
        widget.destroy()


# Hàm update sự kiện
def capnhat(event_list):
    # Xóa nội dung trong event_list
    event_list.delete(0, END)
    for i, event in enumerate(events, 1):
        event_list.insert(END, f"{i}. Ngày: {event.ngay}, Giờ: {event.gio}, Sự kiện: {event.mota}")

# Hàm lưu sự kiện
def luusukien(ngay, gio, mota):
    event = Sukien(ngay, gio, mota)
    events.append(event)
    capnhat(event_list)

# Hàm show danh sách sự kiện
event_list = Listbox(root)

def danhsachsukien():
    clear_root()
    event_list.pack()
    capnhat(event_list)
    nutquaylai()


# Hàm lưu sự kiện vào file
def luudulieuvaofile():
    with open("lst.txt", "w") as file:
        for event in events:
            file.write(f"ngay,{event.ngay},{event.gio},{event.mota}\n")

# Hàm đọc sự kiện từ file
def docfile():
    try:
        with open("lst.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 4 and parts[0] == "ngay":
                    _, ngay, gio, mota = parts
                    event = Sukien(ngay, gio, mota)
                    events.append(event)
        capnhat(event_list)
    except FileNotFoundError:
        pass

# Hàm lập lịch 1 tuần
luutru = "lst.txt"

def luudulieu():
    if not os.path.exists(luutru):
        with open(luutru, "w") as f:
            f.write("")

def laplichtuan():
    data = []
    with open(luutru, "r") as f:
        for i in f.readlines():
            data.append(i.strip())
    global event_list
    clear_root()
    tuan_button = Button(root, text="Lập lịch tuần", command=laplichtuan)
    tuan_button.pack()
    o = Frame(root)
    o.pack()
    for i in range(1, 8):
        thu_ngay = Label(o, text=f"Thứ {i + 1}" if i < 7 else "Chủ nhật")
        thu_ngay.grid(row=0, column=i)
        oghichu = Frame(o)
        oghichu.grid(row=1, column=i)
        for j in range(10):
            s = Entry(oghichu)
            s.grid(row=j, column=0)
    c = 0
    cnt = len(data)
    for i in range(1, 8):
        for j in range(10):
            test_data = o.grid_slaves(row=1, column=i)[0].grid_slaves(row=j, column=0)[0]
            if c < cnt:
                test_data.insert(0, data[c])
                c += 1
            else:
                break

    def luulich():
        notes = []
        for i in range(1, 8):
            for j in range(10):
                s = o.grid_slaves(row=1, column=i)[0].grid_slaves(row=j, column=0)[0]
                note = s.get()
                notes.append(note)
        with open(luutru, "w") as f:
            for note in notes:
                f.write(note + "\n")
    luu_button = Button(root, text="Thêm Lịch", font=("arial", 12), foreground="red", command=luulich)
    luu_button.pack(pady=7)
    nutquaylai()

# Đọc dữ liệu từ tệp khi khởi động chương trình
docfile()

root.title("Ứng dụng quản lý thời gian")
root.geometry("900x370")

luudulieu()

menu_button = Button(root, text="Menu chính", font=('Arial', 30), command=mainmenu)
menu_button.pack(padx=50, pady=130)

current_interface = danhsachsukien

root.mainloop()
