# Minesweeper

Requirements: [https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/](https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/)

> The project implements functionality to play Minesweeper with the help of AI. This is done with propositional logic, which allows for inference and knowledge engineering.

The game can be played normally, with the optional help of the model to choose a move.

## Knowledge Representation

Knowledge is represented in the following form:  

`{A, B, C, D} = 1`

Whereby `A`, `B`, `C` & `D` represent tuples corresponding to board coordinates and the integer represents the number of mines that is contained in these cells.

## Logic

Certain logical conclusions can be made with this knowledge representation:

- When a count is 0, all cells in the sentence are safe
- When a count equals the length of cells, all cells are mines
- If set1 is a subset of set2, then set2 - set1 = count2 - count1

As well as the following:  

- When a cell is safe, remove it from the sentence
- When a cell is a mine, remove it from the sentence and decrease the count by 1
