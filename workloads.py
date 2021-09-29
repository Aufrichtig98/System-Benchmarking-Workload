import math
import os
import subprocess
from time import time
from os.path import getsize
from os import mkdir

# Get the size of a file


def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def get_file_size(path):
    try:
        return getsize(path)
    except:
        print('File not found')
        return ''

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


    for i in range(1,10):

        pathResult = os.getcwd() + '/result/compression' + str(i) + '/'

        for filename in os.scandir(directory):
            file_and_args.append(addCommand('tar', '-cvf' , filename.name + '.tar',  relativePath + filename.name))
            file_and_args.append(addCommand('./brotli','-j', '-' + str(i), filename.name + '.tar'))
            file_and_args.append(addCommand('zip','-' + str(i), '-r',  pathResult + 'zip/' + filename.name + 'Compression' + '.zip',relativePath + filename.name))
            file_and_args.append(addCommand('mv',  filename.name + '.tar.br', pathResult  +'brotli/'+ filename.name + 'Compression' + ".br"))

    return file_and_args

def execute(file_and_args):

    if (file_and_args[0] == 'mv') or (file_and_args[0] == 'tar'):
        process = subprocess.Popen(file_and_args, stdout=subprocess.PIPE)
        # Wait for process to finish
        process.wait()
        return

    nameType = ''
    timeMeasurements = 0
    if file_and_args[0] == './brotli':
        nameType = file_and_args[3][:len(file_and_args[3]) - 3]
        for i in range(30):
            command = []
            if i == 29:
                command = addCommand(file_and_args[0],file_and_args[1], file_and_args[2], file_and_args[3])
                timeStart = time()
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                process.wait()
                timeEnd = (time() - timeStart) * 1000

            else:
                command = addCommand(file_and_args[0], file_and_args[2], file_and_args[3])
                timeStart = time()
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                process.wait()
                timeEnd = (time() - timeStart) * 1000
                fileName = file_and_args[3] + '.br'
                command = addCommand('rm', fileName)
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                process.wait()
            timeMeasurements += timeEnd
    else:
        nameType = file_and_args[3][:len(file_and_args[3]) - 4]
        for i in range(30):
            command = addCommand(file_and_args[0], file_and_args[1], file_and_args[2], file_and_args[3], file_and_args[4])
            timeStart = time()
            process = subprocess.Popen(command, stdout=subprocess.PIPE)
            process.wait()
            timeEnd = (time() - timeStart) * 1000
            if i != 29:
                command = addCommand('rm',file_and_args[3] )
                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                process.wait()

        timeMeasurements += timeEnd

    log_lines = '[Time measured SUM up: {} ms]\n'.format(timeMeasurements)
    log_lines += '[Time measured Mean: {} ms]\n'.format(timeMeasurements/30)

    # Example of getting a file size
    #size = getsize('wait.py')
    #log_lines += '[File size: {}B]\n'.format(size)

    log_lines += '[Process return code ' + nameType  + ': {}]\n\n'.format(process.returncode)


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
            os.makedirs('result/compression'+ str(i) + '/brotli')
            os.makedirs('result/compression'+ str(i) + '/zip')

    filesToExecute = (addToExecute([]))

    compressionLevelTmp = 0
    compressionLevel = 1
    for file_and_args_list in filesToExecute:
        #20 workloads * 4 commands per file per compression level
        if compressionLevelTmp == 80:
            compressionLevelTmp = 0
            compressionLevel += 1

        if 'brotli' in file_and_args_list[0]:
            log_file = open('result/compression' + str(compressionLevel) +'/brotliComp' + str(compressionLevel) + 'result.txt', 'a+')
        else:
            log_file = open('result/compression' + str(compressionLevel) + '/zipComp' + str(compressionLevel) + 'result.txt','a+')
        execute(file_and_args_list)
        log_file.close()
        compressionLevelTmp += 1
        tmp = 1

    tmp = 0
    for folder in os.scandir(os.getcwd() + '/result/'):
        tmp += 1

        log_file = open(os.getcwd() + '/result/' + 'compression' + str(tmp) + '/' + 'sizes.txt', 'a+')

        for item in os.scandir(os.getcwd() + '/result/' + 'compression' + str(tmp) + '/'):

            if item.name == 'brotli':
                sizeBrotli = get_size(
                    start_path=(os.getcwd() + '/result/' + 'compression' + str(tmp) + '/' + item.name))
                log_lines_write = '[Size Brotli : {} bytes]\n'.format(sizeBrotli)
                write(log_lines_write)

            if item.name == 'zip':
                sizeZip = get_size(
                    start_path=(os.getcwd() + '/result/' + 'compression' + str(tmp) + '/' + item.name))
                log_lines_write = '[Size ZIP : {} bytes]\n'.format(sizeZip)
                write(log_lines_write)

        log_file.close()




