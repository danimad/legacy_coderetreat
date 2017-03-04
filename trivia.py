#!/usr/bin/env python

from enum import Enum

class Idomero:
    elapsedtime = 0
    maxtime = 0
    def __init__(self, maxtime):
        self.maxtime = maxtime
    
    def addanswertime(self, elapsedtime):
        self.elapsedtime += elapsedtime
        return self.maxtime<=elapsedtime
    

class QuestionType(Enum):
     Pop = 'Pop'
     Science = 'Science'
     Sports = 'Sports'
     Rock= 'Rock'
     History = 'Hist'

class QuestionBank:
    currentindexlist = dict()
    qlist = dict()
    def create_question(self, questiontype, question):
        l = self.qlist.get(questiontype, list())
        l.append(question)
        self.qlist[questiontype] = l
    
    def get_next_question(self, questiontype):
        self.currentindexlist[questiontype] = self.currentindexlist.get(questiontype, -1) + 1
        l = self.qlist.get(questiontype, list())
        if self.currentindexlist[questiontype]>=len(l):
            self.currentindexlist[questiontype] = 0
            print 'kerdes:', self.currentindexlist[questiontype], len(l)
        return l[self.currentindexlist[questiontype]]

    
class Board:
    fields = list()
    def __init__(self):
        for t in [QuestionType.Pop, QuestionType.Science, QuestionType.Sports, QuestionType.Rock, \
                  QuestionType.History, QuestionType.Science, QuestionType.Sports, QuestionType.Rock, \
                  QuestionType.History, QuestionType.Science, QuestionType.Sports, QuestionType.Rock]:
            self.fields.append(t.value)

    def get_field_type(self, index):
        return self.fields[index%len(self.fields)]

    def get_board_size(self):
        return len(self.fields)



class Game:
    qbank = None
    board = None
    def __init__(self, board, questionbank):
        self.players = []
        self.places = [0] * 6
        self.purses = [0] * 6
        self.in_penalty_box = [0] * 6
                
        self.current_player = 0
        self.is_getting_out_of_penalty_box = False
        
        if questionbank == None:
            self.qbank = QuestionBank()
            for i in range(50):
                for qType in QuestionType:
                    qt= qType.value #repr(qType).split(".")[1]
                    self.qbank.create_question(qt, qt+' Question '+str(i))
#                    print 'Added '+qt, qt+' Question '+str(i)
        else:
            self.qbank = questionbank
        
        if board == None:
            self.board = Board()
        else:
            self.board = board
    
    def create_rock_question(self, index):
        return "Rock Question %s" % index
    
    def is_playable(self):
        return self.how_many_players >= 2
    
    def add(self, player_name):
        self.players.append(player_name)
        self.places[self.how_many_players] = 0
        self.purses[self.how_many_players] = 0
        self.in_penalty_box[self.how_many_players] = False
        
        print player_name + " was added"
        print "They are player number %s" % len(self.players)
        
        return True
    
    @property
    def how_many_players(self):
        return len(self.players)
    
    def roll(self, roll):
        print "%s is the current player" % self.players[self.current_player]
        print "They have rolled a %s" % roll
        
        if self.in_penalty_box[self.current_player]:
            if roll % 2 != 0:
                self.is_getting_out_of_penalty_box = True
                
                print "%s is getting out of the penalty box" % self.players[self.current_player]
                self.places[self.current_player] = self.places[self.current_player] + roll
                if self.places[self.current_player] > 11:
                    self.places[self.current_player] = self.places[self.current_player] - 12
                
                print self.players[self.current_player] + \
                            '\'s new location is ' + \
                            str(self.places[self.current_player])
                print "The category is %s" % self._current_category
                self._ask_question()
            else:
                print "%s is not getting out of the penalty box" % self.players[self.current_player]
                self.is_getting_out_of_penalty_box = False
        else:
            self.places[self.current_player] = self.places[self.current_player] + roll
            if self.places[self.current_player] > 11:
                self.places[self.current_player] = self.places[self.current_player] - 12
            
            print self.players[self.current_player] + \
                        '\'s new location is ' + \
                        str(self.places[self.current_player])
            print "The category is %s" % self._current_category
            self._ask_question()
    
    def _ask_question(self):
        q = self.qbank.get_next_question(self.board.get_field_type(self.places[self.current_player]))
        print q
        

    
    @property
    def _current_category(self):
        if self.places[self.current_player] == 0: return 'Pop'
        if self.places[self.current_player] == 4: return 'Pop'
        if self.places[self.current_player] == 8: return 'Pop'
        if self.places[self.current_player] == 1: return 'Science'
        if self.places[self.current_player] == 5: return 'Science'
        if self.places[self.current_player] == 9: return 'Science'
        if self.places[self.current_player] == 2: return 'Sports'
        if self.places[self.current_player] == 6: return 'Sports'
        if self.places[self.current_player] == 10: return 'Sports'
        return 'Rock'

    def was_correctly_answered(self):
        if self.in_penalty_box[self.current_player]:
            if self.is_getting_out_of_penalty_box:
                print 'Answer was correct!!!!'
                self.purses[self.current_player] += 1
                print self.players[self.current_player] + \
                    ' now has ' + \
                    str(self.purses[self.current_player]) + \
                    ' Gold Coins.'
                
                winner = self._did_player_win()
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                
                return winner
            else:
                self.current_player += 1
                if self.current_player == len(self.players): self.current_player = 0
                return True
            
            
            
        else:
            
            print "Answer was corrent!!!!"
            self.purses[self.current_player] += 1
            print self.players[self.current_player] + \
                ' now has ' + \
                str(self.purses[self.current_player]) + \
                ' Gold Coins.'
            
            winner = self._did_player_win()
            self.current_player += 1
            if self.current_player == len(self.players): self.current_player = 0
            
            return winner
    
    def wrong_answer(self):
        print 'Question was incorrectly answered'
        print self.players[self.current_player] + " was sent to the penalty box"
        self.in_penalty_box[self.current_player] = True
        
        self.current_player += 1
        if self.current_player == len(self.players): self.current_player = 0
        return True
    
    def _did_player_win(self):
        return not (self.purses[self.current_player] == 6)

    def close_game(self, reason):
        # 1 embernek van-e max pontja?
        # ha igen, akkor o a gyoztes.
        # ha nem toroljuk a nem-gyozteseket
        # gyozelem feltetele megvaltozik, hogy a kor vegen kinek vna a legtobb pontja
        maxval=max(self.purses)
        maxindex=self.purses.index(maxval)
        print reason + self.players[maxindex]
        
    
    
from random import randrange

if __name__ == '__main__':
    not_a_winner = False

    game = Game()

    game.add('Chet')
    game.add('Pat')
    game.add('Sue')

    dice_trows =    [6,6,6,1,3,1,6,4,1,2,4,6,1,2,3,4,2,3,1,1,6,1,6,6,3,4,6,4,4,2,6,4,2,5,5,4,6,4,1,6,5,5,5,5,1,2,3,3,4,4]
    given_answers = [6,9,2,4,7,0,5,1,0,2,8,4,2,3,8,1,2,5,1,7,8,4,5,7,8,1,3,1,9,2,9,6,2,2,1,0,2,6,1,2,8,9,7,1,3,5,2,5,1,3]
    given_time =    [1,2,3,4,5,4,3,3,9,9,9,1,1,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

    test_game_states = zip(dice_trows, given_answers, given_time)
    idomero = Idomero(30)

    for (throw, answer, time) in test_game_states:
        game.roll(throw)

        if answer == 7:
            not_a_winner = game.wrong_answer()
        else:
            not_a_winner = game.was_correctly_answered()

        if not not_a_winner: break

        
            

    # while True:
    #     game.roll(randrange(5) + 1)
    #
    #     if randrange(9) == 7:
    #         not_a_winner = game.wrong_answer()
    #     else:
    #         not_a_winner = game.was_correctly_answered()
    #
    #     if not not_a_winner: break
