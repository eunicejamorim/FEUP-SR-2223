# ransomware

## Encrypt
```shell
sudo sh malware.sh
# At the end of each iteration, the programs outputs: "X files encrypted | Y files not encrypted" will be 
````

### Stop encryption
```shell
ps aux
# Identify the PID of the process
sudo kill $PID
````

## Decrypt
```shell
sudo sh decrypt.sh
# At the end of the decryption, the program outputs: "X files have been decrypted"
```
