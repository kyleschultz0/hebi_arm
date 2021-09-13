from tkinter import *
import tkinter.font as font
import encoder_functions


app = Tk()
app.geometry("1000x1000")
arduino = initialize_encoders()

# Define font
bigFont = font.Font(size = 12)


def drawEncoder()
    theta = get_encoder_feedback(arduino, num_encoders=2)
    

def get_x_and_y(event):
    global lasx, lasy
    lasx, lasy = event.x, event.y

def draw_smth(event):
    global lasx, lasy
    canvas.create_line((lasx, lasy, event.x, event.y), fill='red', width=2)
    lasx, lasy = event.x, event.y
    

canvas = Canvas(app, bg='white')
canvas.pack(anchor='nw', fill='both', expand=1)

buttonOn = Button(command = drawEncoder,
                  text = "Start Drawing",
                  height = 3, 
                  width = 14)
buttonOn['font'] = bigFont
buttonOn.pack(side = LEFT)


canvas.bind("<Button-1>", get_x_and_y)
canvas.bind("<B1-Motion>", draw_smth)



app.mainloop()