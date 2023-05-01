from LogicGate import lgEncrypt

def testEncryptDecrypt():
  lgEncrypt.encrypt('testData', 'testKey', 'help me?')
  assert lgEncrypt.decrypt('testData', 'testKey', True) == 'help me?'