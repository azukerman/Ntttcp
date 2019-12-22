UTF = "utf-8"
class Cmd_executor_result:
    stdout=None
    stderr=None
    returncode=None
    result_outputs=[]


    def __init__(self,stdout,stderr,returncode,command=None):
        self.stdout=stdout
        self.stderr = stderr
        self.returncode = returncode
        self.command =command
        
    def get_command(self):
        return self.command
    def get_returncode(self):
        return self.returncode

    def get_stderr(self):
        return self.stderr

    def get_stdout(self):
        return (self.stdout)
    def get_outputs(self):
        return self.result_outputs
    def __str__(self):

       return str(self.getResultInDict())
    
    def set_result_output(self,result_outputs):
        self.result_outputs = result_outputs

    def getResultInDict(self):
        result = {}
        result["stdout"] = self.stdout
        result["stderr"] = self.stderr
        result["returncode"] = self.returncode
        if self.command is not None:
            result["command"] = self.command
        return result




