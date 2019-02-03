# tictactoe/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json, string, random

class TicTacToeAIConsumer(WebsocketConsumer):
    def getBoardCopy(self, b):
        # Make a duplicate of the board. When testing moves we don't want to 
        # change the actual board
        dupeBoard = []
        for j in b:
            dupeBoard.append(j)
        return dupeBoard

    def checkWin(self, b, m):
        return ((b[0] == m and b[1] == m and b[2] == m) or  # H top
                (b[3] == m and b[4] == m and b[5] == m) or  # H mid
                (b[6] == m and b[7] == m and b[8] == m) or  # H bot
                (b[0] == m and b[3] == m and b[6] == m) or  # V left
                (b[1] == m and b[4] == m and b[7] == m) or  # V centre
                (b[2] == m and b[5] == m and b[8] == m) or  # V right
                (b[0] == m and b[4] == m and b[8] == m) or  # LR diag
                (b[2] == m and b[4] == m and b[6] == m))  # RL diag

    def testWinMove(self, b, mark, i):
        # b = the board
        # mark = 0 or X
        # i = the square to check if makes a win 
        bCopy = self.getBoardCopy(b)
        bCopy[i] = mark
        return self.checkWin(bCopy, mark)

    def testForkMove(self, b, mark, i):
    # Determines if a move opens up a fork
        bCopy = self.getBoardCopy(b)
        bCopy[i] = mark
        winningMoves = 0
        for j in range(0, 9):
            if self.testWinMove(bCopy, mark, j) and bCopy[j] is None:
                winningMoves += 1
        return winningMoves >= 2

    def getComputerMove(self, b, cpu, player):
        # Check computer win moves
        for i in range(0, 9):
            if b[i] is None and self.testWinMove(b, cpu, i):
                return i
        # Check player win moves
        for i in range(0, 9):
            if b[i] is None and self.testWinMove(b, player, i):
                return i
        # Check computer fork opportunities
        for i in range(0, 9):
            if b[i] is None and self.testForkMove(b, cpu, i):
                return i
        # Check player fork opportunities, incl. two forks
        playerForks = 0
        for i in range(0, 9):
            if b[i] is None and self.testForkMove(b, player, i):
                playerForks += 1
                tempMove = i
        if playerForks == 1:
            return tempMove
        elif playerForks == 2:
            for j in [1, 3, 5, 7]:
                if b[j] is None:
                    return j
        # Play center
        if b[4] is None:
            return 4
        # Play a corner
        for i in [0, 2, 6, 8]:
            if b[i] is None:
                return i
        #Play a side
        for i in [1, 3, 5, 7]:
            if b[i] is None:
                return i
    
    def processBoard(self, data):
        board = data['board']
        player = data['player']
        cpu = "O"
        if player == "O":
            cpu = "X"
        index = self.getComputerMove(board, cpu, player)
        board[index] = cpu
        content = {
            'command': 'tictactoe-AI',
            'board': board
        }
        self.send_move(content)

    commands = {
        'tictactoe-AI': processBoard
    }

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        # leave group room
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_move(self, message):
        # Send message to room group
        self.send(text_data=json.dumps(message))

class TicTacToeMultiConsumer(WebsocketConsumer):
    def processBoard(self, data):
        board = data['board']
        player = data['player']
        content = {
            'command': 'tictactoe-multi',
            'board': board,
            'player': player,
        }
        self.send_move_channel(content)

    def processMessage(self, data):
        message = data['message']
        playerId= data['playerId']
        content = {
            'command': 'tictactoe-multimessage',
            'message': message,
            'playerId': playerId
        }
        self.send_move_channel(content)

    commands = {
        'tictactoe-multi': processBoard,
        'tictactoe-multimessage': processMessage,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'tictactoe_multi_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # leave group room
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_move_channel(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'send_move',
                'message': message
            }
        )

    # Receive message from room group
    def send_move(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))