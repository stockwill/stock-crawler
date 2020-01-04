

# Fix Python Execution Error

```
pip install -r requirements.txt
make: *** [install] Abort trap: 6
```

[](https://github.com/paramiko/paramiko/issues/1538)

```
ln -s /usr/local/Cellar/openssl@1.1/1.1.1d/lib/libcrypto.dylib /usr/local/lib/libcrypto.dylib\n
ln -s /usr/local/Cellar/openssl@1.1/1.1.1d/lib/libssl.dylib /usr/local/lib/libssl.dylib\n
```
