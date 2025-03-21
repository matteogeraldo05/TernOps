import accounts

def test_register_user():
    success, account, message = accounts.register_user("testUsername", "testPassword", False, "src\\Test\\test_accountInfo.csv")
    assert success == True
    assert not isinstance(account, accounts.Guest)
    assert message != ""
