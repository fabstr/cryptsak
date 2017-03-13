# cryptsak
Simple http api service for encrypting and decrypting stuff. Should probably not be trusted in practice.

As long as the master secret is constant the system is stateless as far as a client can be concerned.

## Dependencies: flask and pycrypt 
    
    $ pip install flask pycrypt

## Configuration
Please change the master secret in Config.py. Update host and port as necessary.

### Nginx configuration
It might be a good idea to redirect all http requests to https:

    server {
        listen      0.0.0.0:80;
        server_name www.example.com example.com;
        return 301  https://$host$request_uri;
    }

Configure the reverse proxy, choose good chipers and enable strict transport security:

    server {
        listen      0.0.0.0:443 ssl;
        server_name www.example.com example.com;

        ssl_certificate /path/to/cert.pem;
        ssl_certificate_key /path/to/key.pem;
        ssl_dhparam /path/to/dharams.pem;
        ssl_ciphers "EECDH+aRSA+AESGCM EECDH+aRSA+SHA384 EECDH+aRSA+SHA256 EECDH !ECDHE+RSA+AES256+SHA !AES128 !SEED !CAMELLIA !RC4 !NULL !LOW !MEDIUM !3DES !MD5 !EXP !PSK !SRP !DSS";

        ssl_protocols TLSv1.2 TLSv1.1 TLSv1;

        ssl_prefer_server_ciphers on;
        ssl_session_cache shared:SSL:50m;
        add_header Strict-Transport-Security "max-age=315569520; includeSubDomains; preload";

        location /cryptsak/ {
                rewrite /cryptsak/(.*) $1 break;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_pass http://127.0.0.1:5000;
        }
    }

Update the ip addresses and ports as necessary. Feel free to change /cryptsak/.

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
Write a client api library which validates the certificate.

## License
MIT
