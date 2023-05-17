import LogicGate.LogicGate.LogicGate as lg
import LogicGate.LogicGate.lgEncrypt as lgE

if __name__ == '__main__':
  lgE.encrypt('Datafile', 'key', 'Hello World!\n\n')
  lg.compile('main.lgeso', 'Hello World!')
  print('\n'*5)
  lgE.decrypt('Datafile', 'key')
  lg.run('main.lgeso', gate=True)