#!/bin/sh

/usr/bin/newalaises
/etc/init.d/postfix start
/etc/init.d/dovecot start
