import os
import glob
#import binascii
import zlib

def main():
    ret_arr = obtainValues()
    editFile(ret_arr)
    return 0

def obtainValues():
    files = glob.glob("build/*.elf", recursive=True)
    size = 0
    crcValue = 0
    for file in files:
        size = size + os.path.getsize(file)
        crcValue = crcValue + int(crc(file), 16)

    number = 15

    ret_arr = [ size, crcValue, number ]

    return ret_arr

# def CRC32_from_file(filename):
#     buf = open(filename,'rb').read()
#     buf = (binascii.crc32(buf) & 0xFFFFFFFF)
#     return "%08X" % buf

def crc(fileName):
    prev = 0
    for eachLine in open(fileName,"rb"):
        prev = zlib.crc32(eachLine, prev)
    return "%X"%(prev & 0xFFFFFFFF)

def editFile(ret_arr):

    file_path = './dummyConfig - Kopya.ini'

    fp = open(file_path, 'r')
    lines = fp.readlines()
    fp.close

    lines[4] = ("EntryPoint = " + str(ret_arr[2]) + '\n')
    lines[5] = ("fileSize = " + str(ret_arr[0]) + '\n')
    lines[6] = ("crcValue = " + str(ret_arr[1]) + '\n')

    fp = open(file_path, 'w')

    for line in lines:
        fp.write(line)
    fp.close()

if __name__ == "__main__":
    main()

# for line in fileinput.FileInput(file_path, inplace=1):
#     if 'fileSize' in line:
#         line = line.rstrip()
#         line = line.replace(line, line+'9999')
#         print(line)
#   print(line)
    #sys.stdout.write(line)

# fp_r = open(file_path, 'r+')
# fp_w = open(file_path, 'w')
# last_pos = fp_r.tell()
# inline_pos = 0
# line = fp_r.readline()
# while line != '':
#     if 'fileSize' in line:
#         fp_r.seek(last_pos)
#         fp_r.write()
#         # inline_pos = last_pos
#         # while fp_r.read(1) != '=':
#         #     inline_pos = inline_pos+1
#         # fp_w.seek(inline_pos + 1)
#         # fp_w.write('CHANGED')
#         # while fp.write('') != r'\r\n':
#         #     inline_pos = inline_pos+1
#         # fp.write(' CHANGED')
#         break
#     last_pos = fp_r.tell()
#     line = fp_r.readline()
# fp_r.close()