from django.urls import path
from django.conf.urls import url
from chat.consumers import ChatConsumer
from tictactoe.consumers import TicTacToeAIConsumer
from tictactoe.consumers import TicTacToeMultiConsumer

websocket_urlpatterns = [
    path('ws/chat', ChatConsumer),
    path('ws/tictactoe/ai', TicTacToeAIConsumer),
    url(r'^ws/tictactoe/multi/(?P<room_name>[^/]+)', TicTacToeMultiConsumer),
]