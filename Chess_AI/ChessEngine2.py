'''
 this classs is responsible for storing all the information about the current state of chess game. it will also be responsible for
 detemining the valid move. it will also keep a move log.
'''


class GameState():
    def __init__(self):
        # the bord is an 8x8 2d list,each element of the list has 2 characters.
        # the first chrarcter represent the color of piece, 'b' or 'w'
        # the second chracter represent the type of the piece 'K','Q','N','B','R' or 'P'
        # "--" represent the empty space on the board
        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
        #     ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.board = [
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]]
        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        # self.blackKingLocation = (7, 4)
        # self.whiteKingLocation = (0, 4)
        self.blackKingLocation = (0, 4)
        self.whiteKingLocation = (7, 4)
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.enpassantPossible = ()  # cordinates for the square where en passant capture is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRight = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                             self.currentCastlingRight.wqs, self.currentCastlingRight.bqs)]

    ''' 
    takes a move as a parameter and executed it(this will not work for castling,pawn prmotion and en-passant) 
    '''

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo later
        self.whiteToMove = not self.whiteToMove  # swap player
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        # pwan Promotion
        if move.pawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        # enpassant move
        if move.enPassant:
            self.board[move.startRow][move.endCol] = '--'  # capturing the pwan

        # update enpassant posible variable
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:  # only on 2 suare pwan advance
            self.enpassantPossible = ((move.startRow + move.endRow) // 2, move.startCol)
        else:
            self.enpassantPossible = ()

        self.enpassantPossibleLog.append(self.enpassantPossible)

        # castle move
        if move.castle:
            if move.endCol - move.startCol == 2:  # kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # move the rook
                self.board[move.endRow][move.endCol + 1] = '--'

            else:  # queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]  # move the rook
                self.board[move.endRow][move.endCol - 2] = '--'
        self.inCheck = self.inCheck_fun()
        # update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.bks,
                                                 self.currentCastlingRight.wqs, self.currentCastlingRight.bqs))

    '''this will undo the last move'''

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # update king position
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)
            # undo enpassant move
            if move.enPassant:
                self.board[move.endRow][move.endCol] = '--'  # leave landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                # self.enpassantPossible = (move.endRow, move.endCol)
            # #undo a 2 square pwan advance
            # if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            #     self.enpassantPossible =()
            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # undo castling rights
            self.castleRightsLog.pop()  # get rid of new castle rights from the movw we are undoing
            newRights = self.castleRightsLog[-1]  # set the current castle rights to  the last one in the list
            self.currentCastlingRight = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)

            # undo castle move
            if move.castle:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--'
            self.checkmate = False
            self.stalemate = False

    '''
    update the castling rights
    '''

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRight.wks = False
            self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRight.bks = False
            self.currentCastlingRight.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 7:  # right rook
                    self.currentCastlingRight.wks = False
                elif move.startCol == 0:  # left rook
                    self.currentCastlingRight.wqs = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 7:  # right rook
                    self.currentCastlingRight.bks = False
                elif move.startCol == 0:  # left rook
                    self.currentCastlingRight.bqs = False

        # # if rook is captured
        # if move.pieceCaptured == 'wR':
        #     if move.endRow == 7:
        #         if move.endCol == 0:
        #             self.currentCastlingRight.wqs = False
        #         elif move.endCol == 7:
        #             self.currentCastlingRight.wks = False
        # elif move.pieceCaptured == 'bR':
        #     if move.endRow == 0:
        #         if move.endCol == 0:
        #             self.currentCastlingRight.bqs = False
        #         elif move.endCol == 7:
        #             self.currentCastlingRight.bks = False

        # if rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRight.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRight.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRight.bks = False

    '''
    All move considering checks
    '''

    def getValidMoves(self):

        tempEnpassantPossible = self.enpassantPossible
        tempCastlingRights = CastleRights(self.currentCastlingRight.wks, self.currentCastlingRight.wqs,
                                          self.currentCastlingRight.bks, self.currentCastlingRight.bqs)
        # 1.) generate all the posible move
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        elif not self.whiteToMove:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        # 2.) for each move, make move
        for i in range(len(moves) - 1, -1, -1):  # when removing from a list go backwards throgh the list
            self.makeMove(moves[i])
            # 3.) generate all the opponent's moves
            # 4.) for each of your opponent's moves see if they attack your king
            self.whiteToMove = not self.whiteToMove
            if self.inCheck_fun():
                moves.remove(moves[i])  # 5.) if they attack your king, not a valid move
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:  # either checkmate or stalemate
            if self.inCheck_fun():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRight = tempCastlingRights
        return moves

    '''
    determin if the current player is in chack
    '''

    def inCheck_fun(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    '''determin if the enemy can attack the square r, c'''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove  # switch to opponent's turn
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove  # switch the turn back
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:  # square is under attack
                return True
        return False

    '''
    All moves without considering checks
    '''

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # number of rows
            for c in range(len(self.board[r])):  # number of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)  # calls the appropriate move function based on peice type
        return moves

    '''
    get all the pawn for the pawn located at the row, col and add these moves to the list
    '''

    def getPawnMoves(self, r, c, moves):
        #not when black is down and white is up and use w
        if not self.whiteToMove:
            if self.board[r - 1][c] == "--":  # 1 square pawn move
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn move
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # capture to left
                if self.board[r - 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r - 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, enPassant=True))
            if c + 1 <= 7:  # capture to right
                if self.board[r - 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r - 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, enPassant=True))

        #used for white pawn move when using not and use b
        else:
            if self.board[r + 1][c] == "--":  # 1 square move
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r + 2, c), self.board))

            if c - 1 >= 0:  # capture to left
                if self.board[r + 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r + 1, c - 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, enPassant=True))
            if c + 1 <= 7:  # capture to right
                if self.board[r + 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r + 1, c + 1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, enPassant=True))

    '''
        get all the Rook for the pawn located at the row, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in direction:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # frienly piece
                        break
                else:  # off board
                    break

    '''
        get all the Knight for the pawn located at the row, col and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
        get all the Bishop for the pawn located at the row, col and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly peice
                        break
                else:  # off board
                    break

    '''
        get all the Queen for the pawn located at the row, col and add these moves to the list
    '''

    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r, c, moves)
        self.getBishopMoves(r, c, moves)

    '''
        get all the King for the pawn located at the row, col and add these moves to the list
    '''

    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for i in range(8):
            endRow = r + kingMoves[i][0]
            endCol = c + kingMoves[i][1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r, c):
            return  # can't castle in check
        if (self.whiteToMove and self.currentCastlingRight.wks) or (
                not self.whiteToMove and self.currentCastlingRight.bks):
            self.getkingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRight.wqs) or (
                not self.whiteToMove and self.currentCastlingRight.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getkingsideCastleMoves(self, r, c, moves):
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--':
            if not self.squareUnderAttack(r, c + 1) and not self.squareUnderAttack(r, c + 2):
                moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--':
            if not self.squareUnderAttack(r, c - 1) and not self.squareUnderAttack(r, c - 2):
                moves.append(Move((r, c), (r, c - 2), self.board, castle=True))


class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    # map keys to value
    # key : value

    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, enPassant=False, castle=False, incheck=False, checkmate=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.inCheck = incheck
        self.Checkmate = checkmate
        # pwan promotion
        self.pawnPromotion = (self.pieceMoved == 'wP' and self.endRow == 0) or (
                    self.pieceMoved == 'bP' and self.endRow == 7)
        # enpassant
        self.enPassant = enPassant
        if enPassant:
            self.pieceCaptured = 'wP' if self.pieceMoved == 'bP' else 'bP'
        self.isCapture = self.pieceCaptured != '--'
        # castlemove
        self.castle = castle
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    '''
    overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        piece = self.pieceMoved[1]
        col = self.startCol
        row = self.startRow
        if self.castle:
            return "0-0" if self.endCol == 6 else "0-0-0"
        if piece == "P":
            if self.pieceCaptured != "--":
                return self.getRankFile(row, col) + "x" + self.getRankFile(self.endRow, self.endCol)
            return self.getRankFile(self.endRow, self.endCol)
        elif piece == "R":
            if self.pieceCaptured != "--":
                return "Rx" + self.getRankFile(self.endRow, self.endCol)
            return "R" + self.getRankFile(self.endRow, self.endCol)
        elif piece == "N":
            if self.pieceCaptured != "--":
                return "Nx" + self.getRankFile(self.endRow, self.endCol)
            return "N" + self.getRankFile(self.endRow, self.endCol)
        elif piece == "B":
            if self.pieceCaptured != "--":
                return "Bx" + self.getRankFile(self.endRow, self.endCol)
            return "B" + self.getRankFile(self.endRow, self.endCol)
        elif piece == "Q":
            if self.pieceCaptured != "--":
                return "Qx" + self.getRankFile(self.endRow, self.endCol)
            return "Q" + self.getRankFile(self.endRow, self.endCol)
        elif piece == "K":
            if self.pieceCaptured != "--":
                return "Kx" + self.getRankFile(self.endRow, self.endCol)
            return "K" + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    def __str__(self):
        # Castling
        if self.castle:
            return "O-O" if self.endCol == 6 else "O-O-O"

        piece = self.pieceMoved[1]
        isPawn = piece == "P"
        endSquare = self.getRankFile(self.endRow, self.endCol)

        # Disambiguation
        disambigFile = disambigRank = False
        if not isPawn:
            for move in getattr(self, 'validMoves', []):
                if move.pieceMoved == self.pieceMoved and move.endRow == self.endRow and move.endCol == self.endCol and move != self:
                    if move.startCol != self.startCol:
                        disambigFile = True
                    # if move.startRow != self.startRow:
                    #     disambigRank = True

        san = ""

        # Piece symbol
        if not isPawn:
            san += piece
            if disambigFile:
                san += self.colsToFiles[self.startCol]
            # if disambigRank:
            #     san += self.rowsToRanks[self.startRow]

        # Pawn captures
        if isPawn and self.isCapture:
            san += self.colsToFiles[self.startCol]

        # Capture marker
        if self.isCapture:
            san += "x"

        # Destination square
        san += endSquare

        # Promotion
        if self.pawnPromotion:
            san += "=Q"
        if self.Checkmate:
            san += "#"
        elif self.inCheck:
            san += "+"
        return san