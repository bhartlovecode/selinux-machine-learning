import bcrypt

# Generate a hash password
password = 'password123'
bytes = password.encode('utf-8')
salt = bcrypt.gensalt()
hash = bcrypt.hashpw(bytes, salt)
print(hash)