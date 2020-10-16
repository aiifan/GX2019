import paramiko

# Create your views here.


def connect_ssh(ipaddr, user, password, port=22):
    
    sshclient = paramiko.SSHClient()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshclient.connect(ipaddr, port, user, password,timeout=10)
    stdin,stdout,stderr = sshclient.exec_command("uname")
    try:
        if stdout.channel.recv_exit_status() != 0:
            return stderr.read().decode('utf8')
        else:
            return stdout.read().decode('utf8')
    finally:
        sshclient.close()

# connect_ssh("192.168.0.169", 'root', '123456')


import hashlib
def getPassword(password):
    sha = hashlib.sha3_512()
    #实例化md5加密方法
    sha.update(password.encode())
    #进行加密，python2可以给字符串加密，python3只能给字节加密
    result = sha.hexdigest()
    return result

a = getPassword("123456")

print(a)