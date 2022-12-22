def sanitizeName(userName):
    userName = userName.lower().split()
    userName = ''.join(userName)
    return userName
    
def test_sanitizeName():
    assert sanitizeName("ERIN YOO") == "erinyoo"
    assert sanitizeName("Jonathan") == "jonathan"