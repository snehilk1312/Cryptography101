# generate a private key with the correct length, to be kept secret
openssl genrsa -out private-key.pem 4096

# generate corresponding public key, to be shared i.e public
openssl rsa -in private-key.pem -pubout -out public-key.pem

cat public-key.pem

# optional: create a self-signed certificate
openssl req -new -x509 -key private-key.pem -out cert.pem -days 360

# optional: convert pem to pfx
openssl pkcs12 -export -inkey private-key.pem -in cert.pem -out cert.pfx

openssl rand -base64 32 > key.bin    # to be secret

openssl rsautl -encrypt -inkey public-key.pem -pubin -in key.bin -out key.bin.enc

cat key.bin.enc

openssl rsautl -decrypt -inkey private-key.pem -in key.bin.enc -out key.bin

# Creating a secret file to encrypt
echo "I am Voldemort" > SECRET_FILE

# we can also se without -base64 flag
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -base64 -iter 100000  -salt -in SECRET_FILE -out SECRET_FILE.enc -pass file:./key.bin

cat SECRET_FILE.enc

# if we would have remove -base64 flag in encryption then no need here too
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -base64 -iter 100000 -salt -d -in SECRET_FILE.enc -pass file:./key.bin


