class Binance_code():
    def __init__(self, key, secret, url = None):
        self.key = key
        self.secret = secret
        self.url = url

class Autenthicator():
    def __init__(self, code, email = None):
        self.code = code
        self.email = email
    
testnet = Binance_code("a6867c4e2375806b92424ef51400bcd9678193bdb900b19cedda39e7cb0f25d8", "9e41110e12bdc9c27226f5b2106d19e4b894ff4692399f31c54cff96a93132e6", "https://testnet.binancefuture.com")
original = Binance_code("kQoSH9X67dI3Ia2Lf4gIwgnfHXCr1yMA3ufccLUOTLTS48eVr8hLkZuUIYOgjDxd", "lW8oxIvwMdZAbSQ4mXLa57xUOozgmse0lCrztgrof0MRwyGvg8XBRo4vr4I7u72M", "https://api.binance.com")

#Backup Key Autenthicator
binance_backup_autenthicator = Autenthicator("Z2PNATEDFTPNOXM7","alfonsus92@gmail.com")
