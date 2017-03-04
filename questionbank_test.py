from unittest import TestCase

import trivia

class test_qb1(TestCase):
    qb = trivia.QuestionBank();
    qb.create_question('Pop', 'kerdes1')
    qb.create_question('Pop', 'kerdes2')
    qb.create_question('Scinece', 'kerdes3')
    qb.create_question('Sport', 'kerdes4')
    qb.create_question('Rock', 'kerdes5')
    print qb.get_next_question('Pop')
    print qb.get_next_question('Pop')
    print qb.get_next_question('Rock')
    print qb.get_next_question('Pop')
    

class test_qb2(TestCase):
    qb = trivia.QuestionBank();
    qb.create_question('Pop', 'kerdes1')
    qb.create_question('Pop', 'kerdes2')
    qb.create_question('Scinece', 'kerdes3')
    qb.create_question('Sport', 'kerdes4')
    qb.create_question('Rock', 'kerdes5')
    print qb.get_next_question('Pop')
    print qb.get_next_question('Pop')
    print qb.get_next_question('Rock')
    print qb.get_next_question('Pop')

