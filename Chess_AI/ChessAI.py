import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "P": 1}

whitePawnScores = [[5, 5, 5, 5, 5, 5, 5, 5],
                   [4, 4, 4, 4, 4, 4, 4, 4],
                   [2, 2, 3, 3, 3, 3, 2, 2],
                   [2, 2, 3, 3, 3, 3, 2, 2],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [1, 1, 2, 2, 2, 2, 1, 1],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0]]

blackPawnScores = [[0, 0, 0, 0, 0, 0, 0, 0],
                   [1, 1, 1, 0, 0, 1, 1, 1],
                   [1, 1, 2, 2, 2, 2, 1, 1],
                   [1, 2, 3, 4, 4, 3, 2, 1],
                   [2, 2, 3, 3, 3, 3, 2, 2],
                   [2, 2, 3, 3, 3, 3, 2, 2],
                   [4, 4, 4, 4, 4, 4, 4, 4],
                   [5, 5, 5, 5, 5, 5, 5, 5]]

knightScores = [[1, 1, 1, 1, 1, 1, 1, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 4, 4, 3, 2, 1],
                [1, 2, 3, 3, 3, 3, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 1, 1, 1, 1, 1, 1, 1]]

bishopScores = [[2, 2, 2, 1, 1, 2, 2, 2],
                [3, 4, 3, 2, 2, 3, 4, 3],
                [1, 2, 4, 3, 3, 4, 2, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [1, 3, 3, 4, 4, 3, 3, 1],
                [2, 2, 4, 3, 3, 4, 2, 2],
                [3, 4, 2, 2, 2, 2, 4, 3],
                [2, 2, 2, 1, 1, 2, 2, 2]]

queenScores = [[2, 2, 2, 3, 2, 2, 2, 2],
                [2, 3, 3, 3, 3, 3, 3, 2],
                [2, 3, 4, 4, 4, 4, 3, 2],
                [2, 3, 4, 5, 5, 4, 3, 2],
                [2, 3, 4, 5, 5, 4, 3, 2],
                [2, 3, 4, 4, 4, 4, 3, 2],
                [2, 3, 3, 3, 3, 3, 3, 2],
                [2, 2, 2, 3, 2, 2, 2, 2]]

rookScores = [[3, 3, 4, 4, 4, 4, 3, 3],
                [2, 3, 3, 3, 3, 3, 3, 2],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [1, 2, 2, 3, 3, 2, 2, 1],
                [1, 2, 2, 3, 3, 2, 2, 1],
                [1, 2, 2, 2, 2, 2, 2, 1],
                [2, 3, 3, 3, 3, 3, 3, 2],
                [3, 3, 4, 4, 4, 4, 3, 3]]

piecePositionScores = {"N": knightScores, "Q" :queenScores, "B": bishopScores, "R": rookScores, "wP": whitePawnScores,
                       "bP": blackPawnScores}

CHECKMATE = 10000
STALEMATE = 0
DEPTH =2
'''
picks and returns a random move
'''
def findRandomMove(validMoves):
    #return validMoves[random.shuffle(validMoves)] // it will alwase return the None type
    #return validMoves[random.choice(validMoves)] #// it will directly return the move not valid
    return random.choice(validMoves)  #this should works perfectly.
'''
Find the best move based on matrial alon
'''
# def findBestMoveMinMaxNoRecursion(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         opponentsMoves = gs.getValidMoves()
#         if gs.checkmate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkmate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for opponentsMove in opponentsMoves:
#                 gs.makeMove(opponentsMove)
#                 gs.getValidMoves()
#                 if gs.checkmate:
#                     score = CHECKMATE
#                 elif gs.stalemate:
#                     score = STALEMATE
#                 else:
#                     score = -turnMultiplier * scoreMaterial(gs.board)
#                 if score > opponentMaxScore:
#                     opponentMaxScore = score
#                 gs.undoMove()
#         if opponentMaxScore < opponentMinMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove
'''
helper method to make first recursive call
'''
def findBestMove(gs, validMoves):
    global nextMove
    nextMove = None
    #findMoveMinMax(gs, validMoves, DEPTH, gs.whiteToMove)
    #findMoveNegaMax(gs, validMoves, DEPTH,  1 if gs.whiteToMove else -1)
    findMoveNegaMaxAlphaBeta(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1)
    return nextMove

def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)
    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore =  score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove

    if gs.checkmate:
        return -CHECKMATE if gs.whiteToMove else CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    if depth == 0:
        validMoves = gs.getValidMoves()
        if len(validMoves) == 0:
            if gs.inCheck:
                return -CHECKMATE
            else:
                return STALEMATE
        return turnMultiplier * scoreBoard(gs)
    #move ordering - implement later
    validMoves.sort(key=lambda move: move.pieceCaptured != '--', reverse=True)
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        # Add this block to detect checkmate/stalemate mid-search
        if len(nextMoves) == 0:
            if gs.inCheck:
                score = -CHECKMATE
            else:
                score = STALEMATE
        else:
            score = -findMoveNegaMaxAlphaBeta(gs, nextMoves, depth-1, -beta, -alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move, score)
        gs.undoMove()
        if maxScore > alpha:
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore
'''
A positive score is good for white and negative score is good for black
'''
def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(gs.board)):
        for col in range(len(gs.board[row])):
            square = gs.board[row][col]
            if square != "--":
                piecePositionScore = 0
                #score it positionally
                if square[1] != "K":
                    if square[1] == "P": #for pwan
                        piecePositionScore = piecePositionScores[square][row][col]
                    else: #for other piece
                        piecePositionScore = piecePositionScores[square[1]][row][col]
                if square[0] == 'w':
                    score += pieceScore[square[1]] + piecePositionScore * .1
                elif square[0] == 'b':
                    score -= pieceScore[square[1]] + piecePositionScore * .1
    return score
'''
Score the board based on material.
'''
def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == 'w':
                score += pieceScore[square[1]]
            elif square[0] == 'b':
                score -= pieceScore[square[1]]
    return score