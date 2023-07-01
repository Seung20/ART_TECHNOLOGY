import pygame
import numpy as np 
import os
import sys
from pygame.locals import *

# 게임 윈도우 크기
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 1000

# 색 정의
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)


# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("TicTacToe")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

#박스 크기들과 박스의 사이즈 정의
gap = 15
size = 280

#박스(버튼)의 위치를 정의
pos_x = [(gap), (gap*2 + size), (gap*3 + size*2), (gap), (gap*2 + size), (gap*3 + size*2), (gap), (gap*2 + size), (gap*3 + size*2)]
pos_y = [(gap*3 + size*2), (gap*3 + size*2), (gap*3 + size*2), (gap*2 + size),(gap*2 + size),(gap*2 + size),(gap) ,(gap), (gap)]


# 9개의 버튼을 만들고, board[1]~board[9]까지 저장
# board[7] board[8] board[9]
# board[4] board[5] board[6]
# board[1] board[2] board[3]

losboard = "YOULOSE^^!".split()

# 박스(버튼) 그리기
def drawBoard(board):
    for i in range(0, 9):
        pygame.draw.rect(screen,GREY,[pos_x[i], pos_y[i], size, size])
    for t in range(1, 10):
        ttext = c_font.render(board[t], True, BLACK)
        screen.blit(ttext,(pos_x[t-1]+20, pos_y[t-1]-10))


# player는 O로 고정, computer는 X로 고정
def inputPlayerLetter():
    return ['O', 'X']

# 선공 정하기
# random하게 computer나 player둘중에 골라서 선공을 한다.
def whoGoesFirst():
    # Randomly choose the player who goes first.
    if np.random.randint(0, 2) == 0:
        return 'computer'
    else:
        return 'player'

def makeMove(board, letter, move):
    board[move] = letter

#board(박스)에 letter에 있으면 이기는 경우의 수를 정의했다.
def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or 
    (bo[4] == le and bo[5] == le and bo[6] == le) or 
    (bo[1] == le and bo[2] == le and bo[3] == le) or 
    (bo[7] == le and bo[4] == le and bo[1] == le) or 
    (bo[8] == le and bo[5] == le and bo[2] == le) or 
    (bo[9] == le and bo[6] == le and bo[3] == le) or 
    (bo[7] == le and bo[5] == le and bo[3] == le) or 
    (bo[9] == le and bo[5] == le and bo[1] == le)) 

#board(박스) 복사하기
def getBoardCopy(board):
    boardCopy = []
    for i in board:
        boardCopy.append(i)
    return boardCopy

#빈 board(박스)인지 확인하는 함수
def isSpaceFree(board, move):
    return board[move] == ' '

#possibleMoves라는 array를 만들고, 여기에 빈칸인 board들을 넣는다.
#빈칸이 없는 경우를 제외하고, 빈칸이 있는 경우에는 이 possibleMoves 배열에서 random하게 return한다.
def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if isSpaceFree(board, i):
            possibleMoves.append(i)

    if len(possibleMoves) != 0:
        return np.random.choice(possibleMoves)
    else:
        return None

#컴퓨터의 순서에서의 컴퓨터의 동작
def getComputerMove(board, computerLetter):
    playerLetter = 'O'
    computerLetter = 'X'
    
    #player가 어떤 빈칸을 넣었을 때, 이기는 상황일 때 그 빈칸을 막는다.
    for i in range(1, 10):
        boardCopy = getBoardCopy(board)
        if isSpaceFree(boardCopy, i):
            makeMove(boardCopy, playerLetter, i)
            if isWinner(boardCopy, playerLetter):
                return i

    #제일 승률이 큰 1 3 7 9를 우선으로 고려한다.
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move != None:
        return move

    # 그 다음 승률이 큰 중간값인 5를 고려한다.
    if isSpaceFree(board, 5):
        return 5

    # 그 후 남은 2, 4, 6, 8 중 하나를 고른다.
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

#다 차있으면 true를 아니라면 false를 return한다.
def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True
    
#폰트
a_font = pygame.font.SysFont('onyx', 50)
b_font = pygame.font.SysFont('onyx', 40)
c_font = pygame.font.SysFont('onyx', 400)
starting_text = a_font.render("Tic Tac Toe", True, BLACK)


# # 게임 종료 전까지 반복
done = False
theBoard = [' '] * 10
playerLetter, computerLetter = inputPlayerLetter()
turn = whoGoesFirst()

showingturntext = b_font.render("The " + turn + " will go first", True, BLACK)

# 게임 반복 구간
while not done:
    # 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == MOUSEBUTTONUP: #마우스 버튼이 눌러지고 떠질 때
            mpos = pygame.mouse.get_pos()
            # 사용자 순서
            if turn == 'player':
                drawBoard(theBoard)
                move = ' '
   
                for i in range(9):
                    if (pos_x[i] <= mpos[0] <= pos_x[i] + size) and (pos_y[i] <=mpos[1] <= pos_y[i] + size):       
                        move = i+1 

                makeMove(theBoard, playerLetter, move)

                if isWinner(theBoard, playerLetter):
                    drawBoard(theBoard)
                    pygame.time.delay(2000)
                    done = True
                    

                    
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        pygame.time.delay(2000)
                        done = True
                        break
                    else:
                        turn = 'computer'


            else:
                # 컴퓨터 턴
                move = getComputerMove(theBoard, computerLetter)
                makeMove(theBoard, computerLetter, move)

                if isWinner(theBoard, computerLetter):
                    pygame.time.delay(2000)
                    done = True
                    
                    
                        
                else:
                    if isBoardFull(theBoard):
                        drawBoard(theBoard)
                        done = True
                        pygame.time.delay(2000)
                        break
                    else:
                        turn = 'player'
            
    screen.fill(WHITE)
    drawBoard(theBoard)
    screen.blit(starting_text, (WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2 + 400))
    screen.blit(showingturntext, (WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 + 450))
    
    # 화면 업데이트
    pygame.display.flip()
    
    clock.tick(60) 

# 게임 종료
pygame.quit()