from unittest import TestCase

import sys

import trivia



class test1(TestCase):

    def test_one(self):
        sys.stdout = open('reference/test_result.txt', 'w')

        idomero=trivia.Idomero(30)
        
        game = trivia.Game(None, None)

        game.add('Chet')
        game.add('Pat')
        game.add('Sue')

        dice_trows =    [6,6,6,1,3,1,6,4,1,2,4,6,1,2,3,4,2,3,1,1,6,1,6,6,3,4,6,4,4,2,6,4,2,5,5,4,6,4,1,6,5,5,5,5,1,2,3,3,4,4]
        given_answers = [6,9,2,4,7,0,5,1,0,2,8,4,2,3,8,1,2,5,1,7,8,4,5,7,8,1,3,1,9,2,9,6,2,2,1,0,2,6,1,2,8,9,7,1,3,5,2,5,1,3]
        given_time =    [1,2,3,4,5,4,3,3,9,9,9,1,1,9,9,9,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        test_game_states = zip(dice_trows, given_answers, given_time)

        for (throw, answer, time) in test_game_states:
            game.roll(throw)

            timeout = idomero.addanswertime(time)
            if answer == 7:
                not_a_winner = game.wrong_answer()
            else:
                not_a_winner = game.was_correctly_answered()

            ## nyert valaki / lejart az ido / megy tovabb
            if timeout:
                game.close_game('Winner on timeout: ')
                # gyoztes kihirdetese
            elif not not_a_winner:
                # uj jatek a vesztesekkel + az uj jatekossal
                # Erre meg nem keszult teszt
                game.close_game('Winner on max points: ')
                game = trivia.Game(None, None)
                game.add('Sue')
                game.add('Pat')
                game.add('Bob')
                
                

        sys.stdout.close()

        test_file   = open('reference/result.txt', 'r').read()
        test_result = open('reference/test_result.txt', 'r').read()

        self.assertEqual(test_file, test_result)



