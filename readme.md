# For running clone the repo, add address, token ,and then run docker-compose up
## add address and token to environment in docker-compose.yml file (LINK for Link token, and MATIC for Matic Token)
### this will make a request to get the token specified in the first run  
### uncomment the loop at the bottom of `faucet/main.py` to run the sporadic request (everyday at 7.00 AM and 6.00 PM it will automatically request to the faucet.) but the log will not print any info in sporadic request mode.

