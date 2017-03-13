# cryptsak
Simple http api service for encrypting and decrypting stuff. Should probably not be trusted in practice.

## Dependencies: flask and pycrypt 
    
    $ pip install flask pycrypt

## Configuration
Please change the master secret in Config.py. Update host and port as necessary.

## Usage
There are two functions, encrypt and decrypt. Simply POST data to /encrypt and
save the response. To decrypt, POST the response to /decrypt.

### Run the server
Using python3:

    python main.py

Python 2 has not been tested.

### Encrypt
POST /encrypt with raw data with content type multipart/form-data
    
    this is a string to be encrypted

Which might return (for some particular master secret and state of the operating system secure pseudo random generator)

    +AZe95Ortdj93jv93toyJ+phI7m992MyYrg6d7JGG28=;BOJc/IzGS5giv8OvvYihSAMvcq/GvuJPfxL60gNgDK0=;X3A2FCd29YQ/lctBy/OGZA==

### Decrypt
POST /decrypt with raw data with content type multipart/form-data

    +AZe95Ortdj93jv93toyJ+phI7m992MyYrg6d7JGG28=;BOJc/IzGS5giv8OvvYihSAMvcq/GvuJPfxL60gNgDK0=;X3A2FCd29YQ/lctBy/OGZA==

Which (using the same master secret as above) will return 

    this is a string to be encrypted

You can try this out by using the master secret 'very secret string'.

## Future work
Set up a HTTPS server with a self signed certificate and certificate pinning, then write a client api library which validates the certificate.

## License
MIT
