import hashlib

def hashPassword(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

# Funtion to test if the passwords are being converted to correct hashcode or not
def test_hashPassword():
    assert hashPassword("6094") == "556f0ae1769fa6600e874b4c9cc16e74e595f86df457839357328142cd0b5ff5"
    assert hashPassword("This is my password") == "ead57e206cef37881a434be6096347490d144345a05b8f93849ba1a5747a6777"