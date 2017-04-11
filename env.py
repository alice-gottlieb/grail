from pymongo import MongoClient

import chess
import chess.uci
from modules.fishnet.fishnet import stockfish_command

from modules.Game import GameDB
from modules.PlayerAssessment import PlayerAssessmentDB
from modules.GameAnalysis import GameAnalysisDB

class IrwinEnv:
  def __init__(self, settings):
    self.engine = chess.uci.popen_engine(stockfish_command(False))
    self.engine.setoption({'Threads': settings.threads, 'Hash': settings.memory, 'multipv': 5})
    self.engine.uci()
    self.infoHandler = chess.uci.InfoHandler()
    self.engine.info_handlers.append(self.infoHandler)

    # Set up mongodb
    self.client = MongoClient()
    self.db = self.client.irwin

    # Colls
    self.playerColl = self.db.player
    self.GameAnalysisColl = self.db.gameAnalysis
    self.gameColl = self.db.game
    self.assessColl = self.db.assessments

    # database abstraction
    self.gameDB = GameDB(self.gameColl)
    self.playerAssessmentDB = PlayerAssessmentDB(self.assessColl)
    self.gameAnalysisDB = GameAnalysisDB(self.GameAnalysisColl)