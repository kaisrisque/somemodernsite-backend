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

    def getComputerMove(self, b):
        # Check computer win moves
        for i in range(0, 9):
            if b[i] is None and self.testWinMove(b, 'O', i):
                return i
        # Check player win moves
        for i in range(0, 9):
            if b[i] is None and self.testWinMove(b, 'X', i):
                return i
        # Check computer fork opportunities
        for i in range(0, 9):
            if b[i] is None and self.testForkMove(b, 'O', i):
                return i
        # Check player fork opportunities, incl. two forks
        playerForks = 0
        for i in range(0, 9):
            if b[i] is None and self.testForkMove(b, 'X', i):
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
        index = self.getComputerMove(board)
        board[index] = "O"
        content = {
            'command': 'tictactoe-AI',
            'board': board
        }
        self.send_move(content)

    commands = {
        'tictactoe-AI': processBoard
    }

    def connect(self):
        self.room_name = 'global'
        self.room_group_name = 'tictactoe_%s' % self.room_name

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

    def send_move(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'board',
                'message': message
            }
        )

    # Receive message from room group
    def board(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))

class TicTacToeMultiConsumer(WebsocketConsumer):
    
    def new_message(self, data):
        author = data['from']
        text = data['text']
        message = {
            "author": author,
            "content": text,
        }
        content = {
            'command': 'new_message',
            'message': message
        }
        self.send_chat_message(content)

    commands = {
        'new_message': new_message
    }

    def connect(self):
        self.room_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
        self.room_group_name = 'tictactoe_AI_%s' % self.room_name

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

    def send_chat_message(self, message):
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        # Send message to WebSocket
        self.send(text_data=json.dumps(message))