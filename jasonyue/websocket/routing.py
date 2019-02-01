from django.urls import path
from chat.consumers import ChatConsumer
from tictactoe.consumers import TicTacToeAIConsumer
from tictactoe.consumers import TicTacToeMultiConsumer

websocket_urlpatterns = [
    path('ws/chat', ChatConsumer),
    path('ws/tictactoe/ai', TicTacToeAIConsumer),
    path('ws/tictactoe/multi', TicTacToeMultiConsumer),
]