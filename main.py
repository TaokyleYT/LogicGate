import LogicGate.LogicGate.LogicGate as lg
import LogicGate.LogicGate.lgEncrypt as lgE

if __name__ == '__main__':
  #lgE.encrypt('a.lgeso', 'b.lgeso', 'Hello World!')
  lgE.decrypt('a.lgeso', 'b.lgeso')
  #lg.compile('main.lgeso', 'Hello World!')
  #lg.run('main.lgeso', gate=True)