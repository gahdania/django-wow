FROM alpine

ENV UIID 5000
ENV GID 5000
ENV HOST_NAME mail.gahd.io
ENV DOMAIN_NAME gahd.io
ENV MAIL_DB_HOST postgres
ENV MAIL_DB_USER postfix
ENV MAIL_DB_PASS testpass
ENV MAIL_DB_NAME postfix
ENV NETWORK 172.17.0.0/16
ENV COUNTRY US
ENV PROVIDENCE_STATE Virginia
ENV LOCALITY Springifeld
ENV ORGINZATION GAHD.IO
ENV SUBJECT "/C=${COUNTRY}/ST=${PROVIDENCE_STATE}/L=${LOCALITY}/O=${ORGINZATION}/CN=${HOST_NAME}"


RUN apk update && \
    apk upgrade && \
    apk add --no-cache postfix postfix-pgsql postfix-pcre clamav clamav-milter clamav-scanner dovecot dovecot-pgsql

RUN mkdir -p /var/mail/domains && \
    chown -R $UIID:$GID /var/mail/domains

RUN deluser vmail && \
    delgroup postdrop

RUN adduser -H -D -u $UIID -s /sbin/nologin vmail && \
    adduser vmail vmail

RUN openssl genpkey -algorithm ED25519 -out /etc/ssl/dovecot/${HOST_NAME}.key && \
    openssl req -new -key /etc/ssl/dovecot/${HOST_NAME}.key -out /etc/ssl/${HOST_NAME}.csr -subj $SUBJECT && \
    openssl x509 -req -days 700 -in /etc/ssl/${HOST_NAME}.csr -signkey /etc/ssl/dovecot/${HOST_NAME}.key -out /etc/ssl/dovecot/${HOST_NAME}.crt

RUN mkdir -p /etc/postfix/sql
ADD postfix/* /etc/postfix/
ADD postfix/sql/* /etc/postfix/sql/
ADD dovecot/* /etc/dovecot/
ADD master.cf /
RUN cat /master.cf >> /etc/postfix/master.cf
RUN rm -f /master.cf

RUN sed -ri -e "s|<UID>|$UIID|g" -e "s|<GID>|$GID|g" -e "s|<HOST_NAME>|$HOST_NAME|g" \
      -e "s|<DOMAIN_NAME>|$DOMAIN_NAME|g" -e "s|<NETWORK>|$NETWORK|g" /etc/postfix/main.cf

RUN for file in `ls -1 /etc/postfix/sql/*`; do \
      sed -ri -e "s|<MAIL_DB_USER>|$MAIL_DB_USER|g" -e "s|<MAIL_DB_PASS>|$MAIL_DB_PASS|g" \
        -e "s|<MAIL_DB_NAME>|$MAIL_DB_NAME|g" -e "s|<MAIL_DB_HOST>|$MAIL_DB_HOST|g" $file; done

RUN sed -ri -e "s|<HOST_NAME>|$HOST_NAME|g" /etc/dovecot/dovecot.conf && \
    for file in dovecot-sql.conf dovecot-dict-quota.conf; do \
      sed -ri -e "s|<MAIL_DB_HOST>|$MAIL_DB_HOST|g" -e "s|<MAIL_DB_USER>|$MAIL_DB_USER|g" \
        -e "s|<MAIL_DB_PASS>|$MAIL_DB_PASS|g" -e "s|<MAIL_DB_NAME>|$MAIL_DB_NAME|g" /etc/dovecot/$file; done && \
    sed -ri -e "s|<UIID>|$UIID|g" -e "s|<GID>|$GID|g" /etc/dovecot/dovecot-sql.conf


RUN chown -R root:root /etc/postfix && \
    chown -R root:root /etc/dovecot && \
    chmod og-rwx /etc/postfix/sql/* && \
    chmod og+rx,og-w,g+s /usr/sbin/postqueue /usr/sbin/postdrop && \
    chgrp vmail /usr/sbin/postqueue /usr/sbin/postdrop /var/spool/postfix/public /var/spool/postfix/maildrop


EXPOSE 25/tcp 465/tcp 587/tcp 993/tcp


ADD ./init/* /etc/init.d/
ADD docker-entrypoint.sh /usr/local/bin/

ENTRYPOINT docker-entrypoint.sh
CMD docker-entrypoint.sh
