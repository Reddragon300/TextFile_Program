'''
Created on Apr 20, 2022

Create a graphical user interface that will allow the user to create, open and save a text file. 
It should include a text field for the file name. A text area to display the contents of the file.
And three buttons ( New , Open , Save ) to operate the application. 

@author: Brandon Claspill
'''

from tkinter import *
from tkinter import messagebox, filedialog
import os
import shutil


class Editor(Frame):
    def __init__(self):
        ''' Setup the window and widgets '''
        Frame.__init__(self)
        self.master.title('Text Editor')
        self.grid()

        self._fileLabel = Label(self, text='Filename')
        self._fileLabel.grid(row=0, column=0)

        self._fileVar = StringVar()
        self._fileEntry = Entry(self, textvariable=self._fileVar)
        self._fileEntry.grid(row=0, column=1)

        # Command Buttons
        self._newButton = Button(self, text='New', command=self._newFile)
        self._newButton.grid(row=1, column=0)

        self._openButton = Button(self, text='Open', command=self._openFile)
        self._openButton.grid(row=1, column=1)

        self._saveButton = Button(self, text='Save', command=self._saveFile)
        self._saveButton.grid(row=1, column=2)

        # Frame For Text Box With Scroll
        self._textPane = Frame(self)
        self._textPane.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W)

        self._yScroll = Scrollbar(self._textPane, orient=VERTICAL)
        self._yScroll.grid(row=0, column=1, sticky=N+S)

        self._outputArea = Text(self._textPane, width=80,
                                height=20, yscrollcommand=self._yScroll.set)
        self._outputArea.grid(row=0, column=0, sticky=W+E+N+S)
        self._yScroll['command'] = self._outputArea.yview

    def _newFile(self):
        if self._confirm_clear_text():
            self._fileName = ''
            self._fileVar.set('')
            self._outputArea.delete('1.0', END)

    def _openFile(self):
        if self._confirm_clear_text():
            filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                                  filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
            if filename:
                self._fileName = filename
                self._fileVar.set(os.path.basename(filename))
                try:
                    with open(self._fileName, 'r') as file:
                        self._outputArea.delete('1.0', END)
                        self._outputArea.insert('1.0', file.read())
                except IOError:
                    messagebox.showerror(
                        message='Error reading file!', parent=self)

    def _saveFile(self):
        filename = self._fileVar.get()
        if not filename:
            filename = filedialog.asksaveasfilename(initialdir=os.getcwd(),
                                                    defaultextension='.txt',
                                                    filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')])
            if not filename:
                return
            self._fileName = filename
            self._fileVar.set(os.path.basename(filename))
        if self._confirm_file_overwrite():
            try:
                with open(self._fileName, 'w') as file:
                    file.write(self._outputArea.get('1.0', END))
            except IOError:
                messagebox.showerror(message='Error saving file!', parent=self)

    def _confirm_clear_text(self):
        if self._outputArea.get('1.0', END).strip() != '':
            result = messagebox.askquestion('Confirm Clear', 'Are you sure you want to clear the text?',
                                            icon='warning', parent=self)
            return result == 'yes'
        return True

    def _confirm_file_overwrite(self):
        if os.path.exists(self._fileName):
            result = messagebox.askquestion('Confirm Overwrite', 'The file already exists. Do you want to overwrite it?',
                                            icon='warning', parent=self)
            return result == 'yes'
        return True


def main():
    Editor().mainloop()


if __name__ == '__main__':
    main()
