'''
 This is our main driver file. it will responsible for handling user input and s+displaying the current GameState object
'''
import os
import datetime
import pygame as p
from Chess_AI import ChessEngine as ChessEngine
from Chess_AI import ChessAI
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
BOARD_WIDTH = 680
BOARD_TOP_PADDING = 40
BOARD_BOTTOM_PADDING = 40
BOARD_HEIGHT = 680 + BOARD_TOP_PADDING + BOARD_BOTTOM_PADDING  #760 total
MOVE_LOG_PANEL_WIDTH = 380
MOVE_LOG_PANEL_HIGHT = BOARD_HEIGHT
DIMENTSION = 8 # dimensions of a chess board are 8x8
SQ_SIZE = 680 // DIMENTSION
MAX_FPS = 30
IMAGES = {}
Chess_AI_name = "Ghost"
WHITE_PLAYER_NAME = "Human"
BLACK_PLAYER_NAME = "Ghost"

'''
initialize a globle dictinary of images. this will be called exactly once in main
'''
def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bP', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/"+piece + ".png"),(SQ_SIZE, SQ_SIZE))
    #note: we can access an image by saving 'IMAGES['wP']'

'''
this is main driver this will handle user input and update the graphics
'''
def main():
    p.init()
    screen = p.display.set_mode((BOARD_WIDTH + MOVE_LOG_PANEL_WIDTH, BOARD_HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont("Arial Black", 13, False, False)
    font = p.font.SysFont("Georgia", 24, True)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    animate = False # flag variable for when we should animate a move
    moveMade = False # flag variable for when a move is made
    loadImages() # only do this once, before the white loop
    running = True
    sqSelected =()  # no square is selected, keep track of the last click of the user (tuple: (row, cloumn))
    playerClick = [] # keep track of player click (two tuple: [(6,4), (4,4)])
    gameOver = False
    resign = False
    playerOne = True  # if a human is playing white this will True, if an AI playing then False
    playerTwo = False # same as above but for black
    pgnsaved = False

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN :
                location = p.mouse.get_pos()  # (x,y) location of mouse
                # col = location[0]//SQ_SIZE
                # row = location[1]//SQ_SIZE
                x, y = location
                resign_button = drawResignButton(screen, 680, 778, font)
                if resign_button.collidepoint(location):
                    gameOver = True
                    resign =True
                if not gameOver and humanTurn:
                    if BOARD_TOP_PADDING <= y <= BOARD_TOP_PADDING + 680 and x <= 760:
                        col = x // SQ_SIZE
                        row = (y - BOARD_TOP_PADDING) // SQ_SIZE
                        if 0 <= col < 8 and 0 <= row < 8:
                            if sqSelected == (row, col) or col >= 8: # the user clicked the same square twice
                                sqSelected =()  # deselect
                                playerClick= [] # clear player click
                            else:
                                sqSelected = (row, col)
                                playerClick.append(sqSelected) # append for both 1st and 2nd clicks
                            if len(playerClick) == 2: # after 2nd click
                                move = ChessEngine.Move(playerClick[0], playerClick[1], gs.board)
                                for i in range(len(validMoves)):
                                    if move == validMoves[i]:
                                        # gs.makeMove(validMoves[i])
                                        # moveMade = True
                                        # animate = True
                                        # print(move.getChessNotation(validMoves))
                                        # sqSelected = ()   # reset the user click
                                        # playerClick = []
                                        move = validMoves[i]
                                        gs.makeMove(move)
                                        move.validMoves = validMoves
                                        if gs.checkmate:
                                            print("checkmate")
                                            move.Checkmate = True
                                        if gs.inCheck:
                                            move.inCheck = True

                                        moveMade = True
                                        animate = True
                                        print(str(move))  # or print(move.getChessNotation(validMoves)) if needed
                                        sqSelected = ()
                                        playerClick = []

                                if not moveMade:
                                    playerClick = [sqSelected]
            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r : # reset the board when r is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClick = []
                    moveMade = False
                    animate = False
                    gameOver = False
                    pgnsaved = False

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMove(validMoves)
                if AIMove is None:
                    gs.checkmate = True
                    gameOver = True
                    drawEndGameText(screen,'Draw by Stalemate' if gs.stalemate
                                    else 'Black wins by checkmate'
                                    if gs.whiteToMove else 'White wins by checkmate')
            # gs.makeMove(AIMove)
            # moveMade = True
            # animate = True
           # print(AIMove.getChessNotation(validMoves))
            gs.makeMove(AIMove)
            AIMove.validMoves = validMoves
            if gs.inCheck:
                AIMove.incheck = True
            if gs.checkmate:
                AIMove.Checkmate = True
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkmate or resign:
            gameOver = True

        if gameOver:
            if gs.checkmate:
                drawEndGameText(screen, 'Draw by Stalemate' if gs.stalemate else 'Black wins by checkmate' if gs.whiteToMove else 'White wins by checkmate')
            elif resign:
                drawEndGameText(screen, 'Black wins by Resignation' if gs.whiteToMove else 'White wins by Resignation')
        if e.type == p.QUIT:
            if not pgnsaved and len(gs.moveLog) > 0:
                writePGN(gs.moveLog,playerOne,playerTwo)
                pgnsaved = True
            running = False

        if gameOver and not pgnsaved:
            if gs.checkmate:
                result = "1-0" if not gs.whiteToMove else "0-1"
            elif gs.stalemate:
                result = "1/2-1/2"
            else:
                result = "*"

            writePGN(gs.moveLog,playerOne,playerTwo, result=result)
            pgnsaved = True
        clock.tick(MAX_FPS)
        p.display.flip()

def writePGN(moveLog, wName, bName, result="*", output_dir="games"):
    if wName:
        whiteName = "human"
    else:
        whiteName = Chess_AI_name
    if bName:
        blackName = "human"
    else:
        blackName = Chess_AI_name
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Prepare headers
    now = datetime.datetime.now()
    date = now.strftime("%Y.%m.%d")
    time = now.strftime("%H:%M")
    headers = [
        f'[Event "Casual Game"]',
        f'[Site "Local"]',
        f'[Date "{date}"]',
        f'[Time "{time}"]',
        f'[White "{whiteName}"]',
        f'[Black "{blackName}"]',
        f'[Result "{result}"]'
    ]

    # Build moves in SAN format with move numbers
    moves = []
    for i in range(0, len(moveLog), 2):
        turn = f"{(i // 2) + 1}."
        whiteMove = str(moveLog[i])
        blackMove = str(moveLog[i + 1]) if i + 1 < len(moveLog) else ""
        moves.append(f"{turn} {whiteMove} {blackMove}".strip())

    # Combine all parts
    body = " ".join(moves)
    full_pgn = "\n".join(headers) + "\n\n" + body + f" {result}\n"

    # Save with a timestamp-based filename
    filename = f"{date}-{time.replace(':', '-')}.pgn"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w") as f:
        f.write(full_pgn)
    print(f"PGN saved to {filepath}")

'''
Responsible for graphics within a current game state
'''
def drawGameState(screen,gs, validMoves, sqSelected, moveLogFont):
    font = p.font.SysFont("Georgia", 24, True)
    TOP_BAR_COLOR = p.Color("wheat")  # or any color you want
    BOTTOM_BAR_COLOR = p.Color("wheat")

    # Draw top padding bar (above the board)
    top_bar_rect = p.Rect(0, 0, 680, BOARD_TOP_PADDING)
    p.draw.rect(screen, TOP_BAR_COLOR, top_bar_rect)

    # Draw bottom padding bar (below the board)
    bottom_bar_rect = p.Rect(0, 760 - BOARD_BOTTOM_PADDING, 680, BOARD_BOTTOM_PADDING)
    p.draw.rect(screen, BOTTOM_BAR_COLOR, bottom_bar_rect)
    #draw the resign button
    drawResignButton(screen,680,778,font)
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of those squares
    drawPlayerNames(screen)
    drawMoveLog(screen, gs, moveLogFont)

'''
display the respective player name
'''
def drawPlayerNames(screen):
    font = p.font.SysFont("Georgia", 20, True)

    # White player name (bottom center)
    whiteText = font.render(WHITE_PLAYER_NAME, True, p.Color('black'))
    whitePosX = 25
    whitePosY = 45 + 680   # below the board

    screen.blit(whiteText, (whitePosX, whitePosY))

    # Black player name (top center)
    blackText = font.render(BLACK_PLAYER_NAME, True, p.Color('black'))
    blackPosX = 25
    blackPosY = 5  # nice padding above board
    screen.blit(blackText, (blackPosX, blackPosY))
'''
draw the squeres on the board. the top left square is always light.
'''
def drawBoard(screen):
    global colors
    colors = [p.Color("burlywood"), p.Color("saddlebrown")]
    for r in range(DIMENTSION):
        for c in range(DIMENTSION):
            color =colors[((r+c)%2)]
            rect = p.Rect(c*SQ_SIZE ,BOARD_TOP_PADDING + r*SQ_SIZE,SQ_SIZE,SQ_SIZE)
            p.draw.rect(screen,color,rect)

'''
highlight square selected and moves for peice selected
'''
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if 0 <= r < 8 and 0 <= c < 8 and gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a peice that can move
            #highlight selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(200) #transperancy value -> 0 transparent; 255 opaque
            selected_color = p.Color('black')
            move_hint_color = p.Color('dark gray')
            s.fill(selected_color) #blue
            screen.blit(s, (c*SQ_SIZE, BOARD_TOP_PADDING + r*SQ_SIZE))
            #highlight moves from that square
            s.fill(move_hint_color)#yellow
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    # r_pos = BOARD_TOP_PADDING + r * SQ_SIZE
                    # screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r_pos, SQ_SIZE, SQ_SIZE))
                    screen.blit(s, (move.endCol*SQ_SIZE,BOARD_TOP_PADDING + move.endRow*SQ_SIZE))
'''
draw pieces on the board using the current GameState,board
'''
def drawPieces(screen,board):
    for r in range(DIMENTSION):
        for c in range(DIMENTSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece],p.Rect(c*SQ_SIZE, BOARD_TOP_PADDING + r*SQ_SIZE,SQ_SIZE,SQ_SIZE))
'''
draw the move log
'''
def drawMoveLog(screen, gs, font):
    moveLogRect = p.Rect(BOARD_WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    movelog = gs.moveLog
    moveTexts = []
    for i in range(0, len(movelog), 1):
        moveString = str(i + 1) + ".  " + str(movelog[i]) + "  "
        # if i + 1 < len(movelog): #make sure black made a move
        #     moveString += movelog[i+1].getChessNotation()
        moveTexts.append(moveString)

    movesPerRow = 5
    padding = 5
    textY = padding
    lineSpacing = 2
    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if  i + j < len(moveTexts):
                text += moveTexts[i+j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation = moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + lineSpacing
'''
animating move
'''
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of coord that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move one square
    #frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    frameCount = 20
    for frame in range(frameCount + 1):
        # r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        # r = BOARD_TOP_PADDING + (move.startRow + dR * frame / frameCount) * SQ_SIZE
        # c = (move.startCol + dC * frame / frameCount) * SQ_SIZE

        # Calculate the intermediate position for each frame
        r = move.startRow + dR * frame / frameCount
        c = move.startCol + dC * frame / frameCount

        # Convert to screen coordinates
        r_pos = BOARD_TOP_PADDING + r * SQ_SIZE
        c_pos = c * SQ_SIZE

        drawBoard(screen)
        drawPieces(screen, board)
        #erace the peice moved from it's ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE,BOARD_TOP_PADDING + move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            if move.enPassant:
                enpassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol * SQ_SIZE,BOARD_TOP_PADDING+enpassantRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        #screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c_pos, r_pos, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

def drawEndGameText(screen, text):
    font = p.font.SysFont("Arial Black", 32, True, False)
    textObject = font.render(text, 0, p.Color('Grey'))
    textLocation = p.Rect(0, 0, BOARD_WIDTH, BOARD_HEIGHT).move(BOARD_WIDTH/2 - textObject.get_width()/2, BOARD_HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("Black"))
    screen.blit(textObject, textLocation.move(2, 2))

def drawResignButton(screen, width, height, font):
    button_width = 150
    button_height = 35
    button_color = p.Color("saddlebrown")  # red-ish
    text_color = p.Color("black")  # white

    # Positioning: center bottom
    x = (width - button_width) // 2
    y = height - button_height - 20  # 20px above bottom

    # Draw button rectangle
    resign_button = p.Rect(x, y, button_width, button_height)
    p.draw.rect(screen, button_color, resign_button, border_radius=10)

    # Render text
    text_surface = font.render("Resign", True, text_color)
    text_rect = text_surface.get_rect(center=resign_button.center)
    screen.blit(text_surface, text_rect)

    return resign_button  # return rect so you can detect clicks

def Resigned(screen,gs):
    drawEndGameText(screen, 'Black wins by Resignation' if gs.whiteToMove else 'White wins by Resignation')

if __name__ == "__main__":
    main()
