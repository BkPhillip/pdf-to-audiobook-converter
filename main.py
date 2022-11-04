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
import os


class App:
    def __init__(self):
        self.window = Tk()
        self.window.title("pdf to mp3 converter")
        self.window.geometry("300x200")
        self.window.resizable(False, False)
        self.pdf_filename = ""
        # Button to select pdf file
        self.open_pdf_button = Button(text="Select pdf", command=self.select_file)
        self.open_pdf_button.place(relx=0.5, rely=0.10, anchor=CENTER)
        # Label showing selected pdf file selected if one selected
        self.pdf_title_label = Label(text="No File Selected")
        self.pdf_title_label.place(relx=0.5, rely=0.25, anchor=CENTER)
        # Page selector Radio Buttons, all pages or select which pages
        self.which_pages_to_convert = StringVar()
        self.all_pages_radio_button = Radiobutton(self.window,
                                                  text="All pages",
                                                  value="all",
                                                  variable=self.which_pages_to_convert,
                                                  command=self.disable_select,
                                                  )
        self.all_pages_radio_button.place(relx=0.2,
                                          rely=0.35,
                                          anchor=W)
        self.select_pages_radio_button = Radiobutton(self.window,
                                                     text="",
                                                     value="selected",
                                                     variable=self.which_pages_to_convert,
                                                     command=self.enable_selected,
                                                     )
        self.select_pages_radio_button.place(relx=0.2,
                                             rely=0.5,
                                             anchor=W)
        self.which_pages_to_convert.set("all")
        # From and entry fields in the select pages radio button
        self.from_page = IntVar()
        self.from_label = Label(text="from:", state="disabled")
        self.from_label.place(relx=0.33, rely=0.50, anchor=CENTER)
        self.from_entry = Entry(self.window, width=3, state="disabled")
        self.from_entry.place(relx=0.45, rely=0.5, anchor=CENTER)
        self.to_page = IntVar()
        self.to_label = Label(text="to:", state="disabled")
        self.to_label.place(relx=0.55, rely=0.5, anchor=CENTER)
        self.to_entry = Entry(self.window, width=3, state="disabled")
        self.to_entry.place(relx=0.64, rely=0.5, anchor=CENTER)
        self.select_pages_field = [self.from_label, self.from_entry, self.to_label, self.to_entry]
        # Button to convert pdf to mp3
        self.convert_button = Button(text="Convert", command=lambda: self.convert_pdf_to_mp3(self.pdf_filename))
        # Conversion status label
        self.success_label = Label(text="", foreground="green")
        self.success_label.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.window.mainloop()

    def select_file(self):
        # File dialog to select pdf to convert to mp3
        self.pdf_filename = fd.askopenfilename(title="Select pdf",
                                          initialdir="/Users/BrysonPhillip",
                                          filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
        if self.pdf_filename == "":  # Do nothing if no file is selected
            return
        # Remove success message if selecting another file after a successful conversion
        self.success_label.configure(text="")
        # Option to convert does not appear until file is selected
        self.convert_button.place(relx=0.5, rely=0.65, anchor=CENTER)
        # Remove file path from filename for display
        filename_no_path = self.pdf_filename.split("/")[-1]
        # Update label with selected pdf
        self.pdf_title_label.configure(text=f"filename: {filename_no_path}")
        # Get total number of pages of pdf
        total_pages = self.get_total_number_of_pages(self.pdf_filename)
        # Update last page number of document to the 'to:' entry widget
        if self.to_entry['state'] == "disabled":
            self.to_entry.configure(state="normal")
            self.update_last_page(total_pages)
            self.to_entry.configure(state="disabled")
        else:
            self.update_last_page(total_pages)

    # This function uses text to speech to create an audio file from the text pulled from the pdf
    def convert_pdf_to_mp3(self, pdf_filename):
        self.success_label.configure(text="")  # Remove previous success message
        starting_page = int(self.from_entry.get()) - 1
        ending_page = int(self.to_entry.get()) - 1
        # Add selected pages text to self.full_text
        text_to_convert = self.create_text_string(pdf_filename, starting_page, ending_page)
        tts = gTTS(text_to_convert)  # Create text to speech
        tts.save("audio.mp3")  # Save text to speech to file
        self.save_mp3()  # Run save_mp3 function to save to disc

    # This function opens the file dialog to chose filename and destination and save the audio file there
    def save_mp3(self):
        # File dialog to choose filename and destination
        mp3_filename = fd.asksaveasfilename(title="Save mp3",
                                            defaultextension=".mp3",
                                            initialdir="Users/BrysonPhillip/Downloads",
                                            filetypes=[("Mp3 Files", "*.mp3")]
                                            )
        if mp3_filename == '':  # asksaveasfile return None if dialog closed with "cancel"
            return
        main_file = open("audio.mp3", "rb").read()  # Open text to speech file
        destination_file = open(mp3_filename, "wb+")  # Open file with custom name in desired path
        destination_file.write(main_file)  # Write audio file to destination file
        destination_file.close()  # Close file
        # Update label to show mp3 successfully saved
        self.success_label.configure(text="mp3 successfully saved")
        os.remove("audio.mp3")  # Delete temporary audio file after saved to desired destination

    # This function updates the number in the 'to' entry field to show last page of pdf
    def update_last_page(self, num_pages):
        self.to_entry.delete(0, END)
        self.to_entry.insert(0, num_pages)

    # This function disables the from and to page entry widgets when 'all pages' option selected
    def disable_select(self):
        for widget in self.select_pages_field:
            widget.configure(state="disabled")
            widget.update()

    # This function enables the from and to page entry widgets when selected which pages to print
    def enable_selected(self):
        for widget in self.select_pages_field:
            widget.configure(state="normal")
            widget.update()

    def get_total_number_of_pages(self, pdf_filename):
        pdf_file = open(pdf_filename, "rb")  # Create pdf file object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)  # Create pdf reader object
        number_of_pages = pdf_reader.numPages  # Return total number of pages
        pdf_file.close()  # Close the pdf file object
        return number_of_pages

    def create_text_string(self, pdf_name, from_page, to_page):
        pdf_file = open(pdf_name, "rb")  # Create pdf file object
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)  # Create pdf reader object
        # Get each page of pdf and extract text to string variable
        full_text = ""
        for page in range(from_page, to_page+1):
            pdf_page = pdf_reader.getPage(page)  # Create a page object
            full_text += pdf_page.extractText()  # Add page objects together  to create one text string
        pdf_file.close()  # Close the pdf file object
        return full_text


app = App()
