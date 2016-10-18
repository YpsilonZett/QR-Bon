import MySQLdb

from _misc import Misc


class UserHandler(object):
    """
    Class with functions for user management. Has SQL interface.
    Note: No exception handling in this class.
    """

    def __init__(self):
        self.__CURSOR, self.__CONNECTION = self.__db_connect()

    def __db_connect(self):
        """
        Connects to the database.
        :return: (tuple): ((obj) database cursor, (obj) database connection)
        """

        conn = MySQLdb.connect(host="localhost",
                               user="root",
                               passwd="Alay22xmp",
                               db="qrbon")
        c = conn.cursor()
        return c, conn

    def new_user(self, email, username, password):
        """
        Creates a new user in the database
        :param email: (string) email address, typed into register form
        :param username: (string) username, typed into register form
        :param password: (string) password, typed into register form
        :return: (bool) True, if success or False, if user exists
        """

        status_code = self.__CURSOR.execute(
            "SELECT * FROM users WHERE username = ('{usr_name}')".
            format(usr_name=MySQLdb.escape_string(username))
        )
        if int(status_code) > 0:  # Means, that SQL has found an user with this name
            return False

        self.__CURSOR.execute(
            "INSERT INTO users (username, password, email) VALUES ('{name}', '{pwd}', '{email}')".
            format(name=MySQLdb.escape_string(username),
                   pwd=MySQLdb.escape_string(password),
                   email=MySQLdb.escape_string(email))
        )
        self.__CONNECTION.commit()
        return True

    def check_login(self, username, password):
        """
        Checks, whether the given password is the real user password.
        :param username: (str) name of the user
        :param password: (str) given password to check
        :return: (bool) True, if login is ok, False, if not
        """

        self.__CURSOR.execute(
            "SELECT password FROM users WHERE username = ('{usr_name}')".
            format(usr_name=MySQLdb.escape_string(username))
        )
        real_password = self.__CURSOR.fetchone()

        if real_password is not None:
            if real_password[0] == password:
                return True

        return False

    def __get_user_id(self, username):
        """
        Gets the unique foreignkey for a user from the database
        :param username: (str) name of the user
        :return: (int) primary key of the user
        """

        self.__CURSOR.execute(
            "SELECT uid FROM users WHERE username = ('{user_name}')".
            format(user_name=MySQLdb.escape_string(username))
        )
        return int(self.__CURSOR.fetchone()[0])

    def receipt_to_db(self, receipt):
        """
        Puts a receipt with random generated id in the database, note: isn't assigned to user yet
        :param receipt: (str) string version of dictionary
        :return: (str) 16-digit id
        """

        rand_id = Misc.generate_rid()
        self.__CURSOR.execute(
            "INSERT INTO receipts (receipt, receipt_id) VALUES ('{r}', '{rid}')"
            .format(r=MySQLdb.escape_string(receipt), rid=MySQLdb.escape_string(rand_id))
        )
        self.__CONNECTION.commit()
        return rand_id

    def assign_rid_user(self, rid, username):
        """
        Assigns a receipt id (from an existing receipt in the database) to an owner
        :return: (bool) True, if anything ok, else raise error
        """
        user_id = self.__get_user_id(username)
        self.__CURSOR.execute(
            "UPDATE receipts SET user_id={uid} WHERE receipt_id='{rid}'".
            format(uid=user_id, rid=rid)
        )
        self.__CONNECTION.commit()
        return True

    def receipt_overview(self, username):
        """
        Gets all receipts for the dashboard
        :param username: (str) name of the users who gets the overview
        :return: (list) raw receipt data. Needs to be formatted in the html file
        """

        self.__CURSOR.execute(
            "SELECT receipt FROM receipts WHERE user_id = ({uid})".
            format(uid=self.__get_user_id(username))
        )
        return self.__CURSOR.fetchall()
