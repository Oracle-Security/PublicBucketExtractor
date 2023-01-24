import requests

print("""
.___________. __    __   _______      ______   .______          ___       ______  __       _______ 
|           ||  |  |  | |   ____|    /  __  \  |   _  \        /   \     /      ||  |     |   ____|
`---|  |----`|  |__|  | |  |__      |  |  |  | |  |_)  |      /  ^  \   |  ,----'|  |     |  |__   
    |  |     |   __   | |   __|     |  |  |  | |      /      /  /_\  \  |  |     |  |     |   __|  
    |  |     |  |  |  | |  |____    |  `--'  | |  |\  \----./  _____  \ |  `----.|  `----.|  |____ 
    |__|     |__|  |__| |_______|    \______/  | _| `._____/__/     \__\ \______||_______||_______|
""")
print("Oracle's Bucket Extractor")
print("Exfiltrate the planet. :)")
print("file_paths.txt contains all the file paths, enjoy the data!")

#keywords = ["JWT_SECRET", "MONGO_PASSWORD", "PASSWORD", "DB_", "PRIVATE", "KEY", "API_KEY", "api-key", "Card UID", "Total Sales", "SSN", "Credit"]
#urlextensions = txt,xls,csv,db,sql,yaml,env,tftstate,cs,php
#extensions = ["xls", "db", "sql", "yaml", "env", "tfstate"]

keywords = ["db_", "config"]
urlextensions = "php"
excludekeywords = ""
extensions = ["xls"]
access_token = "" #Input your access token.
doKeyword = False
doExtension = True
paths = []
# Set up the API endpoint and parameters

if doKeyword:
    for keyword in keywords:
        endpoint = f"https://buckets.grayhatwarfare.com/api/v1/files/{keyword}{excludekeywords}/0/1000?extensions={urlextensions}&access_token={access_token}"
        response = requests.get(endpoint)
        data = response.json()
        num_results = data["results"]
        print(f"[+] Extracting " + str(num_results) + f" Of Entries for [{keyword}].")
        num_pages = num_results // 1000

        for i in range(1, num_pages + 1):
            endpoint = f"https://buckets.grayhatwarfare.com/api/v1/files/{keyword}{excludekeywords}/{i*1000}/1000?extensions={urlextensions}&access_token={access_token}"
            response = requests.get(endpoint, verify=True)
            print(response.request.url)
            data = response.json()
            #print(data)
            for file in data["files"]:
                domain_name = file["url"]
                full_path = file["fullPath"]
                #file_data = requests.get(f"{domain_name}{full_path}")
                #open(f"{full_path.split('/')[-1]}", "wb").write(file_data.content)
                paths.append((domain_name, full_path))
                # Write the domain_name and full_path to a .txt file
                with open("file_paths.txt", "a") as f:
                    for path in paths:
                        f.write(f"{path[0]}{path[1]}\n")
        # Clear the list to avoid buffer issues
        paths = []

if doExtension:
    for extension in extensions:
        print("[+] Extracting Extensions now.")
        endpoint = f"https://buckets.grayhatwarfare.com/api/v1/files/{excludekeywords}/0/1000?extensions={extension}&access_token={access_token}"
        response = requests.get(endpoint)
        data = response.json()
        num_results = data["results"]
        print(f"[+] Extracting " + str(num_results) + f" Of Entries for [{extension}].")
        num_pages = num_results // 1000

        for i in range(1, num_pages + 1):
            endpoint = f"https://buckets.grayhatwarfare.com/api/v1/files/{excludekeywords}/{i*1000}/1000?extensions={extension}&access_token={access_token}"
            response = requests.get(endpoint, verify=True)
            data = response.json()
            for file in data["files"]:
                domain_name = file["url"]
                full_path = file["fullPath"]
                paths.append((domain_name, full_path))
                with open("ext_paths.txt", "a") as f:
                    for path in paths:
                        f.write(f"{path[0]}{path[1]}\n")
        # Clear the list to avoid buffer issues
        paths = []