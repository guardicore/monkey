from infection_monkey.post_breach.pba import PBA


class FileExecution(PBA):
    def __init__(self, file_path):
        linux_command = "chmod 110 {0} ; {0} ; rm {0}".format(file_path)
        win_command = "{0} & del {0}".format(file_path)
        super(FileExecution, self).__init__("File execution", linux_command, win_command)
