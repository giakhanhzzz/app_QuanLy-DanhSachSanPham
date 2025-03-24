import tkinter as tk
from tkinter import ttk, messagebox
import json
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Hàm đọc/ghi file JSON
def read_products():
    try:
        with open("products.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_products(data):
    with open("products.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Thêm sản phẩm
def add_product(products, update_ui_callback, name_var, desc_var, price_var, stock_var, image_var, add_window):
    try:
        name, desc, price, stock, image = name_var.get(), desc_var.get(), float(price_var.get()), int(stock_var.get()), image_var.get()
        price = int(price) if price.is_integer() else price
        new_product = {"id": len(products) + 1, "name": name, "description": desc, "price": price, "stock": stock, "image": image}
        products.append(new_product)
        write_products(products)
        update_ui_callback(products)
        add_window.destroy()
        messagebox.showinfo("Thành công", "Đã thêm sản phẩm!")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập thông tin hợp lệ!")

# Xóa sản phẩm
def delete_product(products, update_ui_callback, main_frame, detail_frame, index):
    del products[index]
    write_products(products)
    update_ui_callback(products)
    detail_frame.pack_forget()
    main_frame.pack(expand=True, fill="both")
    messagebox.showinfo("Thành công", "Đã xóa sản phẩm!")

# Cập nhật sản phẩm
def update_product(products, update_ui_callback, name_var, desc_var, price_var, stock_var, image_var, main_frame, detail_frame, index):
    try:
        name, desc, price, stock, image = name_var.get(), desc_var.get(), float(price_var.get()), int(stock_var.get()), image_var.get()
        price = int(price) if price.is_integer() else price
        products[index].update({"name": name, "description": desc, "price": price, "stock": stock, "image": image})
        write_products(products)
        update_ui_callback(products)
        detail_frame.pack_forget()
        main_frame.pack(expand=True, fill="both")
        messagebox.showinfo("Thành công", "Đã cập nhật sản phẩm!")
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập thông tin hợp lệ!")

# Tìm kiếm sản phẩm
def search_products(products, update_ui_callback, search_var):
    keyword = search_var.get().lower()
    filtered = [p for p in products if keyword in p["name"].lower() or keyword in p["description"].lower()]
    update_ui_callback(filtered)
    if not filtered:
        messagebox.showinfo("Kết quả", "Không tìm thấy sản phẩm!")

# Mở cửa sổ thêm sản phẩm
def open_add_window(products, update_ui_callback):
    add_window = tk.Toplevel()
    add_window.title("Thêm sản phẩm")
    add_window.geometry("300x350")

    tk.Label(add_window, text="Tên sản phẩm").pack(pady=5)
    name_var = tk.StringVar()
    tk.Entry(add_window, textvariable=name_var).pack()

    tk.Label(add_window, text="Mô tả").pack(pady=5)
    desc_var = tk.StringVar()
    tk.Entry(add_window, textvariable=desc_var).pack()

    tk.Label(add_window, text="Giá (USD)").pack(pady=5)
    price_var = tk.StringVar()
    tk.Entry(add_window, textvariable=price_var).pack()

    tk.Label(add_window, text="Số lượng").pack(pady=5)
    stock_var = tk.StringVar()
    tk.Entry(add_window, textvariable=stock_var).pack()

    tk.Label(add_window, text="URL ảnh").pack(pady=5)
    image_var = tk.StringVar()
    tk.Entry(add_window, textvariable=image_var).pack()

    tk.Button(add_window, text="Thêm", command=lambda: add_product(products, update_ui_callback, name_var, desc_var, price_var, stock_var, image_var, add_window)).pack(pady=10)

# Hiển thị chi tiết sản phẩm
def show_detail(products, update_ui_callback, main_frame, detail_frame, index):
    product = products[index]

    main_frame.pack_forget()
    for widget in detail_frame.winfo_children():
        widget.destroy()

    # Frame chính cho chi tiết
    content_frame = tk.Frame(detail_frame, bg="#f0f0f0")
    content_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Phần thông tin cho người xem
    info_display_frame = tk.LabelFrame(content_frame, text="Thông tin sản phẩm", font=("Arial", 12, "bold"), bg="#e8f4f8")
    info_display_frame.pack(fill="x", pady=(0, 10))

    # Frame cho ảnh và thông tin
    info_content = tk.Frame(info_display_frame, bg="#e8f4f8")
    info_content.pack(fill="x", padx=10, pady=10)

    # Ảnh
    image_frame = tk.Frame(info_content, bg="#e8f4f8")
    image_frame.pack(side="left", padx=10)
    try:
        response = requests.get(product["image"])
        img_data = BytesIO(response.content)
        img = Image.open(img_data)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        tk.Label(image_frame, image=photo, bg="#e8f4f8").pack(anchor="nw")
        detail_frame.image = photo
    except Exception as e:
        tk.Label(image_frame, text=f"Lỗi tải ảnh: {str(e)}", bg="#e8f4f8").pack(anchor="nw")

    # Thông tin
    info_text_frame = tk.Frame(info_content, bg="#e8f4f8")
    info_text_frame.pack(side="left", fill="both", expand=True)
    tk.Label(info_text_frame, text=f"Tên: {product['name']}", font=("Arial", 14, "bold"), bg="#e8f4f8").pack(anchor="w")
    tk.Label(info_text_frame, text=f"Giá: {product['price']} USD", font=("Arial", 12), bg="#e8f4f8").pack(anchor="w")
    tk.Label(info_text_frame, text=f"Mô tả: {product['description']}", font=("Arial", 12), bg="#e8f4f8").pack(anchor="w")
    tk.Label(info_text_frame, text=f"Số lượng còn trong kho: {product['stock']}", font=("Arial", 12), bg="#e8f4f8").pack(anchor="w")

    # Phần chỉnh sửa cho người bán
    edit_frame = tk.LabelFrame(content_frame, text="Chỉnh sửa thông tin (Dành cho người bán)", font=("Arial", 12, "bold"), bg="#f0f0f0")
    edit_frame.pack(fill="x")

    tk.Label(edit_frame, text="Tên sản phẩm", bg="#f0f0f0").pack(anchor="w")
    name_var = tk.StringVar(value=product["name"])
    tk.Entry(edit_frame, textvariable=name_var, width=40).pack(fill="x")

    tk.Label(edit_frame, text="Mô tả", bg="#f0f0f0").pack(anchor="w")
    desc_var = tk.StringVar(value=product["description"])
    tk.Entry(edit_frame, textvariable=desc_var, width=40).pack(fill="x")

    tk.Label(edit_frame, text="Giá (USD)", bg="#f0f0f0").pack(anchor="w")
    price_var = tk.StringVar(value=product["price"])
    tk.Entry(edit_frame, textvariable=price_var, width=40).pack(fill="x")

    tk.Label(edit_frame, text="Số lượng", bg="#f0f0f0").pack(anchor="w")
    stock_var = tk.StringVar(value=product["stock"])
    tk.Entry(edit_frame, textvariable=stock_var, width=40).pack(fill="x")

    tk.Label(edit_frame, text="URL ảnh", bg="#f0f0f0").pack(anchor="w")
    image_var = tk.StringVar(value=product["image"])
    tk.Entry(edit_frame, textvariable=image_var, width=40).pack(fill="x")

    # Frame cho các nút
    button_frame = tk.Frame(edit_frame, bg="#f0f0f0")
    button_frame.pack(pady=10, fill="x")

    tk.Button(button_frame, text="Cập nhật", width=10, bg="#4CAF50", fg="white", command=lambda: update_product(products, update_ui_callback, name_var, desc_var, price_var, stock_var, image_var, main_frame, detail_frame, index)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Xóa", width=10, bg="#f44336", fg="white", command=lambda: delete_product(products, update_ui_callback, main_frame, detail_frame, index)).pack(side="left", padx=5)
    tk.Button(button_frame, text="Back", width=10, bg="#2196F3", fg="white", command=lambda: [detail_frame.pack_forget(), main_frame.pack(expand=True, fill="both")]).pack(side="left", padx=5)

    detail_frame.pack(expand=True, fill="both")

# Hiển thị danh sách sản phẩm dạng thẻ
def display_products(products, canvas_frame, main_frame, detail_frame):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    row = 0
    col = 0
    for i, product in enumerate(products):
        # Frame cho mỗi sản phẩm (dạng thẻ)
        card_frame = tk.Frame(canvas_frame, bd=2, relief="groove", bg="#ffffff", width=300, height=400)
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card_frame.grid_propagate(False)

        # Ảnh sản phẩm
        try:
            response = requests.get(product["image"])
            img_data = BytesIO(response.content)
            img = Image.open(img_data)
            img = img.resize((150, 150), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            tk.Label(card_frame, image=photo, bg="#ffffff").pack(pady=5)
            card_frame.image = photo  # Giữ tham chiếu
        except:
            tk.Label(card_frame, text="Không tải được ảnh", bg="#ffffff").pack(pady=5)

        # Thông tin sản phẩm
        tk.Label(card_frame, text=product["name"], font=("Arial", 12, "bold"), bg="#ffffff").pack()
        tk.Label(card_frame, text=f"Giá: {product['price']} USD", font=("Arial", 10), bg="#ffffff").pack()
        tk.Label(card_frame, text=f"Mô tả: {product['description']}", font=("Arial", 10), bg="#ffffff", wraplength=250).pack()
        tk.Label(card_frame, text=f"Số lượng còn trong kho: {product['stock']}", font=("Arial", 10), bg="#ffffff").pack()

        # Nút xem chi tiết
        tk.Button(card_frame, text="Xem chi tiết", bg="#2196F3", fg="white", command=lambda idx=i: show_detail(products, lambda p: display_products(p, canvas_frame, main_frame, detail_frame), main_frame, detail_frame, idx)).pack(pady=5)

        col += 1
        if col > 2:  # 3 thẻ mỗi hàng
            col = 0
            row += 1

# Giao diện chính
def main():
    products = read_products()

    root = tk.Tk()
    root.title("Quản Lý Sản Phẩm - Cửa Hàng Trực Tuyến")
    root.geometry("1000x600")
    root.configure(bg="#f0f0f0")

    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(expand=True, fill="both")

    # Thanh tìm kiếm
    search_frame = tk.Frame(main_frame, bg="#f0f0f0")
    search_frame.pack(pady=10)
    search_var = tk.StringVar()
    tk.Entry(search_frame, textvariable=search_var, width=30).pack(side=tk.LEFT, padx=5)
    tk.Button(search_frame, text="Tìm kiếm", bg="#2196F3", fg="white", command=lambda: search_products(products, lambda p: display_products(p, canvas_frame, main_frame, detail_frame), search_var)).pack(side=tk.LEFT)

    tk.Button(search_frame, text="Thêm sản phẩm", bg="#4CAF50", fg="white", command=lambda: open_add_window(products, lambda p: display_products(p, canvas_frame, main_frame, detail_frame))).pack(side=tk.LEFT, padx=5)

    # Canvas để chứa danh sách sản phẩm (có thể cuộn)
    canvas = tk.Canvas(main_frame, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    canvas_frame = tk.Frame(canvas, bg="#f0f0f0")

    # Khai báo detail_frame trước khi gọi display_products
    detail_frame = tk.Frame(root, bg="#f0f0f0")

    canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", expand=True, fill="both")
    canvas.create_window((0, 0), window=canvas_frame, anchor="nw")

    # Hiển thị sản phẩm
    display_products(products, canvas_frame, main_frame, detail_frame)

    # Cập nhật vùng cuộn
    canvas_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    root.mainloop()

if __name__ == "__main__":
    main()