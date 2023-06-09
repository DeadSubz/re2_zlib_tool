#!/usr/bin/env python3

import tkinter as tk
import sys
import os
import zlib

from tkinter import filedialog
from tkinter.filedialog import asksaveasfile
from tkinter.messagebox import askyesno

from PIL import Image, ImageTk

# window config.

root = tk.Tk()

# re2ico config.
im = Image.open('re2ico.png')
photo = ImageTk.PhotoImage(im)

root.title('RE2 - ZLIB Encoder')
root.geometry('360x200')
root.resizable(False, False)

########### ZLIB - CODE ###########

def bytes_to_uint(data):
    data = int.from_bytes(data, byteorder="big")
    return data

def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Choose a file",
                                          filetypes = (("Bin files",
                                                        "*.bin*"),
                                                       ("All files",
                                                        "*.*")))
    text_widget.delete("1.0", "end")
    text_widget.configure(state='normal')
    text_widget.insert("1.0", "File read: "+str(filename)+"\n")
    text_widget.configure(state='disabled')

    if os.path.isfile(filename):
        if (save_button['state'] == tk.DISABLED):
            save_button['state'] = tk.NORMAL
    #main()

def save_file():
    global fileoutput
    fileoutput = asksaveasfile(initialfile = 'untitled.zlib',
                      defaultextension=".zlib",
                      filetypes=[("ZLIB files.",
                                  "*.zlib*"),
                                 ("All files",
                                  "*.*")])
    main()
    text_widget.delete("1.0", "end")
    text_widget.configure(state='normal')
    text_widget.insert("1.0", "File compressed: "+fileoutput.name+"\n")
    text_widget.configure(state='disabled')

def zlib_compress(data): # compress input_file
    c = zlib.compressobj(level=9, wbits=14, strategy=1) # compression type
    res = c.compress(data)
    res += c.flush()
    return res

def zlib_enc(data):
    res = zlib_compress(data)
    return res

def main():
    # Tells if file is compressed.
    comp = b'\x00\x10\x00\x00' # 01 = dec, 02 = unknown.
    # Show input file size
    size = os.path.getsize(filename)
    # Convert input file size to hex string as big endian with 4 bytes length
    hex = size.to_bytes(4, 'big')
    with open(filename, "rb") as i: # read input_file
        print("Opening '%s'...\nInput size = {} bytes. {:02X} hex bytes.".format(size, size) % filename)
        with open(fileoutput.name, "wb") as o: # write output_file
            o.write(zlib_enc(i.read()))
            o.write(comp)
            o.write(hex)
            o.close()
        # Show output file size
        sizeout = os.path.getsize(fileoutput.name)
        print("File compressed and written as '%s'\nOutput size = {} bytes. {:02X} hex bytes.".format(sizeout, sizeout) % fileoutput.name)

#######################

# text widget
text_widget = tk.Text()
text_widget.place(
    x=125,
    y=25,
    width=220,
    height=160
)

# open button
open_button = tk.Button(
    root,
    text='OPEN FILE',
    command=browseFiles
)
open_button.place(
    x=10,
    y=50,
    width=100,
    height=30
)

# save button
save_button = tk.Button(
    root,
    state=tk.DISABLED,
    text='COMPRESS FILE',
    command=save_file
)
save_button.place(
    x=10,
    y=90,
    width=100,
    height=30
)

# exit button
def confirm():
    answer = askyesno(title="Bye bye",
                    message="Do you really want to exit?")
    if answer:
        root.destroy()
exit_button = tk.Button(
    root,
    text='EXIT',
    command=confirm
)
exit_button.place(
    x=10,
    y=130,
    width=100,
    height=30
)

# credits
credits = tk.Label(
    root,
    text='By\nDeadSubiter'
)
credits.place(
    x=25,
    y=165
)

root.wm_iconphoto(True, photo)
root.mainloop()
