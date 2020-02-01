# Install virtualenv

$ pip3 install --user virtualenv
  The script virtualenv is installed in '/Users/stockwill/Library/Python/3.7/bin' which is not on PATH.
  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
$ /Users/stockwill/Library/Python/3.7/bin/virtualenv -p python3 venv

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
