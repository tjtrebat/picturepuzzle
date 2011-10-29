__author__ = 'Tom'

import math
import random
import tkMessageBox
from Tkinter import *
from PIL import Image, ImageTk

class Block:
    def __init__(self, position, image):
        self.position = position
        self.image = image
        self.canvas_image = None
        self.current_position = None

    def __str__(self):
        return "<Block-%d> at %s" % (4 * self.position[0] + self.position[1], str(self.current_position),)

class PicturePuzzle:
    def __init__(self, root):
        self.root = root
        self.image = Image.open("images/toucan.jpg")
        self.canvas = Canvas(self.root, width=109, height=109)
        self.blocks = self.get_blocks()
        self.empty_space = (3, 3)
        self.add_blocks()
        self.canvas.pack()

    def add_blocks(self):
        for i in range(4):
            for j in range(4):
                if (i, j) != (3, 3):
                    block = self.blocks[4 * i + j]
                    block.canvas_image = self.canvas.create_image(27 * j, 27 * i, image=block.image, anchor=NW)
                    block.current_position = (i, j)
                    self.canvas.tag_bind(block.canvas_image, "<Button-1>", self.click)

    def click(self, event):
        block = self.get_block(event.widget.find_closest(event.x, event.y))
        if self.is_movable(block.current_position):
            self.canvas.move(block.canvas_image, 27 * (self.empty_space[1] - block.current_position[1]), 27 * (self.empty_space[0] - block.current_position[0]))
            temp = self.empty_space
            self.empty_space = block.current_position
            block.current_position = temp
        if self.is_game_over():
            tkMessageBox.showinfo(title="Picture Puzzle", message="You solved the puzzle!")

    def is_movable(self, position):
        distance = map(lambda x,y: int(math.fabs(x - y)), position, self.empty_space)
        if sum(distance) <= 1:
            return True
        return False

    def is_game_over(self):
        for block in self.blocks:
            if block.position != block.current_position:
                return False
        return True

    def get_blocks(self):
        blocks = []
        for i in range(4):
            for j in range(4):
                blocks.append(Block((i, j,), ImageTk.PhotoImage(self.image.crop((27 * j, 27 * i, 27 * (j + 1), 27 * (i + 1))))))
        blocks.pop()
        random.shuffle(blocks)
        return blocks

    def get_block(self, image):
        for block in self.blocks:
            if image[0] == block.canvas_image:
                return block

if __name__ == "__main__":
    root = Tk()
    root.resizable(0, 0)
    picture_puzzle = PicturePuzzle(root)
    root.mainloop()