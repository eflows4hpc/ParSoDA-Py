#!/bin/bash

# setup links to .COMPSs and COMPSs_tmp directories
if [ ! -d /root/.COMPSs ]; then
	mkdir /root/.COMPSs
fi

if [ -e /parsoda/.COMPSs ]; then
	rm -rf /parsoda/.COMPSs
fi

ln -s /root/.COMPSs /parsoda/.COMPSs
ln -s /parsoda /root/parsoda

# run ssh daemon
/sbin/sshd -D
