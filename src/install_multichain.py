import os
import errno
import wget
import tarfile


download_multichainAPI = "\tmp"

try:
    os.makedirs(download_multichainAPI)
except OSError as exc: 
    if exc.errno == errno.EEXIST and os.path.isdir(download_multichainAPI):
        pass
os.chdir(download_multichainAPI)

multichain_url = 'http://www.multichain.com/download/multichain-1.0-alpha-21.tar.gz'
multichain_file = wget.download(multichain_url)

subprocess.Popen(['tar', '-xvzf', multichain_file, ''])

multichain_file1 = "multichain-1.0-alpha-21"
os.chdir(multichain_file1)

subprocess.call(["sudo","mv", "multichaind", "multichain-cli"])
subprocess.call(["sudo","mv", "multichain-util", "/usr/local/bin"])


