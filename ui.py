from tkinter import *
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from functools import partial
from TemplateMatcher import TemplateMatcher


allowed_methods = ["TM_CCOEFF", "TM_CCORR", "TM_SQDIFF"]


def openFn():
    filename = filedialog.askopenfilename(title='open')
    return filename


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("TM")
        self.window.geometry("1500x800")

        self.data = {}

        self.method = StringVar(value="TM_CCOEFF")

        for i, value in enumerate(allowed_methods):
            Radiobutton(text=value, variable=self.method, value=value).grid(column=0, row=i, sticky=W)

        self.image = Label(self.window)
        self.image.grid(column=0, row=4)
        self.template = Label(self.window)
        self.template.grid(column=1, row=4)
        self.result = Label(self.window)
        self.result.grid(column=2, row=4)

        Button(self.window, text="open image", command=partial(self.open_img, 500, "image")).grid(column=0, row=3)
        Button(self.window, text="open template", command=partial(self.open_img, 300, "template")).grid(column=1, row=3)
        Button(self.window, text="go", command=self.start).grid(column=2, row=3)

    def start(self):
        try:
            tm = TemplateMatcher(self.data["template"])
            tm.exec(self.data["image"], self.method.get())
            img = Image.open("./result.jpg")
            [width, height] = img.size
            img = img.resize((round(width * 500 / height), 500), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)

            self.result.configure(image=img)
            self.result.image = img
        except:
            messagebox.showinfo('error', 'select both template and image')

    def open_img(self, expected_height, field):
        x = openFn()
        img = Image.open(x)
        [width, height] = img.size
        img = img.resize((round(width * expected_height / height), expected_height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        item = self.template if field == "template" else self.image
        item.configure(image=img)
        item.image = img

        self.data[field] = x

    def start_loop(self):
        self.window.mainloop()


app = App()
app.start_loop()
