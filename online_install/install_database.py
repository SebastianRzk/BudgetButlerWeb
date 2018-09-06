
import pymysql.cursors
import getpass
import os


#TABLES to install


_TABLES = {
    'eintraege': '''CREATE TABLE `eintraege` (
      `id` int(11) NOT NULL,
      `person` varchar(20) NOT NULL,
      `name` varchar(40) NOT NULL,
      `kategorie` varchar(20) NOT NULL,
      `wert` varchar(10) NOT NULL,
      `datum` char(10) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;''',

      'gemeinsam_zuordnung':'''CREATE TABLE `gemeinsam_zuordnung`
       ( `ID` INT NOT NULL AUTO_INCREMENT , `SourcePerson` VARCHAR(249) NOT NULL
        , `DestinationPerson` VARCHAR(249) NOT NULL , PRIMARY KEY (`ID`))
         ENGINE = InnoDB;''',

    'kategorien': '''CREATE TABLE `kategorien` (
      `id` int(11) NOT NULL,
      `person` varchar(20) NOT NULL,
      `name` varchar(40) NOT NULL
      ) ENGINE=InnoDB DEFAULT CHARSET=latin1;''',

    'users': '''CREATE TABLE `users` (
      `id` int(10) UNSIGNED NOT NULL,
      `email` varchar(249) COLLATE utf8mb4_unicode_ci NOT NULL,
      `password` varchar(255) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `username` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
      `status` tinyint(2) UNSIGNED NOT NULL DEFAULT '0',
      `verified` tinyint(1) UNSIGNED NOT NULL DEFAULT '0',
      `resettable` tinyint(1) UNSIGNED NOT NULL DEFAULT '1',
      `roles_mask` int(10) UNSIGNED NOT NULL DEFAULT '0',
      `registered` int(10) UNSIGNED NOT NULL,
      `last_login` int(10) UNSIGNED DEFAULT NULL,
      `force_logout` mediumint(7) UNSIGNED NOT NULL DEFAULT '0'
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

    'users_confirmations': '''CREATE TABLE `users_confirmations` (
        `id` int(10) UNSIGNED NOT NULL,
        `user_id` int(10) UNSIGNED NOT NULL,
        `email` varchar(249) COLLATE utf8mb4_unicode_ci NOT NULL,
        `selector` varchar(16) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
        `token` varchar(255) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
        `expires` int(10) UNSIGNED NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

    'users_remembered': '''CREATE TABLE `users_remembered` (
      `id` bigint(20) UNSIGNED NOT NULL,
      `user` int(10) UNSIGNED NOT NULL,
      `selector` varchar(24) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `token` varchar(255) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `expires` int(10) UNSIGNED NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;''',

    'users_throttling': '''CREATE TABLE `users_throttling` (
      `bucket` varchar(44) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `tokens` float UNSIGNED NOT NULL,
      `replenished_at` int(10) UNSIGNED NOT NULL,
      `expires_at` int(10) UNSIGNED NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    ''',

    'users_resets': '''CREATE TABLE `users_resets` (
      `id` bigint(20) UNSIGNED NOT NULL,
      `user` int(10) UNSIGNED NOT NULL,
      `selector` varchar(20) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `token` varchar(255) CHARACTER SET latin1 COLLATE latin1_general_cs NOT NULL,
      `expires` int(10) UNSIGNED NOT NULL
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;'''
}

_INDIZES = {
    'eintraege': '''ALTER TABLE `eintraege` ADD PRIMARY KEY (`id`);''',
    'kategorien': '''ALTER TABLE `kategorien` ADD PRIMARY KEY (`id`);''',
    'users': 'ALTER TABLE `users` ADD PRIMARY KEY (`id`), ADD UNIQUE KEY `email` (`email`);',

    'users_confirmations': '''ALTER TABLE `users_confirmations`
      ADD PRIMARY KEY (`id`),
      ADD UNIQUE KEY `selector` (`selector`),
      ADD KEY `email_expires` (`email`,`expires`),
      ADD KEY `user_id` (`user_id`);''',

    'users_remembered': '''ALTER TABLE `users_remembered`
      ADD PRIMARY KEY (`id`),
      ADD UNIQUE KEY `selector` (`selector`),
      ADD KEY `user` (`user`);''',

    'users_resets': '''ALTER TABLE `users_resets`
      ADD PRIMARY KEY (`id`),
      ADD UNIQUE KEY `selector` (`selector`),
      ADD KEY `user_expires` (`user`,`expires`);''',

    'users_throttling': '''ALTER TABLE `users_throttling`
      ADD PRIMARY KEY (`bucket`),
      ADD KEY `expires_at` (`expires_at`);'''
}


_AUTO_INCREMENT = {
    'eintraege': 'ALTER TABLE `eintraege` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;',

    'kategorien': 'ALTER TABLE `kategorien` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;',

    'users': 'ALTER TABLE `users` MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;',

    'users_confirmations': 'ALTER TABLE `users_confirmations` MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;',

    'users_remembered': 'ALTER TABLE `users_remembered` MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;',

    'users_resets': 'ALTER TABLE `users_resets` MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;'
}

_DATA = {
    'users_confirmations': '''INSERT INTO `users_confirmations` (`id`, `user_id`, `email`, `selector`, `token`, `expires`) VALUES
        (1, 1, 'admin@admin.de', 'UG8hQHpU1LPw2why', '$2y$10$PCHPGfdrYic4FneutCosTuDeOnnUwppG3Fa.afBD/Y1YuZm.MjidC', 1533067604);''',
    'users': '''INSERT INTO `users` (`id`, `email`, `password`, `username`, `status`, `verified`, `resettable`, `roles_mask`, `registered`, `last_login`, `force_logout`) VALUES
        (1, 'admin@admin.de', '$2y$10$KTQSNUgSzuCU3WFOFgMGWulBAjmbPyzt3zbnTqUBWXyhbWbwO5k6q', 'admin', 0, 1, 1, 0, 1532901494, 1533280621, 3);'''
}

def _execute_queries(cursor, sql_dict, already_installed_tables):
    for table_name, query in sql_dict.items():
        if table_name in already_installed_tables:
            print('skipping', table_name, '(already installed)')
            continue
        print('EXECUTING', '{', query, '}')
        cursor.execute(query)

if 'TRAVIS_INTEGRATION' in os.environ:
    host = 'localhost'
    dbname = 'testdb'
    user = 'root'
    passwd = ''
else:
    host = input('DB host: ')
    dbname = input('DB name: ')
    user = input('DB user: ')
    passwd = getpass.getpass('Password for ' + user + ': ')

# Connect to the database
connection = pymysql.connect(host=host,
                             user=user,
                             password=passwd,
                             db=dbname,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print('WRITING DATABASE...')
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s"
        cursor.execute(sql, (dbname))
        result = result = cursor.fetchall()

        installed_tables = set()
        for table in result:
            installed_tables.add(table['TABLE_NAME'])

        print('Already installed tables:')
        print(installed_tables)

        print('INSTALL _TABLES')
        _execute_queries(cursor, _TABLES, installed_tables)

        print('INSTALL _INDIZES')
        _execute_queries(cursor, _INDIZES, installed_tables)

        print('INSTALL _AUTO_INCREMENT')
        _execute_queries(cursor, _AUTO_INCREMENT, installed_tables)

        print('INSTALL _DATA')
        _execute_queries(cursor, _DATA, installed_tables)
        connection.commit()
finally:
    connection.close()

print('WRITING CONFIG...')

config = '''db_name = {dbname}
db_usr = {dbuser}
db_pw ={dbpw}
'''.format(dbname=dbname, dbuser=user, dbpw=passwd)
config_file = open('../online/db.ini', 'w')
config_file.write(config)
config_file.close()

print('DONE :-)')



