def sanitizeName(userName):
    userName = userName.lower().split()
    userName = ''.join(userName)
    return userName
    
    # Function to check if the names are being converted to the required format or not
def test_sanitizeName():
    assert sanitizeName("ERIN YOO") == "erinyoo"
    assert sanitizeName("Jonathan") == "jonathan"