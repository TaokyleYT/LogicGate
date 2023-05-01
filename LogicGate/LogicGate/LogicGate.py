from os.path import exists
from sys import argv
import sys, os
from random import randint
from math import sqrt


def run(
  filename: str,
  gate: bool = False,  #show gate in result
  ascii: bool = True,  #show ascii in result
  debug: bool = False,  #log during process
  check: str = '',  #check for error in code, mostly for debug
  out: bool = True
):
  """To run this filename is the only thing needed, Error will be raised and nothing will return if something went wrong. If ascii is on, it will return the ascii result, otherwise 0.
  
  Arguments, type of input, usecases:
      filename: string, specify which file needed to run
      gate: boolean(True or False), if the result shows gate result or not
      ascii: boolean, if the result converts to ascii and show or not
      debug: boolean, show the unhuman log during the interpute
      check: string, if it is specified then the result will be colored. It compares the difference between the gate result and the binary of check input, only works if both gate and ascii is True 
             (color: green=correct bit
                     red=incorrect bit
                     blue box=missing bit 1
                     purple box=missing bit 0)
      out: boolean, enable for outputs
                     """

  def process(
    obj,  #first command
    line: tuple = (
      0, 0
    ),  #for error reporting, first is line and second is index, sometimes third for the latest gate called
    aft=None,  #command afterward
    an=None,  #None/True/False -> (1/0/Not)/And/Or
  ) -> tuple:  #(0 or 1, unprocessed commands that may be used by and/or gates in previous commands in list)
    'One line code processor, return one output from a line of input, internal use only'
    if debug: print('called, args:', obj, line, aft, an)
    if len(str(obj)) == 1:  #if the first process string is a single command
      obj = str(obj)
      if obj == "#":
        if aft[:2] == '##':
          return
      AnList = None
      if an != None:
        #if AnList exists, it is an and/or gate, depends on the first index is True(and) or False(or)
        AnList = [an]
        if debug: print('AnList init:', AnList)
      if obj == '1':
        if debug: print('1:', aft)
        if AnList:
          AnList.append((1, aft))
        else:
          return (1, aft)
      elif obj == '0':
        if debug: print('0:', aft)
        if AnList:
          AnList.append((0, aft))
        else:
          return (0, aft)
      if aft != None and aft != []:
        if debug: print('gate sector for', obj)
        if obj == 'N':
          proc = process(aft[0], line=(line[0], line[1] + 1, 'N'), aft=aft[1:])
          if debug: print('not:', proc)
          if AnList:
            AnList.append((0 if proc[0] else 1, proc[1]))
          else:
            return (0 if proc[0] else 1, proc[1])
        elif obj == 'A':
          proc = process(aft[0],
                         line=(line[0], line[1] + 1, 'A'),
                         aft=aft[1:],
                         an=True)
          if debug: print('and:', proc)
          if AnList:
            AnList.append(proc)
          else:
            return tuple(proc)
        elif obj == 'O':
          proc = process(aft[0],
                         line=(line[0], line[1] + 1, 'O'),
                         aft=aft[1:],
                         an=False)
          if debug: print('or:', proc)
          if AnList:
            AnList.append(proc)
          else:
            return tuple(proc)
      if AnList != None:
        if debug: print('And/Or gate:', AnList)
        try:
          if AnList[1][1] == None:
            raise IndexError()
          AnList.append(
            process(
              AnList[1][1][0],
              line=(line[0], line[1] + 1, 'A' if AnList[0] else 'O'),
              aft=None if len(str(AnList[1][1])) == 1 else AnList[1][1][1:]))
        except IndexError:
          sys.tracebacklimit = 0
          sys.stdout = sys.__stdout__
          raise SyntaxError(
            f'gate {line[2] if obj=="0" or obj=="1" else obj} in line {line[0]} index {line[1]-1} requires {"1" if (line[2] if obj=="0" or obj=="1" else obj)=="N" else "2"} inputs, 1 received'
          )
        if len(AnList) == 3:
          if AnList[0]:
            return (AnList[1][0] and AnList[2][0], AnList[2][1])
          else:
            return (AnList[1][0] or AnList[2][0], AnList[2][1])
      else:
        #and/or gate syntax error
        sys.tracebacklimit = 0
        sys.stdout = sys.__stdout__
        raise SyntaxError(
          f'gate {line[2] if obj=="0" or obj=="1" else obj} in line {line[0]} index {line[1]} requires {"1" if (line[2] if obj=="0" or obj=="1" else obj).upper()=="N" else "2"} inputs, 0 received'
        )
    else:
      #if the first command given is not one command
      sys.stdout = sys.__stdout__
      raise SystemError(
        'Internal error, unexpected arguments received in internal helper function, please do not change the code'
      )

  
  if out:
    sys.stdout = sys.__stdout__
  else:
    sys.stdout = open(os.devnull, 'w')
  if exists(filename):
    with open(filename, 'r') as f:
      f.seek(0,0)
      Out = [[]]
      dt = f.readlines()
      if filename[-6:] != '.lgeso':
        sys.tracebacklimit = 0
        sys.stdout = sys.__stdout__
        raise NameError(
          f'{filename} is not an lgeso file, maybe renaming the file extension to lgeso and try again')
      for dtidx, line in enumerate(dt):
        line = line.replace('\n', '')
        if '---' in line:
          Out.append([])
        else:
          try:
            Out[-1].append(
            str(
              process(line[0],
                      line=(dtidx + 1, 1),
                      aft=(None if len(line) == 1 else line[1:]))[0]))
          except OverflowError:
            sys.tracebacklimit = 0
            sys.stdout = sys.__stdout__
            raise OverflowError(f'too many commands in line {dtidx+1}, more than max command on this os ({sys.getrecursionlimit()} commands per line), process overflowed, exited')
      hold = ""
      checkOut = ""
      checkhold = []
      if check:
        for char in check:
          checkhold.append(str(bin(ord(char))[2:]))
      if gate:
        print('gates result:')
      for nidx, n in enumerate(Out):
        checkOut+='-'
        Nhold = n.copy()
        if n == []:
          continue
        if gate:
          for chekidx, chek in enumerate(n):
            if '\033[0;37;41m' in chek and '\033[0;37;40m' in chek:
              continue
            if chek != '1' and chek != '0' and chek != ' ':
              print(
                f'error char {repr(chek)} found in index {chekidx}, line {nidx+1}, please report that line of code shown in lgeso file to the dev. '
              )
            if ascii and check:
              if nidx >= len(checkhold):
                n[chekidx] = f'\033[0;37;41m{chek}\033[0;37;40m'
                checkOut+=chek
              else:
                if len(n) > len(checkhold[nidx]):
                  for _ in range(len(n)-len(checkhold[nidx])):
                    checkhold[nidx] = '0' + checkhold[nidx]
                if chek != checkhold[nidx][chekidx]:
                  n[chekidx] = f'\033[0;37;41m{chek}\033[0;37;40m'
                  checkOut+=chek
                else:
                  n[chekidx] = f'\033[0;37;42m{chek}\033[0;37;40m'
          if nidx < len(checkhold):
            if len(n) < len(checkhold[nidx]):
              for x in checkhold[nidx][len(n):]:
                n.append(f'\033[0;37;{"46" if int(x) else "45"}m▯\033[0;37;40m')
                checkOut+='0' if int(x) else '1'
          n.append(' ')
          print(''.join(n))
        if ascii:
          try:
            hold += chr(int(''.join(Nhold), 2))
          except ValueError:
            print(
              f'unacceptable ascii result received, ascii code: {"".join(Nhold), 2}'
            )
      if ascii:
        print("\nAscii converted result:\n" + hold)
        if gate and check:
          print('\nExpected result:\n' + check)
      sys.stdout = sys.__stdout__
      return checkOut if (check and gate and ascii) else hold if ascii else 0
  else:
    sys.tracebacklimit = 0
    sys.stdout = sys.__stdout__
    raise FileNotFoundError(
      f'{filename} is not an existing file from given path, prehaps try moving the file to the same directory as this program?'
    )


def compile(
  filename: str = 'main.lgeso',
  output: str = 'Hello World!',
  randomize: bool = True,
  random_range: list = [1, 5],
  write:bool = True,
  override:bool = False,
  BitLock:int = -1
) -> None:  #I swear if this thing returns anything somehow somewhere and somewhat, python is dying or my brain is dying
  """compile string to lgeso file, random_range is needed only when randomize is true.
  filename: string, specify which file to write the data into, new file named as filename will be created if it doesn't exist
  output: string, specify what result will be produced
  randomize: boolean, if the data written is pure binary or further encrypted with gates
  random_range: list, the maximum set of gates in the written data will be the square of the second item while the minimum will be the square of the first item.
  write: boolean, if the result is returned or is written to file
  override: boolean, safety checks are off, proceed with caution
  BitLock: integer, if the binary of a character is shorter than this value, 0 will be appended. Defalt is -1, which is off, all negative number will be counted as ignore as well"""

  out = ""
  override = not override
  if not output and override:
    output = 'Hello World!'
  if filename and write and override:
    if len(filename) > 6:
      if filename[-6:] != '.lgeso':
        print(f'filename is not an lgeso file, filename changed to {filename}')
        filename += '.lgeso'
    elif '.' in filename:
      print(f'filename is not an lgeso file, filename changed to {filename}')
      filename += '.lgeso'
    else:
      print(f'filename is not an lgeso file, filename changed to {filename}')
      filename = 'main.lgeso'
  else:
    if override:
      print(f'filename is not an lgeso file, filename changed to {filename}')
      filename = 'main.lgeso'
  with open(filename, 'w') as f:
    if (len(random_range) != 2 or random_range[0] > random_range[1]) and override:
      print('invalid random range received, changed to 1-5')
      random_range = [1, 5]  #when the random_range is not correctly formatted
    for checkidx, check in enumerate(random_range):
      try:
        random_range[checkidx] == int(check)  #if the input is a number or not
      except ValueError:
        if override:
          print('invalid random range received, changed to 1-5')
          random_range = [1, 5]
          break
      else:
        if (check < 1 or check > (sqrt(sys.getrecursionlimit())//3)) and override:  #avoid overflow error when running
          print(
            'an item in random range is too large or too small, changed to 1-5'
          )
          random_range = [1, 5]
          break
    for char in output:
      line = str(bin(ord(char))[2:])
      if len(line) < BitLock and BitLock >= 0:
        for _ in range(BitLock-len(line)):
          line = '0'+line
      for char in line:
        if randomize:
          charGoal = int(char)  #the ideal final output after the randomizing
          for _ in range(
              randint(random_range[0], random_range[1]) *
              randint(random_range[0], random_range[1])):
            gates = randint(0, 3)
            if gates == 1:
              char = ('N0' if char == '1' else 'N1' if char == '0' else
                      ('NN' + char))
            elif gates == 2:
              buff = ('1' if randint(0, 1) else '0') if charGoal else '0'
              char = 'O' + (char + buff if randint(0, 1) else buff + char)
            elif gates == 3:
              buff = '1' if charGoal else ('1' if randint(0, 1) else '0')
              char = 'A' + (char + buff if randint(0, 1) else buff + char)
        if write:
          f.write(char + '\n')
        else:
          out += char
      if write:
        f.write('---\n')
      else:
        out += "-"
    print(
      f'compilation completed and result {"written in" if write else "returned"} {filename if write else ""} with output as {output}\nrandomizaion is {"on" if randomize else "off"}\n\n\n'
    )
    return None if write else out


if __name__ == '__main__':
  exit(run((str(argv[1]) if len(argv) != 1 else 'main.lgeso')))
