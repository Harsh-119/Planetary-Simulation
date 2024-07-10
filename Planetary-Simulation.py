
# These are the appropriate imports that I will be using.
from tkinter import *
import math
import time

# The green planets that are spawn are referred to as ball or balls.
ballsRadius = []
ballsCenter = []
angles = []


# This is the main class in which the canvas for the simulation will be built in, this area also contains the labels used in Tkinter.
class Main(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Simulation')
        
        # Tkinter canvas creation area
        self.canvas = Canvas(self, width=300, height=300, background='black')
        
        # Using Tkinter grid geometry manager.
        self.canvas.grid(row=0, column=0)

        self.frame = Frame(self)
        self.frame.grid(row=0, column=1)
        
        # Creates the appropriate labels.
        label1 = Label(self.frame, text='Mass of Sun (x * 10^29 kg):').grid(row=0, column=0)
        self.entry1 = Entry(self.frame)
        self.entry1.grid(row=0, column=1)

        self.variable = StringVar(self)
        self.variable.set('Display Data')

        self.optionMenu = OptionMenu(self.frame, self.variable, '')
        self.optionMenu.grid(row=1, column=0)
        
        # This is the Time scale variable which can be edited by the user, this acts as a speeding up tool.
        label3 = Label(self.frame, text='Time Scale (1 sec = x days):').grid(row=2, column=0)
        self.entry2 = Entry(self.frame)
        self.entry2.grid(row=2, column=1)

        # These are the buttons which the user can click, each of these buttons have a specific function.

        button1 = Button(self.frame, text='Add Planet', command=self.on_add_ball).grid(row=3, column=0)
        button2 = Button(self.frame, text='Start/Stop', command=self.on_start_stop).grid(row=4, column=0)
        button6 = Button(self.frame, text='Reset', command=self.on_reset).grid(row=6, column=0)
        button7 = Button(self.frame, text='Display', command=self.on_display).grid(row=1, column=1)
        button3 = Button(self.frame, text='Save Data', command=self.on_save).grid(row=5, column=0)
        self.stop = True
        # This creates the sun and its x, y, r, colour of the object and tag.
        sun = self.create_circle(150, 150, 20, 'red', 'sun')


    # This function creates the sun or planet when its called upon.
    def create_circle(self, x, y, r, color, tag):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill=color, tag=tag)

    
    # Function which can be called upon when the button add planet is clicked.
    def on_add_ball(self):
        cAddBall = AddBall()
        cAddBall.mainloop()

        
    # This is the star stop button funcation which the user can press to pause or play the simulation.
    def on_start_stop(self):
        self.stop = not self.stop
        if not self.stop:
            def animate():
                if not self.stop:
                    self.canvas.delete('delete')
                    for i in range(0, len(ballsRadius)):
                        ballsCenter[i][0] = 150 - ballsRadius[i] * math.sin(math.radians(angles[i]))
                        ballsCenter[i][1] = 150 - ballsRadius[i] * math.cos(math.radians(angles[i]))

                        self.create_circle(ballsCenter[i][0], ballsCenter[i][1], 5, 'green', 'delete')
                        angles[i] += 500 / ballsRadius[i]
                    self.update()
                    self.after(int(1000 / int(self.entry2.get())) - int(self.entry1.get()), animate)


            animate()

    def swap_stop(self):
        self.stop = not self.stop

        
    # This function makes it so whenever the mass of sun and time scale is changed it updates the values instantly showing instant effects.
    def on_update(self):
        for radius in ballsRadius:
            self.create_circle(150, 150 - radius, 5, 'green', 'delete')
            options = [str('Planet ' + str(x)) for x in range(1, len(ballsRadius) + 1)] 
            # This shows the ammount of planets in the display data drop down menu.
        self.optionMenu = OptionMenu(self.frame, self.variable, *options)
        self.optionMenu.grid(row=1, column=0)

    def on_display(self):
        ballNum = int(str(self.variable.get())[6:]) - 1
        cDisplayData = DisplayData(ballNum)
        cDisplayData.mainloop()
        
    # This is the reset function.
    def on_reset(self):
        self.destroy()
        cMain = Main()
        cMain.mainloop()


    # This is the save function, when the user clicks the "savedata" button it creates a file with the .txt extension.
    # The information stored in the data.txt is the planet number, the radius, the velocity and the acceleration. 
    def on_save(self):
        with open('data.txt', 'w') as fout:
            for ballIndex in range(len(ballsRadius)):
                fout.write(str('Data for Planet ' + str(ballIndex + 1) + ':\n'))
                fout.write(str('Radius is: ' + str(ballsRadius[ballIndex])) + ' m \n')
                fout.write(str('Velocity is: ') + str(round(math.sqrt(
                    (6.673 * 10 ** -11 * int(cMain.entry1.get()) * 10 ** 29 / (ballsRadius[ballIndex] * 10 ** 9))),
                                                            2)) + ' m/s \n')
                fout.write(str('Acceleration is: ') + str(round(((round(math.sqrt(
                    (6.673 * 10 ** -11 * int(cMain.entry1.get()) * 10 ** 29 / (ballsRadius[ballIndex] * 10 ** 9))),
                                                                        2)) * (round(math.sqrt(

                    (6.673 * 10 ** -11 * int(cMain.entry1.get()) * 10 ** 29 / (ballsRadius[ballIndex] * 10 ** 9))),
                                                                                     2))) / (
                                                                    int(ballsRadius[ballIndex] * 10 ** 9)),
                                                                3)) + ' m/s² \n')


 # This is the class that allows the user to add more planets
 # When the "add planet" button is clicked the user is prompted with a text box in which they have to type in a valid radius.
 # When the user clicks "ok" in the enter radius text box the planet is spawned in at the given radius.
class AddBall(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('Add Planet')


        # This is the label for the enter radius text box.
        label1 = Label(self, text='Radius (x * 10^9 m)').grid(row=0, column=0)
        self.entry1 = Entry(self)
        self.entry1.grid(row=0, column=1)

        
        # This is the button which the user clicks after a valid radius has been entered.
        
        button1 = Button(self, text='OK', command=self.on_ok).grid(row=1, column=0)

    def on_ok(self):
        ballsRadius.append(int(self.entry1.get()))
        ballsCenter.append([150 - int(self.entry1.get()), 150])
        angles.append(0)
        cMain.on_update()
        self.destroy()

# This class is where the information in the "data" text box is created.
# The variables velo and accel are used to make the acceleration variable.
# Velo use the formula v = sqroot(Gm/r).
# Accel uses the formula a = v^2/r.
class DisplayData(Tk):
    def __init__(self, ballIndex):
        Tk.__init__(self)
        self.title('Data')

        velo = (round(

            math.sqrt((6.673 * 10 ** -11 * int(cMain.entry1.get()) * 10 ** 29 / (ballsRadius[ballIndex] * 10 ** 9))),
            2))
        accel = (velo * velo) / int(ballsRadius[ballIndex] * 10 ** 9)

        # Labels for the planet number, radius, velocity and acceleration.
        label1 = Label(self, text=str('Data for Planet ' + str(ballIndex + 1) + ':')).grid(row=0, column=0)
        label2 = Label(self, text=str('Radius is: ' + str(ballsRadius[ballIndex]) + '*10^9 m            ')).grid(row=1, column=0)
        label3 = Label(self, text=str('Velocity is : ') + str(round(
            math.sqrt((6.673 * 10 ** -11 * int(cMain.entry1.get()) * 10 ** 29 / (ballsRadius[ballIndex] * 10 ** 9))),
            2)) + ' m/s').grid(row=2, column=0)
        label4 = Label(self, text=str('         Acceleration is : ' + str(round(accel, 3)) + ' m/s²              ')).grid(row=3, column=0)


cMain = Main()
cMain.mainloop()


