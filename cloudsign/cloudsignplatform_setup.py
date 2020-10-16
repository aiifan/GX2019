#!/usr/bin/python
# encoding:utf-8
# 云签章无网络一键部署脚本,仅适用于centos7.6.1810 minimal(aliyun 25-Nov-2018 21:25)版本。
from __future__ import print_function
import os
import shutil
import zipfile
import tarfile
import subprocess

# 解压zip文件

def un_zip(zipfile_dir, unzip_file_dir):
    shutil.rmtree(os.path.join(unzip_file_dir, (zipfile_dir.split("/")[-1]).split(".")[-2]), ignore_errors=True)
    fx = zipfile.ZipFile(zipfile_dir, "r", zipfile.ZIP_DEFLATED)
    fx.extractall(unzip_file_dir)

#解压tar.gz文件
def un_tar(tar_name, get_tar_dir):
    shutil.rmtree(get_tar_dir, ignore_errors=True)
    os.makedirs(get_tar_dir)
    tar_file = tarfile.open(tar_name)
    tar_file.extractall(get_tar_dir)

#关闭selinux
def disable_selinux(selinux_config):
    python_shell("setenforce=0")
    file_data = ""
    with open(selinux_config) as f:
        old_selinux = "SELINUX=enforcing"
        new_selinx = "SELINUX=disabled"
        for line in f.readlines():
            if old_selinux not in line:
                pass
            else:
                line = line.replace(old_selinux, new_selinx)
            file_data += line
    with open(selinux_config, "w") as f:
        f.write(file_data)

# 追加一行文件内容
def add_one_file(file_path, add_content):
    with open(file_path, "a+") as f:
        f.seek(0)
        if add_content in f.readlines():
            pass
        else:
            f.write(add_content)

# 修改文件内容
def mod_file(filename, file_content):
    with open(filename, "w+") as f:
        f.write(file_content)

# 追加多行文件内容
def add_two_file(file_path, add_content, compare_content):
    with open(file_path, "a+") as f:
        f.seek(0)
        if compare_content in f.readlines():
            pass
        else:
            f.write(add_content)

# 执行shell操作
def python_shell(commod, pathname="/"):
    # subprocess.call(commod, shell=True, cwd=pathname)
    p = subprocess.Popen(commod, shell=True, cwd=pathname, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        return p.returncode, stderr
    return p.returncode, stdout

# 配置supervisord
def supervisord_config(supervisord_config_file, supervisord_config_content):
    if os.access(supervisord_config_file, os.F_OK):
        pass
    else:
        with open(supervisord_config_file, "w+") as f:
            f.write(supervisord_config_content)

# 新建文件夹
def new_folder(folder_name):
    shutil.rmtree(folder_name, ignore_errors=True)
    os.makedirs(folder_name)

# 创建软连接
def ln_sf(source, link_name):
    if os.access(link_name, os.F_OK):
        os.remove(link_name)
    else:
        pass
    os.symlink(source, link_name)

# 提示语
def explain(hint):
    print(hint)

def main():
    # 配置云签章所需环境：asp supervisord redis
    explain("Setup has started. Please wait")
    un_zip("./rpm.zip", "./rpm")
    explain("Dependent package decompression complete")
    python_shell("sudo yum install -y rpm/*", "./")
    shutil.rmtree("./rpm", ignore_errors=True)
    explain("Dependency package installation complete")
    python_shell("ln -sf libdl-2.*.so libdl.so", "/usr/lib64")
    explain("libgdiplus-devel accomplish")
    un_tar("dotnet-sdk-2.2.401-linux-x64.tar.gz", "/usr/local/dotnet")
    ln_sf("/usr/local/dotnet/dotnet", "/usr/bin/dotnet")
    explain("asp Environment configuration completed")
    un_tar("jdk-8u221-linux-x64.tar.gz", "/usr/local/java")
    java_export = """export JAVA_HOME=/usr/local/java/jdk1.8.0_221
export JAVA_BIN=$JAVA_HOME/bin
export JAVA_LIB=$JAVA_HOME/lib
export CLASSPATH=.:$JAVA_LIB/tools.jar:$JAVA_LIB/dt.jar
export PATH=$JAVA_BIN:$PATH
    """
    add_two_file("/etc/profile", java_export, "export JAVA_HOME=/usr/local/java/jdk1.8.0_221\n")
    python_shell("source /etc/profile")
    ln_sf("/usr/local/java/jdk1.8.0_221/bin/java", "/usr/bin/java")
    explain("JAVA Environment configuration completed")
    python_shell("systemctl restart redis && systemctl enable redis")
    explain("Redis is started")
    # 字体
    new_folder("/usr/share/fonts/cloudfonts")
    un_zip("cloudfonts.zip", "/usr/share/fonts/cloudfonts/")
    python_shell("mkfontscale", "/usr/share/fonts/cloudfonts")
    python_shell("mkfontdir", "/usr/share/fonts/cloudfonts")
    python_shell("fc-cache", "/usr/share/fonts/cloudfonts")
    ln_sf("/usr/share/fonts/cloudfonts", "/var/fonts")
    explain("cloudfonts Configuration is successful")
    # 配置supervisord
    new_folder("/var/log/GXCloudSignPlatform")
    supervisord_cloudsignpathform="""[program:CloudSignPlatForm]
command=dotnet CloudSignPlatform.dll
directory=/GX/CloudSignPlatform/ ; 命令执行的目录
autorestart=true ; 程序意外退出是否自动重启
stderr_logfile=/var/log/GXCloudSignPlatform/CloudSignPlatform.err.log ; 错误日志文件
stdout_logfile=/var/log/GXCloudSignPlatform/CloudSignPlatform.out.log ; 输出日志文件
environment=ASPNETCORE_ENVIRONMENT=Development ; 进程环境变量
user=root ; 进程执行的用户身份
stopsignal=INT
    """
    supervisord_asposewebservice="""[program:AsposeWebService]
command=/usr/local/java/jdk1.8.0_221/bin/java -jar /GX/CloudSignPlatform/AsposeWebService_fat.jar
directory=/GX/CloudSignPlatform/ ; 命令执行的目录
autorestart=true ; 程序意外退出是否自动重启
stderr_logfile=/var/log/GXCloudSignPlatform/AsposeWebService.err.log ; 错误日志文件
stdout_logfile=/var/log/GXCloudSignPlatform/AsposeWebService.out.log ; 输出日志文件
user=root ; 进程执行的用户身份
stopsignal=INT
    """
    supervisord_GMSeal="""[program:GMSeal]
command=dotnet SealManagement.dll ; 运行程序的命令
directory=/GX/GMSeal ; 命令执行的目录
autorestart=true ; 程序意外退出是否自动重启
stderr_logfile=/var/log/GXCloudSignPlatform/GMSeal.err.log ; 错误日志文件
stdout_logfile=/var/log/GXCloudSignPlatform/GMSeal.out.log ; 输出日志文件
environment=ASPNETCORE_ENVIRONMENT=Production ; 进程环境变量
user=root ; 进程执行的用户身份
stopsignal=INT
    """
    supervisord_config("/etc/supervisord.d/CloudSignPlatform.ini", supervisord_cloudsignpathform)
    supervisord_config("/etc/supervisord.d/AsposeWebService.ini", supervisord_asposewebservice)
    supervisord_config("/etc/supervisord.d/GMSeal.ini", supervisord_GMSeal)
    explain("supervisord The configuration file has been written")
    # 修改优化系统参数
    python_shell("ulimit -n 102400")
    add_two_file("/etc/security/limits.conf", "soft nofile 102400\nhard nofile 102400\n", "soft nofile 102400\n")
    add_one_file("/etc/sysctl.conf", "fs.inotify.max_user_instances = 102400\n")
    mod_file("/proc/sys/fs/inotify/max_user_instances", "102400")
    explain("System optimization completed")
    # 拷贝云签包
    new_folder("/GX")
    un_zip("CloudSignPlatform.zip", "/GX")
    un_zip("GMSeal.zip", "/GX")
    # 启动云签服务
    disable_selinux("/etc/selinux/config")
    python_shell("firewall-cmd --zone=public --add-port=8003/tcp --permanent")
    python_shell("firewall-cmd --zone=public --add-port=8004/tcp --permanent")
    python_shell("systemctl restart firewalld")
    python_shell("systemctl restart supervisord && systemctl enable supervisord")
    explain("cloudsignpathform deployment is complete")

if __name__ == "__main__":
    main()
