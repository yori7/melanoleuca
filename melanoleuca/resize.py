import tkinter as tk
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import copy

class FitImageFrame(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def set_image(self, image):
        self.image = image
        self._resize(self)
        self.canvas.bind("<Configure>", self._resize)

    def get_image(self):
        return self.image

    def _resize(self, event):
        image_size = self.image.size
        canvas_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
        diff = [canvas - image for canvas, image in zip(image_size, canvas_size)]
        max_diff = max(diff)
        max_index = diff.index(max_diff)
        min_index = max_index - 1
        min_diff = diff[min_index]
        changed_size = [0, 0]
        
        changed_size[max_index] = image_size[max_index] - max_diff
        changed_size[min_index] = changed_size[max_index] * image_size[min_index] / image_size[max_index]
        self.newimage = self.image.resize([round(i) for i in changed_size])
        imagetk = ImageTk.PhotoImage(image=self.newimage)
        self.canvas.photo = imagetk

        self.update()
        imagex = self.canvas.winfo_width() / 2
        imagey = self.canvas.winfo_height() / 2
        self.canvas.delete("all")
        self.canvas.create_image(imagex, imagey, image=imagetk)

    def close(self):
        self.canvas.delete("all")
        try:
            del self.image
        except AttributeError as e:
            pass

    def reload_canvas(self):
        self.canvas.delete("all")
        try:
            self._resize(self)
        except AttributeError as e:
            pass

class ScrollableFrame(tk.Frame):
    def __init__(self, parent, minimal_canvas_size):
        tk.Frame.__init__(self, parent)

        self.minimal_canvas_size = minimal_canvas_size

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=False)

        # 横スクロールバー
        hscrollbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hscrollbar.pack(fill=tk.X, side=tk.BOTTOM, expand=False)

        # Canvas
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
            yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # スクロールバーをCanvasに関連付け
        vscrollbar.config(command=self.canvas.yview)
        hscrollbar.config(command=self.canvas.xview)

        # Canvasの位置の初期化
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # スクロール範囲の設定
        self.canvas.config(scrollregion=(0, 0, self.minimal_canvas_size[0], self.minimal_canvas_size[1]))

        # Canvas内にフレーム作成
        self.interior = tk.Frame(self.canvas)
        self.canvas.create_window(0, 0, window=self.interior, anchor='nw')

        # Canvasの大きさを変える関数
        def _configure_interior(event):
            size = (max(self.interior.winfo_reqwidth(), self.minimal_canvas_size[0]),
                max(self.interior.winfo_reqheight(), self.minimal_canvas_size[1]))
            self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
            if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
                self.canvas.config(width = self.interior.winfo_reqwidth())
            if self.interior.winfo_reqheight() != self.canvas.winfo_height():
                self.canvas.config(height = self.interior.winfo_reqheight())

        # 内部フレームの大きさが変わったらCanvasの大きさを変える関数を呼び出す
        self.interior.bind('<Configure>', _configure_interior)