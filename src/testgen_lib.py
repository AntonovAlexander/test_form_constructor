# -*- coding:utf-8 -*-

#
# test_generator.py
#
#  Created on: 01.04.2024
#      Author: Alexander Antonov <antonov.alex.alex@gmail.com>
#     License: See LICENSE file for details
#

from __future__ import division

import struct
import serial
import os
import random

class test_generator:
    
    def __init__(self, testname_in, printable_testname_in, stud_id_in, stud_name_in):
        self.printable_testname = printable_testname_in
        self.stud_id = stud_id_in
        self.stud_name = stud_name_in
        self.form_filename = testname_in + ".html"
        self.ref_filename = testname_in + ".csv"
        self.test_questions = []
        self.test_questions_counter = 0
    
    def add_tq(self, new_test_question):
        self.test_questions_counter += 1
        new_test_question.SetQuestionCounter(self.test_questions_counter)
        self.test_questions.append(new_test_question)
    
    def writeForm(self, path):
        with open(path + "/" + self.stud_id + "_" + self.form_filename, "w") as file:
            file.write("<!DOCTYPE html>\n")
            file.write("<html>\n")
            file.write("\n")
            
            file.write("<head>\n");
            file.write("\t<title>" + self.printable_testname + "</title>\n")
            file.write("\t<script src=\"FileSaver.js\"></script>\n")
            file.write("</head>\n")
            file.write("\n")
            
            file.write("<body>\n")
            file.write("\n")
            
            file.write("<h1>" + self.printable_testname + "</h1>\n")
            file.write("<h3>ID: " + self.stud_id + "</h3>\n")
            file.write("<h3>Name: " + self.stud_name + "</h3>\n")
            file.write("\n")
        
            for tq in self.test_questions:
                tq.write_question_html(file)
            file.write("\n")
            
            file.write("<script>\n")
            file.write("function CreateTextFile() {\n")
            
            file.write("var ans = new Blob([\"\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("\n")
            
            for tq in self.test_questions:
                tq.write_csvdownloader_js(file)
            file.write("\n")
            file.write("saveAs(ans, \"" + self.stud_id + "_submitted.csv\");\n")
            file.write("\n")
            
            file.write("}\n")
            file.write("</script>\n")
            file.write("<p></p>")
            file.write("<button type = \"button\" onclick = \"CreateTextFile();\">Generate answers CSV file</button>\n")
            file.write("\n")
            
            file.write("</body>\n")
            file.write("\n")
            file.write("</html>\n");
    
    def writeReference(self, path):
        with open(path + "/" + self.stud_id + "_" + self.ref_filename, "w") as file:
            for tq in self.test_questions:
                tq.write_ref_csv(file)
    
    def writeFiles(self, path):
        try:
            os.makedirs(path + "/forms")
        except:
            print("Warning: directory " + path + " already exists")
        self.writeForm(path + "/forms")
        try:
            os.makedirs(path + "/refs")
        except:
            print("Warning: directory " + path + "/refs" + " already exists")
        self.writeReference(path + "/refs")
        

class test_question:
    def __init__(self):
        self.questionLines = []
        self.test_question_num = 0
    
    def SetQuestionText(self,  new_question):
        self.questionLines = []
        self.questionLines.append(new_question)
    
    def AddQuestionTextLine(self,  new_textline):
        self.questionLines.append(new_textline)
    
    def SetQuestionCounter(self, num):
        self.test_question_num = num
    
    def write_question_html(self, file):
        file.write("test question!")

    def GetQuestionLines(self):
        return self.questionLines
    
    def GetQuestion(self):
        ret_question = ""
        for questionLine in self.questionLines:
            ret_question += (" " + questionLine)
        return ret_question
    
    def GetTQNum(self):
        return self.test_question_num

class test_question_text(test_question):
    def __init__(self):
        super().__init__()
    
    def SetCorrAnswerText(self, corr_ans_text_in):
        self.corr_ans_text = corr_ans_text_in
    
    def write_question_html(self, file):
        file.write("<p>Question " + str(super().GetTQNum()) + ": ")
        for q_textline in super().GetQuestionLines():
            file.write("<br>" + q_textline)
        file.write("</p>\n")
        file.write("<form>\n")
        file.write("<input type=\"text\" id=\"a" + str(super().GetTQNum()) + "\">")
        file.write("</form>\n")
    
    def write_csvdownloader_js(self, file):
        file.write("ans = new Blob([ans, \"" + str(super().GetTQNum()) + "\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("ans = new Blob([ans, \";t;\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("ans = new Blob([ans, \"" + str(super().GetQuestion()) + "\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("ans = new Blob([ans, \";\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("ans = new Blob([ans, document.getElementById('a" + str(super().GetTQNum()) + "').value], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("ans = new Blob([ans, \"\\n\"], {type: \"text/plain;charset=utf-8\"});\n")
    
    def write_ref_csv(self, file):
        file.write(str(super().GetTQNum()) + ";t;" + str(super().GetQuestion()) + ";" + self.corr_ans_text + "\n")
        

class test_question_multiple_choice(test_question):
    def __init__(self):
        super().__init__()
        self.options = []
        self.corr_flags = []
    
    def SetOptions(self,  new_options):
        self.options = new_options
        
    def AddOption(self,  new_options):
        self.options.append(new_options)
    
    def SetCorrFlags(self, new_corr_flags):
        self.corr_flags = new_corr_flags
    
    def AddCorrFlag(self, new_corr_flags):
        self.corr_flags.append(new_corr_flags)
    
    def write_question_html(self, file):
        file.write("<p>Question " + str(super().GetTQNum()) + ": ")
        for q_textline in super().GetQuestionLines():
            file.write("<br>" + q_textline)
        file.write("</p>\n")
        file.write("<form>\n")
        for option in self.options:
            file.write("<input type=\"checkbox\" id=\"a" + str(super().GetTQNum()) +  "_" + str(self.options.index(option)) + "\" name=\"a" + str(super().GetTQNum()) + "\" value=\"HTML\">\n")
            file.write("<label for=\"a1_0\">" + option + "</label><br>\n")
        file.write("</form>\n")
    
    def write_csvdownloader_js(self, file):
        for option in self.options:
            file.write("ans = new Blob([ans, \"" + str(super().GetTQNum()) + "\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \";m;\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \"" + option + "\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \";\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("if(document.getElementById('a" + str(super().GetTQNum()) + "_" + str(self.options.index(option)) + "').checked) {\n")
            file.write("\tans = new Blob([ans, \"1\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("} else {\n")
            file.write("\tans = new Blob([ans, \"0\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("}\n")
            file.write("ans = new Blob([ans, \"\\n\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("\n")
    
    def write_ref_csv(self, file):
        for option in self.options:
            file.write(str(super().GetTQNum()) + ";m;" + option + ";" + str(self.corr_flags[self.options.index(option)]) + "\n")

class test_question_radio(test_question):
    def __init__(self):
        super().__init__()
        self.options = []
        self.corr_flags = []
    
    def SetOptions(self,  new_options):
        self.options = new_options
        
    def AddOption(self,  new_options):
        self.options.append(new_options)
    
    def SetCorrFlags(self, new_corr_flags):
        self.corr_flags = new_corr_flags
    
    def AddCorrFlag(self, new_corr_flags):
        self.corr_flags.append(new_corr_flags)
    
    def write_question_html(self, file):
        file.write("<p>Question " + str(super().GetTQNum()) + ": ")
        for q_textline in super().GetQuestionLines():
            file.write("<br>" + q_textline)
        file.write("</p>\n")
        file.write("<form>\n")
        for option in self.options:
            file.write("<input type=\"radio\" id=\"a" + str(super().GetTQNum()) +  "_" + str(self.options.index(option)) + "\" name=\"a" + str(super().GetTQNum()) + "\" value=\"HTML\">\n")
            file.write("<label for=\"a1_0\">" + option + "</label><br>\n")
        file.write("</form>\n")
    
    def write_csvdownloader_js(self, file):
        for option in self.options:
            file.write("ans = new Blob([ans, \"" + str(super().GetTQNum()) + "\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \";r;\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \"" + option + "\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("ans = new Blob([ans, \";\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("if(document.getElementById('a" + str(super().GetTQNum()) + "_" + str(self.options.index(option)) + "').checked) {\n")
            file.write("\tans = new Blob([ans, \"1\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("} else {\n")
            file.write("\tans = new Blob([ans, \"0\"], {type: \"text/plain;charset=utf-8\"});\n")
            file.write("}\n")
            file.write("ans = new Blob([ans, \"\\n\"], {type: \"text/plain;charset=utf-8\"});\n")
        file.write("\n")
    
    def write_ref_csv(self, file):
        for option in self.options:
            file.write(str(super().GetTQNum()) + ";r;" + option + ";" + str(self.corr_flags[self.options.index(option)]) + "\n")
