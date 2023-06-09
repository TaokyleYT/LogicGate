from os.path import exists
from os import remove
from sys import getrecursionlimit as maxcur
from math import sqrt
from random import randint
try:
  exec(
    f'import {"LogicGate" if (__name__=="__main__") else "".join(str(__name__).rsplit("".join((__file__.split("/")[-1]).rsplit(".py", 1)), 1))+"LogicGate"} as lg'
  )
except ModuleNotFoundError:
  raise ImportError('module require LogicGate, LogicGate not found')
except ImportError:
  raise ImportError('module require LogicGate, LogicGate not found')


def encrypt(filename: str = "main.lgeso",
            key_file: str = "key.lgeso",
            msg: str = "Hello World!",
            output : bool = True):
  """
  an encryption module with the help of LogicGate main module, LogicGate.py is needed.
  Note: this encryption method is not safe, anyone with the data of the 2 files will be able to see the information. 
  filename: string, file to write the encrypted code to
  key_file: string, file to keep the key string into
  msg: string, word to encrypt
  output: boolean, whether outputs are present or not
  """

  if not msg.isascii():
    raise ValueError(
      f'message received ({repr(msg)}) is not available in ascii')
  k, f, kOut, fOut = [''] * 4
  data = []
  chekK = []
  chekF = []
  for char in msg:
    data.append(str(bin(ord(char))[2:]))
  for i in data:
    k = ''
    f = ''
    if len(i) < 7:
      i = '0' * (7 - len(i)) + i
    for idx, char in enumerate(i):
      while randint(0, 1) == randint(0, 1):
        rand = randint(0, 1)
        k += str(rand)
        f += str(rand)
      k += '0' if int(char) else '1'
      f += str(char)
    while char := randint(0, 1) == randint(0, 1):
      k += str(int(char))
      f += str(int(char))
    if len(k) % 7 != 0 or len(f) % 7 != 0:
      k = '0' * (7 - (len(k) % 7)) + k
      f = '0' * (7 - (len(f) % 7)) + f
    tempK = []
    tempF = []
    for kIdx in range(0, len(k), 7):
      tempK.append(k[kIdx:kIdx + 7])
    for fIdx in range(0, len(f), 7):
      tempF.append(f[fIdx:fIdx + 7])
    if len(tempF) != len(tempK):
      raise SystemError(
        "length of passes doesn't match, internal error raised")
    chekF.append(''.join(tempF))
    chekK.append(''.join(tempK))
    for ko in tempK:
      kOut += chr(int(str(''.join(ko)), 2))
    for fo in tempF:
      fOut += chr(int(str(''.join(fo)), 2))
  checkBuf = []
  check = []
  for fChek, kChek in zip(chekF, chekK):
    for objF, objK in zip(fChek, kChek):
      if objK != objF:
        checkBuf.append(objF)
  for chek in range(0, len(checkBuf), 7):
    check.append(checkBuf[chek:chek + 7])
  for n in range(0, len(data) - 1):
    if str(data[n]) != ''.join(check[n]) and output:

      print('BitWarning: bit unaligned\ndata bit : compile bit\n' +
            str(data[n]) + ' : ' + ''.join(check[n]) + '\n')
  lg.compile(filename,
             fOut,
             random_range=(10, sqrt(maxcur()) // 3),
             output=output,
             override=True,
             BitLock=7)
  lg.compile(key_file,
             kOut,
             random_range=(10, sqrt(maxcur()) // 3),
             output=output,
             override=True,
             BitLock=7)


def decrypt(filename: str, key_file: str, sause: bool = False, debug: bool = False, debug_ALL: bool = False):
  """basic decryption, filename and keyfile is required.
  If sause is True, no output will be give pn out but result returned, normally used for another module's extra encryption
  If debug is on, all hidden outout will be outputted.
  If debug_ALL is on, every single coded output sentense except warning or error will be outputted, this will create a massive lag and do not recommend

  NOTE: file __decrypt__.lgeso and will be used for temperary data store and bypasser for LogicGate.decompile lgeso file locker.
  THE FILE WILL BE CLEARED, WRITTEN AND DELETED AFTER USING THIS FUNCTON"""
  if exists(filename) and exists(key_file):
    with open(filename, 'r') as f, open(key_file, 'r') as k:
      dk = open('__decrypt__.lgeso', 'w')
      Fdt = f.read()
      Kdt = k.read()
      dk.write(Kdt)
      dk.close()
      CheckStr = lg.decompile('__decrypt__.lgeso', ascii=True, debug=debug_ALL, out=debug)
      df = open('__decrypt__.lgeso', 'w')
      df.write(Fdt)
      df.close()
      out = lg.decompile('__decrypt__.lgeso',
                   ascii=True,
                   gate=True,
                   check=CheckStr,
                   debug=debug_ALL,
                   out=debug).split('-')
      do = open('__decrypt__.lgeso', 'w')
      out = ''.join(out)
      outP = []
      for O in range(0, len(out), 7):
        outP.append(out[O:O + 7])
      for n in outP:
        do.write("\n".join(n))
        do.write("\n---\n")
      do.close()
      out = lg.decompile('__decrypt__.lgeso', gate=True, debug=debug_ALL, out=(debug or not sause))
      remove('__decrypt__.lgeso')
      return out
  else:
    print("filename or key_file doesn't exist, exiting")


if __name__ == '__main__':
  f = 'encFile'
  k = 'encKey'
  encrypt(f, k, 'Hello World!')
  decrypt(f, k)
