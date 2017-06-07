#！ -*-coding:utf-8-*-
import sqlite3
import sys,time 
from subprocess  import  Popen
from robot.result import ExecutionResult
import config 
reload(sys)
sys.setdefaultencoding("utf-8")

env_for_test ='syf1.1.1'
testsuite = 'timepointe'
subsuite = 'performance'
try:
     
     file_name = config.ui_suites_dir +'\\'+env_for_test+'\\'+str(testsuite)+'\\'
     test_name = str(subsuite) + '.txt'


     command_line = "pybot %s" % test_name
     process = Popen(command_line , shell=True, cwd= file_name )
     retcode = process.wait()
     # 只拿结果中suite来用
     result= ExecutionResult(file_name+"output.xml").statistics
     totalcase = result .total.all.failed + result .total.all.passed
     passedcase = result .total.all.passed
     failedcase = result .total.all.failed
     print totalcase , passedcase , failedcase
except Exception,e:  
          print  e, "不存在该路径"
     
#将执行结果存入数据库中
#连接数据库
connection = sqlite3.connect(config.db_dir)
cursor = connection.cursor()

#事先将数据库中老的数据删除
del_sql= "delete from TestSuite where projectname='" + str(env_for_test)+ "' and testsuitename='" + str(testsuite)+ "'and subsuite='" + str(subsuite)+ "'"
print  del_sql
cursor.execute(del_sql)
insert_sql = "insert into TestSuitevalues('" + str(env_for_test) + "'," + "'" + str(testsuite) + "'," + "'" + str(subsuite) + "'," + "'"++"',"+"