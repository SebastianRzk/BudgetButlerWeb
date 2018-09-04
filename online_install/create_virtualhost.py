import os

_VIRTUALHOST_FILE_CONTENT = '''
<VirtualHost *:80>
        DocumentRoot /var/www/budgetbutler/
        ServerAdmin localhost
        ServerName localhost
        <Directory /var/www/budgetbutler/>
                Options Indexes FollowSymLinks MultiViews ExecCGI
                AllowOverride None
                Order allow,deny
                allow from all
        </Directory>
        # Wire up Apache to use Travis CI's php-fpm.
        <IfModule mod_fastcgi.c>
           AddHandler php5-fcgi .php
           Action php5-fcgi /php5-fcgi
           Alias /php5-fcgi /usr/lib/cgi-bin/php5-fcgi
           FastCgiExternalServer /usr/lib/cgi-bin/php5-fcgi -host 127.0.0.1:9000 -pass-header Authorization
           <Directory /usr/lib/cgi-bin>
              Require all granted
           </Directory>
        </IfModule>

        ErrorLog /var/log/apache2/error.log
        LogLevel warn
        CustomLog /var/log/apache2/access.log combined
        ServerSignature On
</VirtualHost>'''

_APACHE_CONF = '''
<Directory {directory}>
        Options Indexes FollowSymLinks ExecCGI
        AllowOverride None
        Require all granted
</Directory>'''



if 'TRAVIS_BUILD_DIR' in os.environ:
    path = os.environ['TRAVIS_BUILD_DIR']
else:
    path = input('Please enter path of online project: ')

path = path + '/online/'
content = _VIRTUALHOST_FILE_CONTENT.format(directory=path)
print('content:')
print(content)


virtualhost_file = open('budget.online.conf', 'w')
virtualhost_file.write(content)
virtualhost_file.close()

return 0

content = _APACHE_CONF.format(directory=path)
print('apache conf:')
print(content)
apache_conf_file = open('apache.conf', 'w')
apache_conf_file.write(content)
apache_conf_file.close()
