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
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["bQ", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "bR"],
        #     ["--", "--", "--", "--", "wK", "--", "--", "--"]]

        # self.board = [
        #     ["bR", "bN", "bB", "bQ", "--", "bB", "bN", "bR"],
        #     ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wK", "--", "--", "--", "--", "--", "--", "--"],
        #     ["wQ", "--", "--", "--", "--", "--", "--", "--"],
        #     ["--", "--", "--", "--", "--", "--", "--", "wR"],
        #     ["--", "--", "--", "--", "bK", "--", "--", "--"]]

        self.moveFunctions = {'P': self.getPawnMoves, 'R': self.getRookMoves, 'N': self.getKnightMoves,
                              'B': self.getBishopMoves, 'Q': self.getQueenMoves, 'K': self.getKingMoves}
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.inCheck = False
        self.pins = []
        self.checks = []
        self.checkmate = False
        self.stalemate = False
        self.draw = False
        self.enPassantPossible = ()
        # self.enpassantPossibleLog = [self.enPassantPossible]
        # castling rights
        self.whiteCastleKingside = True
        self.whiteCastleQueenside = True
        self.blackCastleKingside = True
        self.blackCastleQueenside = True
        self.castleRightsLog = [
            CastleRights(self.whiteCastleKingside, self.blackCastleKingside, self.whiteCastleQueenside,
                         self.blackCastleQueenside)]

        ''' takes a move as a parameter and executed it(this will not work for castling,pawn prmotion and en-passant) '''

    def makeMove(self, move):
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.board[move.startRow][move.startCol] = "--"
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        # update king location if moved
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)
        # if pawn move twise, next move can capture the pawn
        if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
            self.enPassantPossible = ((move.endRow + move.startRow) // 2, move.endCol)
        else:
            self.enPassantPossible = ()
        # if en passant move, must update the board to capture the pawn
        if move.enPassant:
            self.board[move.startRow][move.endCol] = "--"
        # if pawn promostion change piece
        if move.pawnPromotion:
            # promotedPiece = input("Promote to Q, R, B, or N:")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'  # promotedPiece
        # update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.whiteCastleKingside, self.blackCastleKingside,
                                                 self.whiteCastleQueenside, self.blackCastleQueenside))

        # castle moves
        if move.castle:
            if move.endCol - move.startCol == 2:  # kingside
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]  # move Rook
                self.board[move.endRow][move.endCol + 1] = '--'  # empty space where rook was

            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'  # empty space where rook was
        # After updating the board and toggling whiteToMove
        self.inCheck, self.checkmate, self.stalemate = self.checkGameStatus()

    def checkGameStatus(self):
        if self.whiteToMove:
            kingRow, kingCol = self.whiteKingLocation
            allyColor = 'w'
        else:
            kingRow, kingCol = self.blackKingLocation
            allyColor = 'b'

        kingInCheck = self.squareUnderAttack(kingRow, kingCol, allyColor)
        moves = self.getValidMoves()
        if len(moves) == 0:
            if kingInCheck:
                return True, True, False  # inCheck, checkmate, stalemate
            else:
                return False, False, True
        return kingInCheck, False, False

    '''this will undo the last move'''

    def undoMove(self):
        if len(self.moveLog) != 0:  # there is a move to undo
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove  # switch turns back
            # update king position if needed
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo enpassant is different
            if move.enPassant:
                self.board[move.endRow][move.endCol] = "--"  # removes the pawn thay was added in the wrong square
                self.board[move.startRow][
                    move.endCol] = move.pieceCaptured  # puts the pawn back on the correct square it was captured from
                self.enPassantPossible = (move.endRow, move.endCol)  # allow an en passant to happen on the next move
            # undo a 2 square pawn advance should make enPassantPossible = () again
            if move.pieceMoved[1] == 'P' and abs(move.startRow - move.endRow) == 2:
                self.enPassantPossible = ()
            # self.enpassantPossibleLog.pop()
            # self.enpassantPossible = self.enpassantPossibleLog[-1]

            # give back castle rights if move took away
            self.castleRightsLog.pop()  # remove last moves updates
            castleRights = self.castleRightsLog[-1]

            self.whiteCastleKingside = castleRights.wks
            self.blackCastleKingside = castleRights.bks
            self.whiteCastleQueenside = castleRights.wqs
            self.blackCastleQueenside = castleRights.bqs

            # undo castle
            if move.castle:
                if move.endCol - move.startCol == 2:  # kingside
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]  # move rook
                    self.board[move.endRow][move.endCol - 1] = "--"
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = "--"  # empty space where rook was

            self.checkmate = False
            self.stalemate = False

    '''
    All move considering checks
    '''

    def getValidMoves(self):
        moves = []
        self.inCheck, self.pins, self.check = self.checkForPinsAndChecks()
        if self.whiteToMove:
            kingRow = self.whiteKingLocation[0]
            kingCol = self.whiteKingLocation[1]
        else:
            kingRow = self.blackKingLocation[0]
            kingCol = self.blackKingLocation[1]
        if self.inCheck:
            if len(self.check) == 1:  # only 1 check, block check or move king
                moves = self.getAllPossibleMoves()
                # to block a check you must move a piece into one of the square between the enemy piece and king
                check = self.check[0]  # check information
                checkRow = check[0]
                checkCol = check[1]
                pieceChecking = self.board[checkRow][checkCol]
                validSquares = []
                # if knight check, must capture knight or move king, other pieces can not block
                if pieceChecking[1] == 'N':
                    validSquares = [(checkRow, checkCol)]
                else:
                    for i in range(1, 8):
                        validSquare = (kingRow + check[2] * i,
                                       kingCol + check[3] * i)  # check[2] and check[3] are the check informatoin
                        validSquares.append(validSquare)
                        if validSquare[0] == checkRow and validSquare[
                            1] == checkCol:  # once you get to piece and checks
                            break
                # get rid of any move that don't check or move king
                for i in range(len(moves) - 1, -1,
                               -1):  # go through backwords when you are removing from a list as iterating
                    if moves[i].pieceMoved[1] != 'K':  # move doesn't move king so it must block or capture
                        if not (moves[i].endRow, moves[i].endCol) in validSquares:
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(kingRow, kingCol, moves)
        else:  # not in check so all moves are fine
            moves = self.getAllPossibleMoves()

        if len(moves) == 0:
            if self.inCheck:
                self.checkmate = True

            else:
                self.stalemate = True

        else:
            self.checkmate = False
            self.stalemate = False

        return moves

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
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.whiteToMove:
            moveAmount = -1
            startRow = 6
            backRow = 0
            enemyColor = 'b'
            kingRow, kingCol = self.whiteKingLocation
        else:
            moveAmount = 1
            startRow = 1
            backRow = 7
            enemyColor = 'w'
            kingRow, kingCol = self.blackKingLocation
        pawnPromotion = False

        if self.board[r + moveAmount][c] == "--":  # 1 square move
            if not piecePinned or pinDirection == (moveAmount, 0):
                if r + moveAmount == backRow:  # if piece gets to back rank then it is pawn promotion
                    pawnPromotion = True
                moves.append(Move((r, c), (r + moveAmount, c), self.board, pawnPromotion=pawnPromotion))
                if r == startRow and self.board[r + 2 * moveAmount][c] == "--":  # 2 square move
                    moves.append(Move((r, c), (r + 2 * moveAmount, c), self.board))
        if c - 1 >= 0:  # capture to left
            if not piecePinned or pinDirection == (moveAmount, -1):
                if self.board[r + moveAmount][c - 1][0] == enemyColor:
                    if r + moveAmount == backRow:  # if piece gets to back rank then it is a pawn promostion
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c - 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king left to the pwan
                            # inside between king and pwan, outside range between pwan border
                            insideRange = range(kingCol + 1, c - 1)
                            outsideRange = range(c + 1, 8)
                        else:
                            insideRange = range(kingCol - 1, c, -1)
                            outsideRange = range(c - 2, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":  # some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c - 1), self.board, enPassant=True))
        if c + 1 <= 7:  # capture to right
            if not piecePinned or pinDirection == (moveAmount, 1):
                if self.board[r + moveAmount][c + 1][0] == enemyColor:
                    if r + moveAmount == backRow:  # if piece gets to back rank then it is pawnpromotion
                        pawnPromotion = True
                    moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, pawnPromotion=pawnPromotion))
                if (r + moveAmount, c + 1) == self.enPassantPossible:
                    attackingPiece = blockingPiece = False
                    if kingRow == r:
                        if kingCol < c:  # king left to the pwan
                            # inside between king and pwan, outside range between pwan border
                            insideRange = range(kingCol + 1, c)
                            outsideRange = range(c + 2, 8)
                        else:
                            insideRange = range(kingCol - 1, c + 1, -1)
                            outsideRange = range(c - 1, -1, -1)
                        for i in insideRange:
                            if self.board[r][i] != "--":  # some piece blocks
                                blockingPiece = True
                        for i in outsideRange:
                            square = self.board[r][i]
                            if square[0] == enemyColor and (square[1] == "R" or square[1] == "Q"):
                                attackingPiece = True
                            elif square != "--":
                                blockingPiece = True
                    if not attackingPiece or blockingPiece:
                        moves.append(Move((r, c), (r + moveAmount, c + 1), self.board, enPassant=True))

    '''
        get all the Rook for the pawn located at the row, col and add these moves to the list
    '''

    def getRookMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                if self.board[r][c][
                    1] != 'Q':  # can't remove queen from pin or rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on bloard
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # friendly piecce invalid
                            break
                else:  # off board
                    break

    '''
        get all the Knight for the pawn located at the row, col and add these moves to the list
    '''

    def getKnightMoves(self, r, c, moves):
        piecePinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                self.pins.remove(self.pins[i])
                break
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                if not piecePinned:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:  # not an ally piece (empty or enemy piece )
                        moves.append(Move((r, c), (endRow, endCol), self.board))

    '''
        get all the Bishop for the pawn located at the row, col and add these moves to the list
    '''

    def getBishopMoves(self, r, c, moves):
        piecePinned = False
        pinDirection = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == r and self.pins[i][1] == c:
                piecePinned = True
                pinDirection = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    if not piecePinned or pinDirection == d or pinDirection == (-d[0], -d[1]):
                        endPiece = self.board[endRow][endCol]
                        if endPiece == "--":  # empty space valid move
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                        elif endPiece[0] == enemyColor:  # enemy piece valid
                            moves.append(Move((r, c), (endRow, endCol), self.board))
                            break
                        else:  # frindlt piece invlaid
                            break
                else:  # off the board
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
        rowMoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colMoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        allycolor = 'w' if self.whiteToMove else 'b'
        for i in range(8):
            endRow = r + rowMoves[i]
            endCol = c + colMoves[i]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allycolor:  # not an ally piece (empty or enemy piece)
                    # place king on end square and check for checks
                    if allycolor == 'w':
                        self.whiteKingLocation = (endRow, endCol)
                    else:
                        self.blackKingLocation = (endRow, endCol)
                    inCheck, pins, checks = self.checkForPinsAndChecks()
                    if not inCheck:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    # place king back on original location
                    if allycolor == 'w':
                        self.whiteKingLocation = (r, c)
                    else:
                        self.blackKingLocation = (r, c)
        self.getCastleMoves(r, c, moves, allycolor)

    '''
       returns if the player is in the check, a list of pins and a list of checks 
    '''

    def checkForPinsAndChecks(self):
        pins = []  # squares where the allied pinned piece is and direction pinned from
        checks = []  # squares where enemy is applying a check
        inCheck = False
        if self.whiteToMove:
            enemyColor = 'b'
            allyColor = 'w'
            startRow = self.whiteKingLocation[0]
            startCol = self.whiteKingLocation[1]
        else:
            enemyColor = 'w'
            allyColor = 'b'
            startRow = self.blackKingLocation[0]
            startCol = self.blackKingLocation[1]
        # check outward from king pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            d = directions[j]
            possiblePin = ()  # reset possible pin
            for i in range(1, 8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor and endPiece[1] != 'K':
                        if possiblePin == ():  # 1st allied piece could be pinned
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:  # 2nd allied piece, so no pin or check possible in this direction
                            break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in this complex condition
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away piece is a king(this is necessary to prevent a king move to
                        #    square controlled by another king)
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and
                                 ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            if possiblePin == ():
                                inCheck = True
                                checks.append((endRow, endCol, d[0], d[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possiblePin)
                                break
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off board
        # check for knight check
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                    inCheck = True
                    checks.append((endRow, endCol, m[0], m[1]))

        return inCheck, pins, checks

    '''
    determin if the enemy can attack the square r, c
    '''

    def squareUnderAttack(self, r, c, allyColor):
        # check outward from square
        enemyColor = 'w' if allyColor == 'b' else 'b'
        direction = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(direction)):
            d = direction[j]
            for i in range(1, 8):
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] == allyColor:  # no attack from the direction
                        break
                    elif endPiece[0] == enemyColor:
                        type = endPiece[1]
                        # 5 possibilities here in this complex condition
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away piece is a king
                        if (0 <= j <= 3 and type == 'R') or \
                                (4 <= j <= 7 and type == 'B') or \
                                (i == 1 and type == 'P' and
                                 ((enemyColor == 'w' and 6 <= j <= 7) or (enemyColor == 'b' and 4 <= j <= 5))) or \
                                (type == 'Q') or (i == 1 and type == 'K'):
                            return True
                        else:  # enemy piece not applying check
                            break
                else:
                    break  # off board
        # check for knight check
        knightMoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        for m in knightMoves:
            endRow = r + m[0]
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece[0] == enemyColor and endPiece[1] == 'N':  # enemy knight attacking king
                    return True
        return False

    def getCastleMoves(self, r, c, moves, allyColor):
        inCheck = self.squareUnderAttack(r, c, allyColor)
        if inCheck:
            return  # can't castle in check
        if (self.whiteToMove and self.whiteCastleKingside) or (
                not self.whiteToMove and self.blackCastleKingside):  # cant castle if given up rights
            self.getkingsideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.whiteCastleQueenside) or (not self.whiteToMove and self.blackCastleQueenside):
            self.getQueensideCastleMoves(r, c, moves, allyColor)

    def getkingsideCastleMoves(self, r, c, moves, allyColor):
        # check if the squre between king and rrok are clear and not under attack
        if self.board[r][c + 1] == '--' and self.board[r][c + 2] == '--' and \
                not self.squareUnderAttack(r, c + 1, allyColor) and not self.squareUnderAttack(r, c + 2, allyColor):
            moves.append(Move((r, c), (r, c + 2), self.board, castle=True))

    def getQueensideCastleMoves(self, r, c, moves, allyColor):
        # check if there square between king and rook are clear and two square left of the king are not under attack
        if self.board[r][c - 1] == '--' and self.board[r][c - 2] == '--' and self.board[r][c - 3] == '--' and \
                not self.squareUnderAttack(r, c - 1, allyColor) and not self.squareUnderAttack(r, c - 2, allyColor):
            moves.append(Move((r, c), (r, c - 2), self.board, castle=True))

    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.whiteCastleKingside = False
            self.whiteCastleQueenside = False
        elif move.pieceMoved == 'bK':
            self.blackCastleKingside = False
            self.blackCastleQueenside = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 7:
                    self.whiteCastleKingside = False
                elif move.startCol == 0:
                    self.whiteCastleQueenside = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 7:
                    self.blackCastleKingside = False
                elif move.startCol == 0:
                    self.blackCastleQueenside = False

        # if rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.whiteCastleQueenside = False
                elif move.endCol == 7:
                    self.whiteCastleKingside = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.blackCastleQueenside = False
                elif move.endCol == 7:
                    self.blackCastleKingside = False


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

    def __init__(self, startSq, endSq, board, enPassant=False, pawnPromotion=False, castle=False, incheck=False,
                 checkmate=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.enPassant = enPassant
        self.pawnPromotion = pawnPromotion
        self.castle = castle
        self.incheck = incheck
        self.Checkmate = checkmate
        if enPassant:
            self.pieceCaptured = 'bP' if self.pieceMoved == 'wP' else 'wP'  # enpassant captures opposite colored pawn
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol
        self.isCapture = self.pieceCaptured != '--'

    '''
    overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    # def getChessNotation(self):
    #
    #     piece = self.pieceMoved[1]
    #     col = self.startCol
    #     row = self.startRow
    #     if piece == "P":
    #         endSquare = self.getRankFile(self.endRow, self.endCol)
    #         if endSquare[1] == '8':
    #             return self.colsToFiles[self.startCol] + endSquare[1] + "=Q"
    #         # if self.pieceCaptured == "bP" or self.pieceCaptured == "wP":
    #         #     return self.getRankFile(row,col) + "x" + self.getRankFile(self.endRow,self.endCol)
    #         if self.isCapture:
    #             return self.colsToFiles[self.startCol] + "x" + endSquare
    #         return self.getRankFile(self.endRow,self.endCol)
    #
    #     elif piece == "R":
    #         if self.pieceCaptured != "--":
    #             return "Rx" + self.getRankFile(self.endRow,self.endCol)
    #         return "R" + self.getRankFile(self.endRow,self.endCol)
    #     elif piece == "N":
    #         if self.pieceCaptured != "--":
    #             return "Nx" + self.getRankFile(self.endRow,self.endCol)
    #         return "N" + self.getRankFile(self.endRow,self.endCol)
    #     elif piece == "B":
    #         if self.pieceCaptured != "--":
    #             return "Bx" + self.getRankFile(self.endRow,self.endCol)
    #         return "B" + self.getRankFile(self.endRow,self.endCol)
    #     elif piece == "Q":
    #         if self.pieceCaptured != "--":
    #             return "Qx" + self.getRankFile(self.endRow,self.endCol)
    #         return "Q" + self.getRankFile(self.endRow,self.endCol)
    #     elif piece == "K":
    #         if self.pieceCaptured != "--":
    #             return "Kx" + self.getRankFile(self.endRow,self.endCol)
    #         return "K" + self.getRankFile(self.endRow,self.endCol)

    # def getChessNotation(self, validMoves):
    #     piece = self.pieceMoved[1]
    #     if piece == "P":
    #         notation = ""
    #         if self.isCapture:
    #             notation += self.colsToFiles[self.startCol] + "x"
    #         notation += self.getRankFile(self.endRow, self.endCol)
    #         if self.endRow == 0 or self.endRow == 7:
    #             notation += "=Q"
    #         return notation
    #
    #     if self.castle:
    #         return "O-O" if self.endCol == 6 else "O-O-O"
    #
    #     disambiguate = ""
    #     similarMoves = [m for m in validMoves if m.pieceMoved == self.pieceMoved and
    #                     m.endRow == self.endRow and m.endCol == self.endCol and m != self]
    #
    #     if similarMoves:
    #         sameFile = any(m.startCol == self.startCol for m in similarMoves)
    #         sameRank = any(m.startRow == self.startRow for m in similarMoves)
    #
    #         if not sameFile:
    #             disambiguate = self.colsToFiles[self.startCol]
    #         elif not sameRank:
    #             disambiguate = self.rowsToRanks[self.startRow]
    #         else:
    #             disambiguate = self.getRankFile(self.startRow, self.startCol)
    #
    #     notation = piece
    #     notation += disambiguate
    #     if self.isCapture:
    #         notation += "x"
    #     notation += self.getRankFile(self.endRow, self.endCol)
    #     return notation

    # def getChessNotation(self, validMoves):
    #     print("notation", self.castle)
    #     if self.castle:
    #         return "O-O" if self.endCol == 6 else "O-O-O"
    #
    #     piece = self.pieceMoved[1]
    #     isPawn = piece == "P"
    #     endSquare = self.getRankFile(self.endRow, self.endCol)
    #
    #     # Determine if disambiguation is needed
    #     disambigFile = disambigRank = False
    #     if not isPawn:
    #         for move in validMoves:
    #             if move.pieceMoved == self.pieceMoved and move != self and move.endRow == self.endRow and move.endCol == self.endCol:
    #                 if move.startCol != self.startCol:
    #                     disambigFile = True
    #                 if move.startRow != self.startRow:
    #                     disambigRank = True
    #
    #     san = ""
    #
    #     if not isPawn:
    #         san += piece
    #         if disambigFile:
    #             san += self.colsToFiles[self.startCol]
    #         if disambigRank:
    #             san += self.rowsToRanks[self.startRow]
    #     if isPawn and self.isCapture:
    #         san += self.colsToFiles[self.startCol]
    #     if self.isCapture:
    #         san += "x"
    #     san += endSquare
    #     if self.pawnPromotion:
    #         san += "=Q"
    #
    #     return san

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

    # def __str__(self):
    #     if self.castle:
    #         return "0-0" if self.endCol == 6 else "0-0-0"
    #
    #     endSquare = self.getRankFile(self.endRow, self.endCol)
    #     if self.pieceMoved[1] == 'P':
    #         if self.isCapture:
    #             return self.colsToFiles[self.startCol] + "x" + endSquare
    #         elif endSquare[1] == '8':
    #             return self.colsToFiles[self.startCol] + endSquare[1] + "=Q"
    #         else:
    #             return endSquare
    #     moveString = self.pieceMoved[1]
    #     if self.isCapture:
    #         moveString += 'x'
    #     return moveString + endSquare

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
        elif self.incheck:
            san += "+"

        return san