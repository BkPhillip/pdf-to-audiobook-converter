"""
PDF to Audiobook Converter
by Bryson Phillip
11/01/2022

"""
import PyPDF2
from gtts import gTTS
from tkinter import *
from tkinter import filedialog as fd


class App:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("300x300")
        self.window.resizable(False, False)
        self.open_pdf_button = Button(text="Select pdf", command=self.select_file)
        self.open_pdf_button.pack()
        self.pdf_title_label = Label(text="No File Selected")
        self.pdf_title_label.pack()
        self.window.mainloop()

    def select_file(self):
        filename = fd.askopenfilename(title="Select pdf",
                                      initialdir="/Users/BrysonPhillip")
        # Do nothing if no file is selected
        if filename == "":
            return
        filename_no_path = filename.split("/")[-1]
        self.pdf_title_label.configure(text=filename_no_path)
        self.convert_pdf_to_mp3(filename)

    def convert_pdf_to_mp3(self, file):
        # Create pdf file object
        pdf_file = open(file, "rb")

        # Create pdf reader object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        # Create page object and print extracted text for each page in pdf
        full_text = ""
        for page in range(pdf_reader.numPages):
            # Create a page object
            pdf_page = pdf_reader.getPage(page)

            # Create one text string
            full_text += pdf_page.extractText()

        tts = gTTS(full_text)

        tts.save("test.mp3")

        # Close the pdf file object
        pdf_file.close()


app = App()
