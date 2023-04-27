from LogicGate import __version__, LogicGate
from random import randint



def testCompileDecompile():
  LogicGate.compile('test', 'hello there', randomize=(True if randint(0, 1) else False))
  assert LogicGate.run('test.lgeso',
                       gate=True,
                       ascii=True,
                       check="hello there") == ""
