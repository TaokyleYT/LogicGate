from os.path import exists
from os import remove
from sys import getrecursionlimit as maxcur
from math import sqrt
from random import randint
try:
  exec(f'import {"LogicGate" if (__name__=="__main__") else "".join(str(__name__).rsplit("".join((__file__.split("/")[-1]).rsplit(".py", 1)), 1))+"LogicGate"} as lg')
except ModuleNotFoundError:
  raise ImportError('lgEncrypt module require LogicGate, LogicGate not found')
except ImportError:
  raise ImportError('lgEncrypt module require LogicGate, LogicGate not found')


  
def encrypt(filename:str = "main.lgeso", key_file:str = "key.lgeso", msg:str = "Hello World!"):
  """
  an encryption module with the help of LogicGate main module, LogicGate.py is needed.
  filename: string, file to write the encrypted code to
  key_file: string, file to keep the key string into
  msg: string, word to encrypt
  """

  k, f, kOut, fOut = ['']*4
  data = []
  for char in msg:
    data.append(str(bin(ord(char))[2:]))
  for i in data:
    k = ''
    f = ''
    if len(i) < 7:
      i = '0'*(7-len(i)) + i
    for idx, char in enumerate(i):
      while randint(0, 1)==randint(0, 1):
        k += str(char)
        f += str(char)
      k += '0' if int(char) else '1'
      f += str(char)
    while char:=randint(0, 1)==randint(0, 1):
      k += str(int(char))
      f += str(int(char))
    if len(k)%7 != 0 or len(f)%7 != 0:
      k = '0'*(7-(len(k)%7)) + k
      f = '0'*(7-(len(f)%7)) + f
    tempK = []
    tempF = []
    for Kidx, Kobj in enumerate(k):
      if Kidx%7==0:
        tempK.append([])
      tempK[-1] += str(Kobj)
    for Fidx, Fobj in enumerate(f):
      if Fidx%7==0:
        tempF.append([])
      tempF[-1] += str(Fobj)
    if len(tempF) != len(tempK):
      raise SystemError("length of passes doesn't match, internal error raised")
    else:
      pass
    for ko in tempK:
      kOut += chr(int(str(''.join(ko)), 2))
    for fo in tempF:
      fOut += chr(int(str(''.join(fo)), 2))
  lg.compile(filename, fOut, random_range=(10, sqrt(maxcur())//3), override=True)
  lg.compile(key_file, kOut, random_range=(10, sqrt(maxcur())//3), override=True)
        


def decrypt(filename:str, key_file:str, sause:bool=False):
  "basic decryption, filename and keyfile is required, and if sause is True, no printing will happen but result given"
  if exists(filename) and exists(key_file):
    with open(filename, 'r') as f, open(key_file, 'r') as k, open('__decrypt__.lgeso', 'w') as df, open('__decrypt2__.lgeso', 'w') as dk, open('__decrypt3__.lgeso', 'w') as do:
      Fdt = f.read()
      Kdt = k.read()
      df.write(Fdt)
      dk.write(Kdt)
      out = lg.run('__decrypt__.lgeso', gate=True, check=(DEB:=lg.run('__decrypt2__.lgeso', ascii=True, out=True)), out=True).split('-')
      print(repr(out), repr(DEB))
      out = ''.join(out)
      outP = []
      for Oidx, O in enumerate(out):
        if Oidx%7 == 0:
          outP.append([])
        outP[-1] += str(int(O))
      for n in outP:
        do.write("\n".join(n))
        do.write("\n---\n")
      print('\n\n\n')
      uh = lg.run('__decrypt3__.lgeso', gate=True, out=not sause)
      #remove('__decrypt__.lgeso')
      #remove('__decrypt2__.lgeso')
      #remove('__decrypt3__.lgeso')
      return uh
  else:
    print("filename or key_file doesn't exist, exiting")


if __name__ == '__main__':
  f = 'encFile'
  k = 'encKey'
  encrypt(f, k, 'Hello World!')
  decrypt(f, k)