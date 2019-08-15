import zipfile
import re
from Board import Board
from tkinter import filedialog
import tkinter

class File_Converter:

    def __init__(self,folder):
        self.cluepath = folder+"/clues.csv"
        self.answerpath = folder+"/layout.csv"
        self.valid_characters = ["A","B","C","D","E","F","G","H","I","J","K","L",
            "M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","A\n","B\n",
            "C\n","D\n","E\n","F\n","G\n","H\n","I\n","J\n","K\n","L\n","M\n","N\n",
            "O\n","P\n","Q\n","R\n","S\n","T\n","U\n","V\n","W\n","X\n","Y\n","Z\n"
        ]

    def make_layout(self):
        file = open(self.answerpath)
        output = []
        for line in file:
            temp = []
            array = re.split(",",line.upper())
            for character in array:
                if character in self.valid_characters:
                    temp.append(character[0])
                else:
                    temp.append(None)
            output.append(temp)
        return output

    def make_clue_dictionary(self):
        clue_dict = {}
        file = open(self.cluepath)
        for line in file:
            array = re.split(",",line.upper())
            new_array = []
            for otha_line in array:
                new_array.append(otha_line.replace("\ufeff",""))
            key = ""
            for i in range(len(new_array)-1):
                key += new_array[i]
            temp = new_array[-1].replace("\n","")
            temp = temp.replace("\t","")
            temp = temp.replace(" ","")
            clue_dict[key] = temp
        return clue_dict

    def generate_board(self):
        board = Board(self.make_clue_dictionary(),self.make_layout())
        board.display()

if __name__ == '__main__':
    def select_dir():
        folder_selected = filedialog.askdirectory()
        root.destroy()
        fc = File_Converter(folder_selected)
        fc.generate_board()
    root = tkinter.Tk()
    tkinter.Button(master=root, text='Select Folder', command = select_dir).pack()
    root.mainloop()
