#!/bin/bash

# setup links to .COMPSs and COMPSs_tmp directories
if [ ! -d /root/.COMPSs ]; then
	mkdir /root/.COMPSs
fi

if [ ! -d /root/COMPSs_tmp ]; then
	mkdir /root/COMPSs_tmp
fi

if [ -e /parsoda/.COMPSs ]; then
	rm -rf /parsoda/.COMPSs
fi

if [ -e /parsoda/COMPSs_tmp ]; then
	rm -rf /parsoda/COMPSs_tmp
fi

ln -s /root/.COMPSs /parsoda/.COMPSs
ln -s /root/COMPSS_tmp /parsoda/COMPSs_tmp
ln -s /parsoda /root/parsoda

# run ssh daemon
/sbin/sshd -D
