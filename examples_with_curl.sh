# for use with spnego (e. g. kerberos), encrypt stuff
curl --negotiate -u :  -X POST --data-binary @- "https://example.com/encrypt"

# for use with spnego (e. g. kerberos), decrypt stuff
curl --negotiate -u :  -X POST --data-binary @- "https://example.com/decrypt"

# unauthenticated version, encrypt
# curl -X POST --data-binary @- "https://example.com/encrypt"

# unauthenticated version, decrypt
# curl -X POST --data-binary @- "https://example.com/decrypt"
