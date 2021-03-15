from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import ImageTk, Image
from functools import partial
from FaceDetector import FaceDetector


allowed_methods = ["TM_CCOEFF", "TM_CCORR", "TM_SQDIFF"]


def openFn():
    filename = filedialog.askopenfilename(title='open')
    return filename


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("TM")
        self.window.geometry("1100x800")

        self.notebook = ttk.Notebook(self.window, width=1100, height=800)
        tm = ttk.Frame(self.notebook)
        vj = ttk.Frame(self.notebook)
        self.notebook.add(tm, text="Template Matching")
        self.notebook.add(vj, text="Viola Jones")

        self.data = {}

        self.method = StringVar(value="TM_CCOEFF")

        for i, value in enumerate(allowed_methods):
            ttk.Radiobutton(tm, text=value, variable=self.method, value=value).grid(column=0, row=i, sticky=W)

        self.tm_image = ttk.Label(tm)
        self.tm_image.grid(column=0, row=4)
        self.template = ttk.Label(tm)
        self.template.grid(column=1, row=4)
        self.tm_result = ttk.Label(tm)
        self.tm_result.grid(column=2, row=4)

        Button(tm, text="open image", width=40, command=partial(self.open_img, 400, "tm_image", self.tm_image)).grid(column=0, row=3)
        Button(tm, text="open template", width=20, command=partial(self.open_img, 200, "template", self.template)).grid(column=1, row=3)
        Button(tm, text="go", width=40, command=self.start_tm).grid(column=2, row=3)

        self.vj_image = ttk.Label(vj)
        self.vj_image.grid(column=0, row=1)
        self.vj_result = ttk.Label(vj)
        self.vj_result.grid(column=1, row=1)

        Button(vj, text="open image", width=50, command=partial(self.open_img, 500, "vj_image", self.vj_image)).grid(column=0, row=0)
        Button(vj, text="go", width=50, command=self.start_vj).grid(column=1, row=0)

        self.notebook.grid(column=0, row=0)

    def start_vj(self):
        try:
            fd = FaceDetector(self.data["vj_image"])
            fd.viola_jones()
            img = Image.open("./result_vj.jpg")
            [width, height] = img.size
            img = img.resize((500, round(height * 500 / width)), Image.ANTIALIAS)
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
            img = img.resize((400, round(height * 400 / width)), Image.ANTIALIAS)
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
