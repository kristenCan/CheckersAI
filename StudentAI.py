import copy

from random import randint
from BoardClasses import Move
from BoardClasses import Board
import time


# The following part should be completed by students.
# Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self, col, row, p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col, row, p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1: 2, 2: 1}
        self.color = 2

    def evalFunction(self, newBoard, color):
        blackScore = 0
        whiteScore = 0
        totalPieces = 0
        for x in range(0, newBoard.row):
            for y in range(0, newBoard.col):
                checker = newBoard.board[x][y]
                if checker.get_color() == 'W':
                    if checker.is_king:
                        whiteScore += 5 + newBoard.row + 2
                        totalPieces += 1
                    else:
                        whiteScore += 5 + checker.row
                        totalPieces += 1
                    if checker.row == 0 or checker.row == newBoard.row:
                        whiteScore += 5

                elif checker.get_color() == 'B':
                    if checker.is_king:
                        blackScore += 5 + newBoard.row + 2
                        totalPieces += 1
                    else:
                        blackScore += 5 + (newBoard.row - checker.row)
                        totalPieces += 1
                    if checker.col == 0 or checker.col == newBoard.col:
                        blackScore += 5
        if color == 1:
            return (blackScore - whiteScore) / totalPieces
        else:
            return (whiteScore - blackScore) / totalPieces

    def alphaBeta(self, newBoard, depth, alpha, beta, maxPlayer):
        # myScore = -9999
        # enemyScore = 9999
        #
        # if maxPlayer:
        #     prevTurn = self.opponent[self.color]
        # else:
        #     prevTurn = self.color

        # if(newBoard.is_win(prevTurn)) or (newBoard.is_win(prevTurn) == 0):
        #     print(newBoard.is_win(prevTurn))

        if depth == 0:
            # return the score
            # if maxPlayer:
            score = self.evalFunction(newBoard, self.color)
            return score  # return the heuristic value of the board.
        else:

            # if it is max player, then for every child, choose the one with the max score
            if maxPlayer:
                score = -9999
                # newMoves gets all possible moves (child nodes)
                newMoves = newBoard.get_all_possible_moves(self.color)
                for elem in newMoves:
                    for move in elem:
                        # print("max making move: ", move)
                        newBoard.make_move(move, self.color)
                        score = max(score,self.alphaBeta(newBoard, depth - 1, alpha, beta, False))


                        # if score >= myScore:
                        #     myScore = score
                        # score = max(score, self.alphaBeta(newBoard, depth - 1, alpha, beta, False))
                        alpha = max(alpha, score)
                        # prunes
                        if alpha >= beta:  # beta cut off
                            # print("undo: ", move)
                            newBoard.undo()
                            break
                        # print("undo: ", move)
                        newBoard.undo()
                return score

            else:
                # if min player, choose the minimum score
                score = 9999
                newMoves = newBoard.get_all_possible_moves(self.opponent[self.color])

                for elem in newMoves:
                    for move in elem:
                        # print("min making move: ", move)
                        newBoard.make_move(move, self.opponent[self.color])
                        score = min(score,self.alphaBeta(newBoard, depth - 1, alpha, beta, True))
                        # score = min(score, self.alphaBeta(newBoard, depth - 1, alpha, beta, True))
                        # if score <= enemyScore:
                        #     enemyScore = score
                        beta = min(beta, score)
                        # prunes
                        if alpha >= beta:  # alpha cut off
                            # print("undo: ", move)
                            newBoard.undo()
                            break
                        # print("undo: ", move)
                        newBoard.undo()
                return score

    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)
        bestScore = -9999
        bestMove = Move([])
        for elem in moves:
            for move in elem:

                # for elem in move:
                # make deep copy of board
                # print("max making move: ", move)
                self.board.make_move(move, self.color)
                score = self.alphaBeta(self.board, 3, -9999, 9999, False)
                # print("score: ", score)
                if score >= bestScore:
                    bestScore = score
                    bestMove = move
                # print("undo: ", move)
                self.board.undo()
        # print("best move:", bestMove)
        print("best score: ", bestScore)
        self.board.make_move(bestMove, self.color)
        return bestMove
