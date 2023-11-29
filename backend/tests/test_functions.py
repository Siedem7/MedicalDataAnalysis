import unittest

from src.app import *


class tests(unittest.TestCase):

    # test if method is hashing password correctly
    def test_hash_password(self):
        password = "password"
        hashed_password = hashlib.sha512(password.encode("utf-8")).hexdigest()
        self.assertEqual(hash_password(password), hashed_password, "Wrong hashing!")

    # test if method returns true if email is correct
    def test_validate_email(self):
        correct_email = "kamil123@wp.pl"
        wrong_email = "marek326.com"
        self.assertTrue(validate_email(correct_email), "This string is email!")
        self.assertFalse(validate_email(wrong_email), "This string is not email!")

    def test_generate_token(self):
        test_user_id = 1
        result = generate_token(test_user_id)
        self.assertEqual(1, get_id_from_token(result), "Token was generated incorrectly")

    # test if method get id correctly from generated token
    def test_get_id_from_token(self):
        test_user_id = 1
        test_expired_token = jwt.encode({
            'exp': datetime.utcnow() - timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': test_user_id
        }, 'some key', algorithm='HS256')
        test_correct_token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': test_user_id
        }, 'some key', algorithm='HS256')

        self.assertEqual('Signature expired. Please log in again.', get_id_from_token(test_expired_token),
                         "Function returned wrong value!")
        self.assertEqual(1, get_id_from_token(test_correct_token), "Function returned wrong user_id!")

    # test if method correctly authorize
    def test_authorize(self, app):
        test_correct_token = generate_token(1)
        test_no_user_token = generate_token(20)

        with app.app_context():
            try:
                user = db.session.execute(db.select(User).filter_by(id=1)).scalar_one()
                # self.assertEqual((401, user),authorize(test_correct_token),"Something went wrong")
                # self.assertEqual((401, 'No user with provided token.'),authorize(test_no_user_token),"Something went wrong")
            except NoResultFound:
                return
        test_incorrect_token = "some token"
        self.assertEqual((401, 'Invalid token.'), authorize(test_incorrect_token), "Token was invalid")

    # test if method correctly authorize permissions
    def test_authorize_permissions(self, app):
        test_incorrect_token = generate_token(10)
        permission = ["permission"]
        self.assertEqual((401, 'Invalid token.'), authorize_permissions(test_incorrect_token, permission),
                         "Wrong return")

        test_correct_token = generate_token(1)
        status, result = authorize(test_correct_token)
        # self.assertEqual((403, 'No permission to access this feature.'),authorize_permissions(test_correct_token,permission),"Wrong return")
        correct_permission = ["CREATE_USER_ACCOUNT"]
        # self.assertEqual((status,result),authorize_permissions(test_correct_token,correct_permission),"Wrong return")


suite = unittest.TestLoader().loadTestsFromTestCase(tests)
unittest.TextTestRunner(verbosity=2).run(suite)
