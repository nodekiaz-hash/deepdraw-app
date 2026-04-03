import requests

url = "https://crlhkdftulncmrcyctya.supabase.co/rest/v1/users"
headers = {
    "apikey": "sb_publishable_ScFyHjHK10qnqi7AVkz32A_nUmSCPc7",
    "Authorization": "Bearer sb_publishable_ScFyHjHK10qnqi7AVkz32A_nUmSCPc7"
}

response = requests.get(url, headers=headers)

print(response.json())