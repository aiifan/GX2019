#!/bin/bash
#encoding:utf-8
#适用于centos6 32位 09型密码卡

MIMAKA_DIR=/lib/swcsmdrv
MIMAKA_LIBSWSDS=libswsds.so.2.5.6.0

chmod +x ./*

if [ ! -d $MIMAKA_DIR ]; then
    mkdir $MIMAKA_DIR
else    
    ${MIMAKA_DIR}/unload  || ./unload 
    rm -rf ${MIMAKA_DIR}
    mkdir $MIMAKA_DIR
fi
cp swcsm09.ko loaddrv unload ${MIMAKA_LIBSWSDS} ${MIMAKA_DIR}
ln -sf ${MIMAKA_DIR}/${MIMAKA_LIBSWSDS} /usr/lib/libswsds.so
${MIMAKA_DIR}/loaddrv

grep -w 'cd /lib/swcsmdrv/ && ./loaddrv' /etc/rc.d/rc.local >/dev/null
if test $? -ne 0
then
   echo 'cd /lib/swcsmdrv/ && ./loaddrv'>>/etc/rc.d/rc.local
fi
chmod +x /etc/rc.d/rc.local

echo "succeed"
