# -*- coding:utf-8 -*-
from __future__ import division

import testgen_lib
from testgen_lib import *
     
class csd_question_ttype(test_question_text):
    def randomize(self):
        q_num = random.randint(0, len(self.questions)-1)
        super().SetQuestionText(self.questions[q_num])
        super().SetCorrAnswerText(self.answers[q_num])
        
    def __init__(self):
        super().__init__()
        self.questions = []
        self.answers = []
        
        self.questions.append("Write answer (1.5 is correct)")
        self.questions.append("Write answer (4.0 is correct)")
        self.questions.append("Write answer (12 is correct)")
        self.questions.append("Write answer (274.3 is correct)")
        
        self.answers.append("1.5")
        self.answers.append("4.0")
        self.answers.append("12")
        self.answers.append("274.3")
        
        self.randomize()

class example_question_mtype(test_question_multiple_choice):
    def randomize(self):
        q_num = random.randint(0, len(self.questions)-1)
        super().SetQuestionText(self.questions[q_num])
        for i in range(len(self.custom_options)):
            super().AddOption(self.custom_options[i])
            super().AddCorrFlag(self.custom_corr_qflags[i][q_num])
        
    def __init__(self):
        super().__init__()
        self.questions = []
        self.custom_option_nums = []
        self.custom_options = []
        self.custom_corr_qflags = []
        
        self.questions.append("Multiple choice: question var. 1")
        self.questions.append("Multiple choice: question var. 2")
        self.questions.append("Multiple choice: question var. 3")
        self.questions.append("Multiple choice: question var. 4")
        
        self.custom_options.append("Answer: correct for question var. 1")
        self.custom_corr_qflags.append([1,0,0,0])
        
        self.custom_options.append("Answer: correct for question var. 2, 3")
        self.custom_corr_qflags.append([0,1,1,0])
        
        self.custom_options.append("Answer: correct for question var. 3, 4")
        self.custom_corr_qflags.append([0,0,0,1])
        
        self.custom_options.append("Answer: correct for question var. 4")
        self.custom_corr_qflags.append([0,0,0,1])
        
        self.randomize()

class example_question_rtype(test_question_radio):
    def randomize(self):
        q_num = random.randint(0, len(self.questions)-1)
        super().SetQuestionText(self.questions[q_num])
        for i in range(len(self.custom_options)):
            super().AddOption(self.custom_options[i])
            super().AddCorrFlag(self.custom_corr_qflags[i][q_num])
        
    def __init__(self):
        super().__init__()
        self.questions = []
        self.custom_option_nums = []
        self.custom_options = []
        self.custom_corr_qflags = []
        
        self.questions.append("Single choice: question var. 1")
        self.questions.append("Single choice: question var. 2")
        self.questions.append("Single choice: question var. 3")
        self.questions.append("Single choice: question var. 4")
        
        self.custom_options.append("Answer: correct for question var. 1")
        self.custom_corr_qflags.append([1,0,0,0])
        
        self.custom_options.append("Answer: correct for question var. 2")
        self.custom_corr_qflags.append([0,1,0,0])
        
        self.custom_options.append("Answer: correct for question var. 3")
        self.custom_corr_qflags.append([0,0,1,0])
        
        self.custom_options.append("Answer: correct for question var. 4")
        self.custom_corr_qflags.append([0,0,0,1])
        
        self.randomize()

class example_test(test_generator):
    def __init__(self, testname_in, printable_testname_in, stud_id_in, stud_name_in):
        super().__init__(testname_in, printable_testname_in, stud_id_in, stud_name_in)
        
        q0 = csd_question_ttype()
        super().add_tq(q0)
        
        q1 = example_question_mtype()
        super().add_tq(q1)
        
        q2 = example_question_rtype()
        super().add_tq(q2)
