from unittest import TestCase

import sys

import trivia



class test1(TestCase):

    def test_one(self):
        sys.stdout = open('reference/test_result.txt', 'w')

        game = trivia.Game()

        game.add('Chet')
        game.add('Pat')
        game.add('Sue')

        dice_trows = [6, 6, 6, 1, 3, 1, 6, 4, 1, 2, 4, 6, 1, 2, 3, 4, 2, 3, 1, 1, 6, 1, 6, 6, 3, 4, 6, 4, 4, 2, 6, 4, 2,
                      5, 5, 4, 6, 4, 1, 6, 5, 5, 5, 5, 1, 2, 3, 3, 4, 4]
        given_answers = [6, 9, 2, 4, 7, 0, 5, 1, 0, 2, 8, 4, 2, 3, 8, 1, 2, 5, 1, 7, 8, 4, 5, 7, 8, 1, 3, 1, 9, 2, 9, 6,
                         2, 2, 1, 0, 2, 6, 1, 2, 8, 9, 7, 1, 3, 5, 2, 5, 1, 3]

        test_game_states = zip(dice_trows, given_answers)

        for (throw, answer) in test_game_states:
            game.roll(throw)

            if answer == 7:
                not_a_winner = game.wrong_answer()
            else:
                not_a_winner = game.was_correctly_answered()

            if not not_a_winner: break

        sys.stdout.close()

        test_file   = open('reference/result.txt', 'r').read()
        test_result = open('reference/test_result.txt', 'r').read()

        self.assertEqual(test_file, test_result)
