# Mix3r
A wordlist mixer that increases the probability of successful password cracking using common user password combinations. 


# Usage

## Single Wordlist

`python3 ~/mix3r.py ~/wordlists/rockyou.txt | hashcat -m 1000 ntlm-hashes -r ~/cracking/rules/OneRuleToRuleThemAll.rule -O -w 3 --backend-ignore-cuda`

## Wordlist Directory

`python3 ~/mix3r.py ~/wordlists/ | hashcat -m 1000 ntlm-hashes -r ~/cracking/rules/OneRuleToRuleThemAll.rule -O -w 3 --backend-ignore-cuda`

