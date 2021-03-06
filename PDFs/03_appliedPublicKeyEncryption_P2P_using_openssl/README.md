## Generating Assymetric Key for encrypting symmetric key

### Private Key


```bash
# generate a private key with the correct length, to be kept secret
openssl genrsa -out private-key.pem 4096
```

    Generating RSA private key, 4096 bit long modulus (2 primes)
    .........................................................................................................................................................................++++
    ................................................................................................................................................................++++
    e is 65537 (0x010001)


### Public Key


```bash
# generate corresponding public key, to be shared i.e public
openssl rsa -in private-key.pem -pubout -out public-key.pem
```

    writing RSA key



```bash
cat public-key.pem
```

    -----BEGIN PUBLIC KEY-----
    MIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAqJ2w3PKI1uMXhb3V/dcY
    zNS3Mrdz+T6d37qglNTZWvkU6AZbGJNBV5clOCPpvuOHggs3eErMyf2jr5Ar7m5l
    Z36wSN1aFSZxuwJcUqTt+WiasygOyu8azuuCCxK8v7rTVqVCF3Lz39/d6KJFgycT
    z4yQ4sSRQxjA+crU6Yi4aZy3zaKTEEhv23PXVq8EhcNrGepkR6KI7zo1uVf2omO7
    sz3kcsEnuKmzu/Ced0mrDow5wfTzoqCrI80Iia8iFOnroS5QLU+6zTlB3kLT1cJd
    yxH1FKHVPkfsZMvR61JuaHfXPvUpeDAaEj2l3dWYHhkmpUcGSeblGmA2maJnuDZx
    O8PgzlM3KFY0dEYCW4UzdYLafyJGg/+D8kEzBDqmjg0Fq1HHxcp7rRpLJuSHo6vs
    Czx/oqs22S3gLTF8UG0WC5HyiyReAFyTJ0/zNAAq3Tj+eUtTuJ9TmBBBmPrjXYBj
    YOL9cYZUlxEEPYd1e59rmvkFUts46XLwWjHX/ILpDmcO/Yw7S//ghTuk/fg9+dH0
    8OcI1iLFGOuV1lzPzPYER4GVBbFH+alLsySpGxZM5w0ZkyL8kfdKh/dEMKWQxk6d
    srJT3AQjYkVfQ4FeOJk/ST3sqe00rybFL5hCbmDwTVqBo7pXYk1DUMEYWhy7QsAG
    Z5NBehI+lyYgEKcsLMMcl9kCAwEAAQ==
    -----END PUBLIC KEY-----


### create a self-signed certificate

##### Now that you have a private key, you can use it to generate a self-signed certificate. This is not required, but it allows you to use the key for server/client authentication, or gain X509 specific functionality in technologies such as JWT and SAML. 


```bash
# optional: create a self-signed certificate
openssl req -new -x509 -key private-key.pem -out cert.pem -days 360
```

    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [AU]:



```bash
# optional: convert pem to pfx
openssl pkcs12 -export -inkey private-key.pem -in cert.pem -out cert.pfx
```

    Enter Export Password:
    Can't read Password


## Generating Symmetric key to encrypt our message or file


```bash
openssl rand -base64 32 > key.bin    # to be secret
```

### now we will send this symmetric key "key.bin" to the person , encrypting with his public key(let's say the public key we created in above section is his, i.e he send us)


```bash
openssl rsautl -encrypt -inkey public-key.pem -pubin -in key.bin -out key.bin.enc
```


```bash
cat key.bin.enc
```

    lx^�z� ?Q䚹k�[[U`�bu����֔���E.[c��3�����M{�����W��z�_]��J�@��Q&���L<�f��G7iyS�kJş�'â�Ib�F��
    �!���/R�~\��5Q	Q���f(7M��W��z�E,�"�U[UJ�s+X謁#�N��*}S\8�]�)�b^��� ��pɝ0餼��Jer���g ��9���!�<�^�m�l�ԛ�D���j����h�׺@qX����J�[Ӑ�k+ʦ3؉Q�#�R���-���y���O��nT;��+qcJ�
    O� 5�e������G`5>�x�̎}ya�$o�YS�N �����5�BiC�-����8{l,�����xv��SӭU%�m�O
    �DJe��
    �>��]�3w����"��^�ܟ�`��Œ}	B�

##### so the file key.bin.enc is the encrypted format of our file key.bin , when this file is sent over an unsecure channel like email , the receiver whose public key we have used to encrypt our symmetric key can use his private_key like as follows to get the secret symmetric key :)

## Decrypting Symmetric Key(receiver does with their private key)


```bash
openssl rsautl -decrypt -inkey private-key.pem -in key.bin.enc -out key.bin
```

##### Now the receiver has the symmetric key, we can encrypt a msg using this symmetric key and he can open the same coz he has same symmetric key

## Actually Encrypt our large file


```bash
# Creating a secret file to encrypt
echo "I am Voldemort" > SECRET_FILE
```


```bash
# we can also se without -base64 flag
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -base64 -iter 100000  -salt -in SECRET_FILE -out SECRET_FILE.enc -pass file:./key.bin
```


```bash
cat SECRET_FILE.enc
```

    U2FsdGVkX1/MLfV34Pq3k61zx7OK8nkUkgT31OLrZdU=


## Decrypt the large file  , to be done by other person


```bash
# if we would have remove -base64 flag in encryption then no need here too
openssl enc -aes-256-cbc -md sha512 -pbkdf2 -base64 -iter 100000 -salt -d -in SECRET_FILE.enc -pass file:./key.bin
```

    I am Voldemort


##### references:
https://web.archive.org/web/20210217025411/https://www.czeskis.com/random/openssl-encrypt-file.html

https://www.scottbrady91.com/OpenSSL/Creating-RSA-Keys-using-OpenSSL

https://askubuntu.com/questions/1093591/how-should-i-change-encryption-according-to-warning-deprecated-key-derivat


```bash

```
