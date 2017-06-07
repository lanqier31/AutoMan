# -*- coding:utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import config
from subprocess import Popen,PIPE

file_name = 'd:\projects\gitRepository\AutoMan\Web\ui_suites\syf1.1.1\病理评估\suite01_派生测试A.txt'
test_name= 'suite01_派生测试A' + '.txt'
#print  file_name

command_line = "pybot  %s" %file_name
print  command_line
p1 = Popen ('cd', shell= True )
process =Popen('pybot  test.txt', shell=True, cwd='D:\\')
retcode = process.wait()

print  'patent process'
print config.ui_suites_dir

