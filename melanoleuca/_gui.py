import os
from os.path import expanduser
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from functools import partial
import melanoleuca
import resize
from myIterator import MyIterator


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        master.geometry("570x370+100+100")
        self.create_widgets()

    # Widgets
    def create_widgets(self):
        self.create_filemenu()
        self.create_RGB_input()
        self.create_status()
        self.create_main_frame()

    def create_filemenu(self):
        self.top_menu = tk.Menu(self.master, tearoff=0)
        self.file_menu = tk.Menu(self.top_menu, tearoff=0)

        self.top_menu.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="Open Files", command=partial(open_files, self))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save all", command=partial(save_all, self))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Reload", command=partial(reload_canvas, self))
        self.file_menu.add_command(label="Close", command=partial(close, self))

        self.master.config(menu=self.top_menu)

#    def create_top(self):
#        self.rgb_area = tk.Frame(self.master, bg="gray20", height=10)
#        self.rgb_area.pack(side=tk.TOP, fill=tk.X)
#        self.create_RGB_input()

    def create_RGB_input(self):
        self.rgb_area = tk.Frame(self.master, bg="gray20")
        self.rgb_area.pack(side=tk.TOP, fill=tk.X)
        #Min
        self.min_txt = tk.Label(self.rgb_area, text="Min", fg="black")
        self.min_txt.grid(column=0, row=0, sticky=tk.NSEW)

        self.min_r_frame = tk.Frame(self.rgb_area, bg="red")
        self.min_r_txt = tk.Label(self.min_r_frame, text="R", fg="white", bg="red")
        self.min_r_entry = tk.Entry(self.min_r_frame, width=5)
        self.min_r_frame.grid(column=1, row=0, sticky=tk.NSEW)
        self.min_r_txt.pack(side=tk.LEFT)
        self.min_r_entry.pack(side=tk.LEFT)

        self.min_g_frame = tk.Frame(self.rgb_area, bg="green")
        self.min_g_txt = tk.Label(self.min_g_frame, text="G", fg="white", bg="green")
        self.min_g_entry = tk.Entry(self.min_g_frame, width=5)
        self.min_g_frame.grid(column=2, row=0, sticky=tk.NSEW)
        self.min_g_txt.pack(side=tk.LEFT)
        self.min_g_entry.pack(side=tk.LEFT)

        self.min_b_frame = tk.Frame(self.rgb_area, bg="blue")
        self.min_b_txt = tk.Label(self.min_b_frame, text="B", fg="white", bg="blue")
        self.min_b_entry = tk.Entry(self.min_b_frame, width=5)
        self.min_b_frame.grid(column=3, row=0, sticky=tk.NSEW)
        self.min_b_txt.pack(side=tk.LEFT)
        self.min_b_entry.pack(side=tk.LEFT)

        #Max
        self.max_txt = tk.Label(self.rgb_area, text="Max", fg="black")
        self.max_txt.grid(column=4, row=0, sticky=tk.NSEW)

        self.max_r_frame = tk.Frame(self.rgb_area, bg="red")
        self.max_r_txt = tk.Label(self.max_r_frame, text="R", fg="white", bg="red")
        self.max_r_entry = tk.Entry(self.max_r_frame, width=5)
        self.max_r_frame.grid(column=5, row=0, sticky=tk.NSEW)
        self.max_r_txt.pack(side=tk.LEFT)
        self.max_r_entry.pack(side=tk.LEFT)

        self.max_g_frame = tk.Frame(self.rgb_area, bg="green")
        self.max_g_txt = tk.Label(self.max_g_frame, text="G", fg="white", bg="green")
        self.max_g_entry = tk.Entry(self.max_g_frame, width=5)
        self.max_g_frame.grid(column=6, row=0, sticky=tk.NSEW)
        self.max_g_txt.pack(side=tk.LEFT)
        self.max_g_entry.pack(side=tk.LEFT)

        self.max_b_frame = tk.Frame(self.rgb_area, bg="blue")
        self.max_b_txt = tk.Label(self.max_b_frame, text="B", fg="white", bg="blue")
        self.max_b_entry = tk.Entry(self.max_b_frame, width=5)
        self.max_b_frame.grid(column=7, row=0, sticky=tk.NSEW)
        self.max_b_txt.pack(side=tk.LEFT)
        self.max_b_entry.pack(side=tk.LEFT)

        self.min_r_entry.insert(0, "0")
        self.min_g_entry.insert(0, "0")
        self.min_b_entry.insert(0, "0")
        self.max_r_entry.insert(0, "255")
        self.max_g_entry.insert(0, "255")
        self.max_b_entry.insert(0, "255")

        #Apply button
        self.apply = tk.Button(self.rgb_area, text="Apply", fg="black", bg="#c1ffc1")
        self.apply.grid(column=8, row=0, sticky=tk.NSEW)

        self.rgb_area.grid_columnconfigure(0, weight=20)
        self.rgb_area.grid_columnconfigure(1, weight=100)
        self.rgb_area.grid_columnconfigure(2, weight=100)
        self.rgb_area.grid_columnconfigure(3, weight=100)
        self.rgb_area.grid_columnconfigure(4, weight=20)
        self.rgb_area.grid_columnconfigure(5, weight=100)
        self.rgb_area.grid_columnconfigure(6, weight=100)
        self.rgb_area.grid_columnconfigure(7, weight=100)
        self.rgb_area.grid_columnconfigure(4, weight=20)

    def create_status(self):
        self.bottom_area = tk.Frame(self.master, bg="gray20", height=20)
        self.bottom_area.pack(side=tk.BOTTOM, fill=tk.X)

        self.status_txt = tk.StringVar(self.bottom_area, value="Start Melanoleuca.")
        #status_txt.pack(fill=tk.X)

    def create_main_frame(self):
        self.main_frame = tk.Frame(self.master, bg="black")
        
        self.left_frame = tk.Frame(self.main_frame, bg="gray95", bd=1, relief=tk.SOLID)
        self.right_frame = tk.Frame(self.main_frame, bg="gray95", bd=1, relief=tk.SOLID)
        self.left_frame.grid(column=0, row=0, sticky=tk.NSEW)
        self.right_frame.grid(column=1, row=0, sticky=tk.NSEW)

        self.main_frame.pack(expand=True, fill=tk.BOTH)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        self.left_canvas_frame = resize.FitImageFrame(self.left_frame)
        self.left_canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_canvas_frame = resize.FitImageFrame(self.right_frame)
        self.right_canvas_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#Functions
def open_files(root):
    file_type = [("All Files", "*"), ("BMP", "*.bmp"), ("TIFF", "*.tiff"), ("PNG", "*.png"), ("JPEG","*.jpg",)]
    directory = os.path.abspath(expanduser("~"))
    root.read_file_name = filedialog.askopenfilename(filetypes=file_type, initialdir=directory)
    if len(root.read_file_name) != 0:
        root.left_img = MyIterator([Image.open(root.read_file_name)])
        root.left_canvas_frame.set_image(root.left_img.get(0))
        root.right_canvas_frame.close()
        root.status_txt.set("Open image file.")
        root.apply_id = root.apply.bind("<Button-1>", partial(apply_func, root))

def save(root):
    pass

def save_all(root):
    directory = os.path.abspath(expanduser("~"))
    dirname = filedialog.askdirectory(initialdir = directory)
    basename = os.path.basename(root.read_file_name)
    mark_name = dirname + "/" + basename + "_mark.jpg"
    BW_name = dirname + "/" + basename + "_BW.jpg"
    try:
        left = root.left_canvas_frame.get_image()
        right = root.right_canvas_frame.get_image()
    except ddsdsds:
        pass
    else:
        left.save(mark_name)
        right.save(BW_name)

def close(root):
    root.left_canvas_frame.close()
    root.right_canvas_frame.close()
    root.apply.unbind("<Button-3>", root.apply_id)

def apply_func(root, event):
    try:
        r_min = int(root.min_r_entry.get())
        g_min = int(root.min_g_entry.get())
        b_min = int(root.min_b_entry.get())
        r_max = int(root.max_r_entry.get())
        g_max = int(root.max_g_entry.get())
        b_max = int(root.max_b_entry.get())
    except ValueError as e:
        root.status_txt.set("RGB must be Integer")
        print(e)
    else:
        fname = root.read_file_name
        left_image, right_image = melanoleuca.change_img(fname, r_min, g_min, b_min, r_max, b_max, g_max)
        root.left_img.add(left_image)
        root.left_canvas_frame.set_image(root.left_img.next())
        root.right_canvas_frame.set_image(right_image)
        root.status_txt.set("Extract specifeied RGB area.")

def redo(root, event):
    pass

def undo(root, event):
    pass

def reload_canvas(root):
    root.left_canvas_frame.reload_canvas()
    root.right_canvas_frame.reload_canvas()
    
