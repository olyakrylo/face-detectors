from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial
from FaceDetector import FaceDetector


allowed_tm_methods = ["TM_CCOEFF", "TM_CCORR", "TM_SQDIFF"]
img_width = 400
template_width = 200
big_img_width = 500


def openFn():
    filename = filedialog.askopenfilename(title='open')
    return filename


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("TM")
        self.window.geometry("1000x800")

        self.notebook = ttk.Notebook(self.window, width=1000, height=800)
        tm = ttk.Frame(self.notebook)
        vj = ttk.Frame(self.notebook)
        sym = ttk.Frame(self.notebook)
        self.notebook.add(tm, text="Template Matching")
        self.notebook.add(vj, text="Viola Jones")
        self.notebook.add(sym, text="Symmetry lines")

        self.data = {}

        self.method = StringVar(value="TM_CCOEFF")

        for i, value in enumerate(allowed_tm_methods):
            ttk.Radiobutton(tm, text=value, variable=self.method, value=value).grid(column=0, row=i, sticky=W)

        self.tm_image = ttk.Label(tm, width=50)
        self.tm_image.grid(column=0, row=4)
        self.template = ttk.Label(tm, width=25)
        self.template.grid(column=1, row=4)
        self.tm_result = ttk.Label(tm, width=50)
        self.tm_result.grid(column=2, row=4)

        Button(tm, text="open image", width=40, command=partial(self.open_img, img_width, "tm_image", self.tm_image)).grid(column=0, row=3)
        Button(tm, text="open template", width=20, command=partial(self.open_img, template_width, "template", self.template)).grid(column=1, row=3)
        Button(tm, text="go", width=40, command=self.start_tm).grid(column=2, row=3)

        self.vj_image = ttk.Label(vj, width=62)
        self.vj_image.grid(column=0, row=1)
        self.vj_result = ttk.Label(vj, width=62)
        self.vj_result.grid(column=1, row=1)

        Button(vj, text="open image", width=50, command=partial(self.open_img, big_img_width, "vj_image", self.vj_image)).grid(column=0, row=0)
        Button(vj, text="go", width=50, command=self.start_vj).grid(column=1, row=0)

        self.sym_image = ttk.Label(sym, width=62)
        self.sym_image.grid(column=0, row=1)
        self.sym_result = ttk.Label(sym, width=62)
        self.sym_result.grid(column=1, row=1)

        Button(sym, text="open image", width=50, command=partial(self.open_img, big_img_width, "sym_image", self.sym_image)).grid(column=0, row=0)
        Button(sym, text="go", width=50, command=self.start_sym).grid(column=1, row=0)

        self.notebook.grid(column=0, row=0)

    def start_sym(self):
        try:
            fd = FaceDetector(self.data["sym_image"])
            fd.sym_lines()
            img = Image.open("./result_sym.jpg")
            [width, height] = img.size
            img = img.resize((big_img_width, round(height * big_img_width / width)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.sym_result.configure(image=img)
            self.sym_result.image = img
        except Exception as e:
            print(e)
            messagebox.showinfo('error', 'select image')

    def start_vj(self):
        try:
            fd = FaceDetector(self.data["vj_image"])
            fd.viola_jones()
            img = Image.open("./result_vj.jpg")
            [width, height] = img.size
            img = img.resize((big_img_width, round(height * big_img_width / width)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.vj_result.configure(image=img)
            self.vj_result.image = img
        except Exception as e:
            print(e)
            messagebox.showinfo('error', 'select image')

    def start_tm(self):
        try:
            fd = FaceDetector(self.data["tm_image"])
            fd.template_matching(self.data["template"], self.method.get())
            img = Image.open("./result_tm.jpg")
            [width, height] = img.size
            img = img.resize((img_width, round(height * img_width / width)), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.tm_result.configure(image=img)
            self.tm_result.image = img
        except:
            messagebox.showinfo('error', 'select both template and image')

    def open_img(self, expected_width, field, item):
        x = openFn()
        img = Image.open(x)
        [width, height] = img.size
        img = img.resize((expected_width, round(height * expected_width / width)), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        item.configure(image=img)
        item.image = img

        self.data[field] = x

    def start_loop(self):
        self.window.mainloop()


app = App()
app.start_loop()
