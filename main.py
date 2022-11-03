"""
PDF to Audiobook Converter
by Bryson Phillip
11/01/2022

A simple pdf to mp3 conversion app utilizing text to speech.

"""
import PyPDF2
from gtts import gTTS
from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
import os


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("pdf to mp3 converter")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.pdf_filename = None
        self.open_pdf_button = Button(text="Select pdf", command=self.select_file)
        self.open_pdf_button.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.pdf_title_label = Label(text="No File Selected")
        self.pdf_title_label.place(relx=0.5, rely=0.35, anchor=CENTER)
        self.convert_button = Button(text="Convert", command=lambda: self.convert_pdf_to_mp3(self.pdf_filename))
        self.success_label = Label(text="", foreground="green")
        self.success_label.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.window.mainloop()

    def select_file(self):
        # File dialog to select pdf to convert to mp3
        self.pdf_filename = fd.askopenfilename(title="Select pdf",
                                               initialdir="/Users/BrysonPhillip",
                                               filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        # Do nothing if no file is selected
        if self.pdf_filename == "":
            return
        # Remove success message if selecting another file after a successful conversion
        self.success_label.configure(text="")
        # Option to convert does not appear until file is selected
        self.convert_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        # Remove file path from filename for display
        filename_no_path = self.pdf_filename.split("/")[-1]
        # Update label with selected pdf
        self.pdf_title_label.configure(text=filename_no_path)

    def convert_pdf_to_mp3(self, file):
        self.success_label.configure(text="")
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

        # Create text to speech
        tts = gTTS(full_text)
        # Save text to speech to file
        tts.save("audio.mp3")

        # Close the pdf file object
        pdf_file.close()

        # File dialog to choose filename and destination
        mp3_filename = fd.asksaveasfilename(title="Save mp3",
                                            defaultextension=".mp3",
                                            initialdir="Users/BrysonPhillip/Downloads",
                                            filetypes=[("Mp3 Files", "*.mp3")]
                                            )
        if mp3_filename == '':  # asksaveasfile return None if dialog closed with "cancel"
            return
        # Open text to speech file
        main_file = open("audio.mp3", "rb").read()
        # Open file with custom name in desired path
        destination_file = open(mp3_filename, "wb+")
        # Write audio file to destination file
        destination_file.write(main_file)
        # Close files
        destination_file.close()
        # mp3 successfully saved message
        self.success_label.configure(text="mp3 successfully saved")
        # Delete temporary audio file after saved to desired destination
        os.remove("audio.mp3")


app = App()
