import LogicGate.LogicGate.LogicGate as lg
#import LogicGate.LogicGate.lgEncrypt as lgE

if __name__ == '__main__':
  #lgE.encrypt('Datafile', 'key', 'Hello World!')
  #lgE.decrypt('Datafile', 'key')
  lg.compile('main.lgeso', 'Hello World!')
  lg.run('main.lgeso', gate=True)