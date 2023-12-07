from PIL import ImageTk, Image

def Read_Image(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.BOX))

def Center_Window(window, aplicationWidth, aplicationHeight):
    screenWidth = window.winfo_screenwidth()
    screenHeight = window.winfo_screenheight()
    x = int((screenWidth/2) - (aplicationWidth/2))
    y = int((screenHeight/2) - (aplicationHeight/2))
    return window.geometry(f"{aplicationWidth}x{aplicationHeight}+{x}+{y}")