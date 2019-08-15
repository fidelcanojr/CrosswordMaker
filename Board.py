from Tile import Tile
import tkinter
from tkinter.constants import *
from tkinter import messagebox

class Board:

    def __init__(self,clues,layout):
        self.clues=clues
        self.layout=layout
        self.down={}
        self.across={}
        self.number_string_map={
            1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'J',
            11:'K',12:'L',13:'M',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',
            20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'
        }
        self.tiles = []

    @staticmethod
    def ConvertToBaseB(n, b):
        """Convert a positive number n to its digit representation in base b."""
        digits = []
        while n > 0:
            digits.insert(0, n % b)
            n  = n // b
        return digits

    def check_grid(self):
        for tile in self.tiles:
            if tile.check():
                tile.mark_correct()

    def get_clue(self,answer):
        for clue in self.clues:
            if (self.clues[clue].upper() == answer.upper()):
                return clue
        return None

    def number_clues(self):
        #Find the across clues
        row_letter_counter = 1
        for row in self.layout:
            current_guess = ""
            base_27 = self.ConvertToBaseB(row_letter_counter,27)
            while 0 in base_27:
                row_letter_counter += 1
                base_27 = self.ConvertToBaseB(row_letter_counter,27)
            coordinate = ""
            for digit in base_27:
                coordinate += self.number_string_map[digit]
            for i in range(len(row)):
                test_guy = row[i]
                if (test_guy != None):
                    current_guess += test_guy
                elif ((test_guy == None) and (len(current_guess)>1)):
                    clue = self.get_clue(current_guess)
                    if clue == None:
                        messagebox.showerror("Error!","The input files are incompatible.")
                        print("HERE "+current_guess)
                        break
                    else:
                        self.across[clue] = coordinate+str(i+1-len(current_guess))
                        current_guess = ""
                else:
                    current_guess = ""
            if (len(current_guess) > 1):
                clue = self.get_clue(current_guess)
                if clue == None:
                    messagebox.showerror("Error!","The input files are incompatible.")
                    print("HERE "+current_guess)
                else:
                    self.across[clue] = coordinate+str(len(row)-len(current_guess)+1)
            row_letter_counter += 1
        #Find the down clues
        for column_no in range(len(self.layout[0])):
            current_guess = ""
            start_letter = ""
            row_letter_counter = 1
            for row_no in range(len(self.layout)):

                base_27 = self.ConvertToBaseB(row_letter_counter,27)
                while 0 in base_27:
                    row_letter_counter += 1
                    base_27 = self.ConvertToBaseB(row_letter_counter,27)
                coordinate = ""
                for digit in base_27:
                    coordinate += self.number_string_map[digit]

                test_guy = self.layout[row_no][column_no]
                if (test_guy != None):
                    if (len(current_guess) == 0):
                        start_letter += coordinate
                    current_guess += test_guy
                elif ((test_guy == None) and (len(current_guess)>1)):
                    clue = self.get_clue(current_guess)
                    if (clue==None):
                        messagebox.showerror("Error!","The input files are incompatible.")
                        print("HERE "+current_guess)
                        break
                    else:
                        self.down[clue] = start_letter+str(column_no+1)
                        current_guess = ""
                        start_letter = ""
                else:
                    current_guess = ""
                    start_letter = ""

                row_letter_counter += 1
            if (len(current_guess) > 1):
                clue = self.get_clue(current_guess)
                if clue == None:
                    messagebox.showerror("Error!","The input files are incompatible.")
                    print("HERE "+current_guess)
                else:
                    self.down[clue] = start_letter+str(column_no+1)
        if ((len(self.across)+len(self.down)) != len(self.clues)):
            messagebox.showerror("Error!","The input files are incompatible.")
            print("More clues provided than needed")

    def display(self):
        tk = tkinter.Tk()
        frame = tkinter.Frame(tk)
        frame.pack(fill=BOTH,expand=1)
        for i in range(len(self.layout)):
            for j in range(len(self.layout[0])):
                if self.layout[i][j] != None:
                    tile = Tile(self.layout[i][j],i,j,frame)
                    self.tiles.append(tile)
                    tile.lay_down_tile()
        letter_counter = 1
        for i in range(len(self.layout)):
            base_27 = self.ConvertToBaseB(letter_counter,27)
            while 0 in base_27:
                letter_counter += 1
                base_27 = self.ConvertToBaseB(letter_counter,27)
            tag = ""
            for digit in base_27:
                tag += self.number_string_map[digit]
            label = tkinter.Label(master=frame,text=tag)
            label.grid(row=i+1,column=0)
            letter_counter += 1
        for i in range(len(self.layout[0])):
            label = tkinter.Label(master=frame,text=str(i+1))
            label.grid(row=0,column=i+1)
        check = tkinter.Button(master=frame,command=self.check_grid,text="Check")
        check.grid(row=0,column=0)
        self.number_clues()
        across_box = tkinter.Listbox(master=frame)
        across_box.insert(END,"Across")
        for clue in self.across:
            across_box.insert(END,self.across[clue]+" : "+clue)
        across_box.config(width=0,height=0)
        across_box.grid(row=0,column=len(self.layout[0])+1,rowspan=len(self.layout)+1,padx=10,pady=10)
        down_box = tkinter.Listbox(master=frame)
        down_box.insert(END,"Down")
        for clue in self.down:
            down_box.insert(END,self.down[clue]+" : "+clue)
        down_box.config(width=0,height=0)
        down_box.grid(row=0,column=len(self.layout[0])+2,rowspan=len(self.layout)+1,padx=10,pady=10)
        tk.mainloop()

if __name__ == "__main__":
    example = [[None,None,None,"T","H","I","S"],
                ["I","S",None,None,None,None,"A"],
                [None,"E",None,None,None,"A","N"],
                ["E","X","A","M","P","L","E"]]
    clues = {
        "Clue for this": "this",
        "Clue for is": "is",
        "Clue for an": "an",
        "Clue for example": "example",
        "Clue for sex": "sex",
        "Clue for sane": "sane",
        "Clue for al": "al"
    }
    board = Board(clues,example)
    board.display()
