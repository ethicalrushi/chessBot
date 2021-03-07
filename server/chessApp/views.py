from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import chess
import chess.engine

# Create your views here.

def getBoard(request):
    return render(request, 'chess.html')

@csrf_exempt
def getAIMove(request):
    if request.method == 'POST':
        print(request.body)
        data = json.loads(request.body.decode('UTF-8'))
        fen = data['fen']
        move = data['move']
        
        board = chess.Board(fen)
        with chess.engine.SimpleEngine.popen_uci('stockfish_13_win_x64\stockfish_13_win_x64\stockfish_13_win_x64.exe') as engine:
            move = engine.analyse(board, chess.engine.Limit(time=1), info=chess.engine.INFO_PV)['pv'][0]
            move = move.uci()
            resultMove = {'from':move[:2], 'to':move[2:]}

        return JsonResponse({"move":resultMove})
    return JsonResponse({"false":False})