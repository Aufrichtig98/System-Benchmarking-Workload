import math
import os
import subprocess
from time import time
from os.path import getsize
from os import mkdir

# Get the size of a file
def get_file_size(path):
    try:
        return getsize(path)
    except:
        print('File not found')
        return ''
print
# A list consisting of lists with the file to execute as the first element
# and N elements as command line arguments


def addCommand(*stringList):
    command = []
    for i in range(len(stringList)):
        command.append(stringList[i])
    return command

def addToExecute(file_and_args):

    directory = os.getcwd();
    directory += '/CompressionCorpus/'

    relativePath = 'CompressionCorpus/'

    for i in range(1,2):

        pathResult = os.getcwd() + '/result/compression/' + str(i)

        for filename in os.scandir(directory):
            file_and_args.append(addCommand('tar', '-cvf' , filename.name + '.tar',  relativePath + filename.name))
            file_and_args.append(addCommand('./brotli', '-' + str(i), filename.name + '.tar'))
            file_and_args.append(addCommand('zip','-' + str(i), '-r',  pathResult + filename.name + 'Compression' + str(i) + '.zip', filename.name))
            file_and_args.append(addCommand('mv',  filename.name + '.tar.br', relativePath  + filename.name + 'Compression' + ".br"))

    return file_and_args

def execute(file_and_args):

    if (file_and_args[0] == 'mv') or (file_and_args[0] == 'tar'):
        process = subprocess.Popen(file_and_args, stdout=subprocess.PIPE)
        # Wait for process to finish
        process.wait()
        return

    start = time()
    process = subprocess.Popen(file_and_args, stdout=subprocess.PIPE)
    # Wait for process to finish

    process.wait()
    end = time() - start



    ts = end * 1000
    log_lines = '[Time measured: {} ms]\n'.format(ts)

    # Example of getting a file size
    #size = getsize('wait.py')
    #log_lines += '[File size: {}B]\n'.format(size)

    log_lines += '[Process return code: {}]\n\n'.format(process.returncode)

    write(log_lines)

def write(text):
    log_file.write(text)

if __name__ == '__main__':
    try:
        os.makedirs('result')
    except FileExistsError:
        pass
    except Exception:
        print('Unknown error while creating result directory')
        quit(42)

    if not(os.path.isdir('result/compression1')):
        for i in range(1, 10):
            os.makedirs('result/compression' + str(i))

    filesToExecute = (addToExecute([]))
    print(filesToExecute)

    for file_and_args_list in filesToExecute:
        compressionLevelTmp = 1
        compressionLevel = math.floor(compressionLevelTmp/4)
        log_file = open('result/compression' + str(compressionLevel) + 'result.txt', 'a+')
        execute(file_and_args_list)
        log_file.close()
        compressionLevelTmp += 1









