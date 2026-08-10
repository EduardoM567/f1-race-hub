from auth_consumer import handle_register, handle_login

# Test registration
print(handle_register("testuser@example.com", "MyPassword123"))

# Test duplicate email
print(handle_register("testuser@example.com", "MyPassword123"))
# expect: {'success': False, 'message': 'Email already in use'}

# Test correct login
print(handle_login("testuser@example.com", "MyPassword123"))
# expect: {'success': True, 'message': 'Login successful'}

# Test wrong password
print(handle_login("testuser@example.com", "WrongPassword"))
# expect: {'success': False, 'message': 'Invalid email or password'}

# Test nonexistent email
print(handle_login("nobody@example.com", "whatever"))
# expect: {'success': False, 'message': 'Invalid email or password'}