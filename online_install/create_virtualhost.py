import os

_VIRTUALHOST_FILE_CONTENT = '''
<VirtualHost *:80>
        DocumentRoot {directory}
        ServerAdmin localhost
        ServerName localhost
        <Directory {directory}>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order allow,deny
                allow from all
        </Directory>
        ErrorLog /var/log/apache2/error.log
        LogLevel warn
        CustomLog /var/log/apache2/access.log combined
        ServerSignature On
</VirtualHost>'''

_APACHE_CONF = '''
<Directory {directory}>
        Options Indexes FollowSymLinks
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


content = _APACHE_CONF.format(directory=path)
print('apache conf:')
print(content)
apache_conf_file = open('apache.conf', 'w')
apache_conf_file.write(content)
apache_conf_file.close()
