"""
PDF to Audiobook Converter
by Bryson Phillip
11/01/2022

A simple pdf to mp3 conversion app utilizing text to speech. Option to convert all pages or select pages only.

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
        self.total_pages = None
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
        self.from_label = Label(text="from:", state="disabled")
        self.from_label.place(relx=0.33, rely=0.50, anchor=CENTER)
        self.from_entry = Entry(self.window, width=3, state="disabled")
        self.from_entry.place(relx=0.45, rely=0.5, anchor=CENTER)
        self.to_label = Label(text="to:", state="disabled")
        self.to_label.place(relx=0.55, rely=0.5, anchor=CENTER)
        self.to_entry = Entry(self.window, width=3, state="disabled")
        self.to_entry.place(relx=0.64, rely=0.5, anchor=CENTER)
        self.select_pages_field = [self.from_label, self.from_entry, self.to_label, self.to_entry]
        # Button to convert pdf to mp3
        self.convert_button = Button(text="Convert", command=lambda: self.convert_pdf_to_mp3(self.pdf_filename))
        # Conversion status label
        self.success_label = Label(text="")
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
        self.total_pages = get_total_number_of_pages(self.pdf_filename)
        self.update_page_numbers()

    # This function uses text to speech to create an audio file from the text pulled from the pdf
    def convert_pdf_to_mp3(self, pdf_filename):
        self.success_label.configure(text="")  # Remove previous success message
        # Check radio button if either "all pages" is selected or the from and to page entry boxes is selected
        if self.which_pages_to_convert.get() == "all":
            text_to_convert = create_text_string(pdf_filename, 0, int(self.total_pages))
        else:  # Add selected pages text to self.full_text
            # Exit if entry field doesn't have an integer
            if not is_int(self.from_entry.get()) or not is_int(self.to_entry.get()):
                self.success_label.configure(text="Error: Only numerals allowed in page selection", foreground="red")
                self.update_page_numbers()
                return
            else:
                starting_page = int(self.from_entry.get()) - 1  # Subtract 1 to fit base 0 index
                ending_page = int(self.to_entry.get())
                # Check if from is before page 1, if from is after to, and if to is after last page of pdf
                if starting_page < 0 or starting_page >= ending_page or ending_page > self.total_pages:
                    self.success_label.configure(text="Error: page selection out of range", foreground="red")
                    self.update_page_numbers()
                    return
                else:
                    text_to_convert = create_text_string(pdf_filename, starting_page, ending_page)
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
        self.success_label.configure(text="mp3 successfully saved", foreground="green")
        os.remove("audio.mp3")  # Delete temporary audio file after saved to desired destination

    # This function briefly enables the page number entry state if disabled and updates the page number
    def update_page_numbers(self):
        if self.to_entry['state'] == "disabled":
            self.from_entry.configure(state="normal")
            self.to_entry.configure(state="normal")
            self.update_entry_widgets(self.total_pages)
            self.from_entry.configure(state="disabled")
            self.to_entry.configure(state="disabled")
        else:
            self.update_entry_widgets(self.total_pages)

    # This function updates the page numbers in the 'from:' and 'to:' entry widget.
    # Sets 'from' to 1, and 'to' to the last page
    def update_entry_widgets(self, num_pages):
        self.from_entry.delete(0, END)
        self.from_entry.insert(0, 1)
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


# This function opens the pdf and gets the page count
def get_total_number_of_pages(pdf_filename):
    pdf_file = open(pdf_filename, "rb")  # Create pdf file object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)  # Create pdf reader object
    number_of_pages = pdf_reader.numPages  # Return total number of pages
    pdf_file.close()  # Close the pdf file object
    return number_of_pages


# This function creates a string from the selected pages of the pdf
def create_text_string(pdf_name, from_page, to_page):
    pdf_file = open(pdf_name, "rb")  # Create pdf file object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)  # Create pdf reader object
    # Get each page of pdf and extract text to string variable
    full_text = ""
    for page in range(from_page, to_page):
        pdf_page = pdf_reader.getPage(page)  # Create a page object
        full_text += pdf_page.extractText()  # Add page objects together  to create one text string
    pdf_file.close()  # Close the pdf file object
    return full_text

# This function checks if variable is an integer, used checking the page numbers selected
def is_int(x):
    try:
        x = int(x)
        return True
    except ValueError:
        return False


app = App()
