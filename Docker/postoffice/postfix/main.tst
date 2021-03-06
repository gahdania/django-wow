
setgid_group = 
myhostname = 
mydomain = 
mydestination = localhost.$mydomain, localhost, $mydomain
mynetworks_style = subnet
mynetworks = 127.0.0.0/8, 

virtual_mailbox_domains = proxy:pgsql:/etc/postfix/sql/pgsql_virtual_domains_maps.cf
virtual_alias_maps = proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_maps.cf,
       proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_maps.cf,
       proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_catchall_maps.cf

virtual_mailbox_maps = proxy:pgsql:/etc/postfix/sql/pgsql_virtual_mailbox_maps.cf,
       proxy:pgsql:/etc/postfix/sql/pgsql_virtual_alias_domain_mailbox_maps.cf

virtual_mailbox_base = /var/mail/domains/
virtual_gid_maps = static:
virtual_uid_maps = static:1001
virtual_minimum_uid = 100
virtual_transport = dovecot
dovecot_destination_recipient_limit = 1

mailbox_transport = virtual
local_transport = virtual

smtpd_helo_required = yes
disable_vrfy_command = yes
message_size_limit = 10240000
queue_minfree = 51200000

smtpd_sender_restrictions =
       permit_mynetworks,
       reject_non_fqdn_sender,
       reject_unknown_sender_domain

smtpd_recipient_restrictions =
       reject_non_fqdn_recipient,
       reject_unknown_recipient_domain,
       permit_mynetworks,
       permit_sasl_authenticated,
       reject_unauth_destination,
       reject_rbl_client dnsbl.sorbs.net,
       reject_rbl_client zen.spamhaus.org,
       reject_rbl_client bl.spamcop.net

smtpd_data_restrictions = reject_unauth_pipelining
smtpd_tls_auth_only = yes
content_filter = scan:[127.0.0.1]:10025
smtpd_tls_cert_file = /etc/ssl/.crt
smtpd_tls_key_file = /etc/private/.key
smtpd_tls_CAfile = /etc/lighttpd/ca-crt.pem
smtpd_tls_security_level = may
smtpd_tls_received_header = yes
smtpd_tls_loglevel = 1

smtpd_sasl_type = dovecot
smtpd_sasl_path = private/dovecot-auth.sock
smtpd_sasl_auth_enable = yes
smtpd_sasl_authenticated_header = yes
broken_sasl_auth_clients = yes
smtpd_tls_auth_only = yes
