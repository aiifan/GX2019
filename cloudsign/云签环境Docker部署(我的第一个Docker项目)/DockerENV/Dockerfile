FROM centos:7

EXPOSE 8003 8004 6379
WORKDIR /usr/lib64
ADD dotnet-sdk-2.2.401-linux-x64.tar.gz /usr/local/dotnet
RUN ln -sf /usr/local/dotnet/dotnet /usr/bin/dotnet \
    && yum install -y epel-release \
    && yum update -y \
    && yum install icu -y \
    && yum install -y redis \
    && yum install -y java \
    && yum install -y libgdiplus-devel \
    && yum install -y mkfontscale \
    && yum install -y fontconfig \
    && yum install -y supervisor \
    && ln -sf libdl-2.17.so libdl.so \
    && echo -e "soft nofile 102400\nhard nofile 102400" >> /etc/security/limits.conf \
    && ulimit -n 102400 \
    && echo -e "fs.inotify.max_user_instances = 102400" >> /etc/sysctl.conf

COPY cloudfonts /usr/share/fonts/cloudfonts/cloudfonts
WORKDIR /usr/share/fonts/cloudfonts
RUN mkfontscale \
    && mkfontdir \
    && fc-cache \
    && ln -sf /usr/share/fonts/cloudfonts /var/fonts
CMD [ "/usr/bin/supervisord", "-c", "/GX/supervisord/supervisord.conf" ]