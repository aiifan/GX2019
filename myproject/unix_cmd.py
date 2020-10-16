
import subprocess
def unix_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    p.wait()
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode,stderr
    return p.returncode,stdout

print unix_command("sh /root/test.sh")