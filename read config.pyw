import json 
from tkinter import *
from tkinter import filedialog

#open the config file
config_path = filedialog.askopenfilename(initialdir = "./", title = "Select config file", filetypes = (("json files","*.json"),("all files","*.*")))

with open(config_path, "r") as f:
    config = json.load(f)
    f.close()


def submit():
    #get the values from the gui
    config["host"] = ip_entry.get()
    config["port"] = port_entry.get()
    config["username"] = username_entry.get()
    config["format"] = encoding_entry.get()

    #write the config file
    with open(config_path, "w") as f:
        json.dump(config, f)
        f.close()

tk = Tk()
tk.title("Config editor")
tk.geometry("500x500")

Label(tk, text="IP:").grid(row=1, column=0)
ip_entry = Entry(tk)
ip_entry.grid(row=1, column=1)
ip_entry.insert(0, config["host"])

Label(tk, text="Port:").grid(row=2, column=0)
port_entry = Entry(tk)
port_entry.grid(row=2, column=1)
port_entry.insert(0, config["port"])

Label(tk, text="Username:").grid(row=3, column=0)
username_entry = Entry(tk)
username_entry.grid(row=3, column=1)
username_entry.insert(0, config["username"])


Label(tk, text="encoding:").grid(row=4, column=0)
encoding_entry = Entry(tk)
encoding_entry.grid(row=4, column=1)
encoding_entry.insert(0, config["format"])

Button(tk, text="Submit", command=submit).grid(row=5, column=0)

tk.mainloop()