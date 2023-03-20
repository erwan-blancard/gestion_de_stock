from tkinter import *
from tkinter import font
import mysql.connector
import tkinter.messagebox


class Product:

    def __init__(self, id: int, name: str, desc: str, price: int, amount: int, id_category: int):
        self.__id = id
        self.name = name
        self.desc = desc
        self.price = price
        self.amount = amount
        self.id_category = id_category

    def get_id(self):
        return self.__id

    def get_infos(self):
        return "ID: " + str(self.__id) + "  |  " + self.name + "  |  Prix: " + str(self.price) + "€  |  Quantité: " + str(self.amount) + "  |  Catégorie: " + get_category_name(self.id_category) + "  |  Description: " + self.desc


product_list: list[Product] = []
category_list: dict = {}        # ["name": id, etc]


def close_win(top):
    top.destroy()


def open_product_edit_window():
    items = item_list.curselection()
    if len(items) > 0:
        selected_product = product_list[items[0]]

        top = Toplevel(window)
        top.geometry("300x400")
        top.grab_set()
        top.resizable(width=False, height=False)

        label_name = Label(top, text="Nom:")
        label_name.pack(pady=2)

        name_field = Entry(top)
        name_field.insert(0, selected_product.name)
        name_field.pack(pady=4)

        label_desc = Label(top, text="Description:")
        label_desc.pack(pady=2)

        desc_field = Entry(top)
        desc_field.insert(0, selected_product.desc)
        desc_field.pack(pady=4)

        label_price = Label(top, text="Prix:")
        label_price.pack(pady=2)

        price_field = Entry(top)
        price_field.insert(0, str(selected_product.price))
        price_field.pack(pady=4)

        label_amount = Label(top, text="Quantité:")
        label_amount.pack(pady=2)

        amount_field = Entry(top)
        amount_field.insert(0, str(selected_product.amount))
        amount_field.pack(pady=4)

        # OptionMenu categories
        category_label = Label(top, text="Catégorie:", padx=16)
        category_label.pack(pady=2)
        category = StringVar()

        categories = []
        for cat in category_list:
            categories.append(cat)
        if len(categories) > 0:
            category.set(get_category_name(selected_product.id_category))
        else:
            categories.append("---")
        category_option = OptionMenu(top, category, *categories)
        category_option.pack(pady=4)

        button_validate = Button(
            top, text="Modifier", command=lambda: modify_item(
                top, selected_product.get_id(), name_field.get(), desc_field.get(), price_field.get(), amount_field.get(),
                get_category_id(category.get()))
        )
        button_validate.pack(pady=4)
        button_cancel = Button(top, text="Annuler", command=lambda: close_win(top))
        button_cancel.pack(pady=4)


def modify_item(top, id, name, desc, price, amount, id_category):
    if len(name) > 0 and len(desc) > 0 and len(price) > 0 and len(amount) > 0:
        try:
            db_cursor.execute("UPDATE produit SET nom = '"+name+"' WHERE id="+str(id)+";")
            db_cursor.execute("UPDATE produit SET description = '" + desc + "' WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE produit SET prix = " + price + " WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE produit SET quantite = " + amount + " WHERE id=" + str(id) + ";")
            db_cursor.execute("UPDATE produit SET id_categorie = " + str(id_category) + " WHERE id=" + str(id) + ";")
            db.commit()
            reload_items()
            close_win(top)
        except Exception as e:
            tkinter.messagebox.showerror("Erreur !", "Impossible de modifier le produit: " + str(e))


def open_product_add_window():
    top = Toplevel(window)
    top.geometry("300x400")
    top.grab_set()
    top.resizable(width=False, height=False)

    label_name = Label(top, text="Nom:")
    label_name.pack(pady=2)

    name_field = Entry(top)
    name_field.pack(pady=4)

    label_desc = Label(top, text="Description:")
    label_desc.pack(pady=2)

    desc_field = Entry(top)
    desc_field.pack(pady=4)

    label_price = Label(top, text="Prix:")
    label_price.pack(pady=2)

    price_field = Entry(top)
    price_field.pack(pady=4)

    label_amount = Label(top, text="Quantité:")
    label_amount.pack(pady=2)

    amount_field = Entry(top)
    amount_field.pack(pady=4)

    # OptionMenu categories
    category_label = Label(top, text="Catégorie:", padx=16)
    category_label.pack(pady=2)
    category = StringVar()

    categories = []
    for cat in category_list:
        categories.append(cat)
    if len(categories) > 0:
        category.set(categories[0])
    else:
        categories.append("---")
    category_option = OptionMenu(top, category, *categories)
    category_option.pack(pady=4)

    button_validate = Button(
        top, text="Ajouter", command=lambda: add_item(
            top, name_field.get(), desc_field.get(), price_field.get(), amount_field.get(), get_category_id(category.get()))
    )
    button_validate.pack(pady=4)
    button_cancel = Button(top, text="Annuler", command=lambda: close_win(top))
    button_cancel.pack(pady=4)


def add_item(top, name, desc, price, amount, id_category):
    if len(name) > 0 and len(desc) > 0 and len(price) > 0 and len(amount) > 0:
        try:
            db_cursor.execute("INSERT INTO produit (nom, description, prix, quantite, id_categorie) VALUES ('" + name + "', '" + desc + "', " + price + ", " + amount + ", " + str(id_category) + ");")
            db.commit()
            reload_items()
            close_win(top)
        except Exception as e:
            tkinter.messagebox.showerror("Erreur !", "Impossible d'ajouter le produit: " + str(e))


def open_product_remove_window():
    items = item_list.curselection()
    if len(items) > 0:
        product_index = items[0]
        if tkinter.messagebox.askyesno("Confirmer", "Supprimer le produit sélectionné ("+product_list[product_index].name+") ?"):
            try:
                db_cursor.execute("DELETE FROM produit WHERE id="+str(product_list[product_index].get_id())+";")
                db.commit()
            except Exception as e:
                tkinter.messagebox.showerror("Erreur !", "Impossible de supprimer le produit: " + str(e))
            reload_items()


def reload_items():
    global product_list
    global category_list
    product_list = []
    category_list = {}

    item_list.delete(0, END)

    try:
        db_cursor.execute("SELECT * FROM categorie;")
        # (id, nom)
        for category in db_cursor:
            category_list[category[1]] = category[0]

    except Exception as e:
        tkinter.messagebox.showerror("Erreur !", "Impossible d'actualiser la liste des catégories: " + str(e))
    try:
        db_cursor.execute("SELECT * FROM produit;")
        # (id, nom, description, prix, quantite, id_categorie)
        for product in db_cursor:
            print(product)
            new_product = Product(product[0], product[1], product[2], product[3], product[4], product[5])
            product_list.append(new_product)
            item_list.insert(END, new_product.get_infos())

    except Exception as e:
        tkinter.messagebox.showerror("Erreur !", "Impossible d'actualiser la liste des produits: " + str(e))


def get_category_name(id_category):
    for category in category_list:
        if category_list[category] == id_category:
            return category
    return str(id_category)


def get_category_id(name):
    for category in category_list:
        if category == name:
            return category_list[category]
    return name


# setup database access
try:
    db = mysql.connector.connect(host="localhost", user="root", password="root", database="boutique")
except Exception as e:
    tkinter.messagebox.showerror("Erreur !", "Impossible de se connecter au serveur: "+str(e))
    exit(-1)

db_cursor = db.cursor()
try:
    db_cursor.execute("USE boutique")
except Exception as e:
    tkinter.messagebox.showerror("Erreur !", "Impossible d'accéder à la base de données \"boutique\": "+str(e))
    db_cursor.close()
    exit(-1)

window = Tk(className="Tableau de bord")
font.nametofont("TkDefaultFont").configure(size=12)
window.geometry("500x600")
window.resizable(width=False, height=False)


item_list_frame = Frame(window, pady=16)
item_list = Listbox(item_list_frame, width=92, height=16)

item_list.grid(column=0, row=0, sticky=(N, W, E, S))
scrollbar = Scrollbar(item_list_frame, orient=VERTICAL, command=item_list.yview)
scrollbar.grid(column=1, row=0, sticky=(N, S))
item_list['yscrollcommand'] = scrollbar.set
item_list_frame.grid_columnconfigure(0, weight=1)
item_list_frame.grid_rowconfigure(0, weight=1)

add_item_button = Button(item_list_frame, text="Ajouter...", command=lambda: open_product_add_window())
add_item_button.grid(pady=10)
edit_item_button = Button(item_list_frame, text="Modifier...", command=lambda: open_product_edit_window())
edit_item_button.grid(pady=10)
remove_item_button = Button(item_list_frame, text="Supprimer...", command=lambda: open_product_remove_window())
remove_item_button.grid(pady=10)
reload_items_button = Button(item_list_frame, text="Actualiser...", command=lambda: reload_items())
reload_items_button.grid(pady=10)

item_list_frame.pack()

# loads products from db
reload_items()

window.mainloop()

db_cursor.close()
