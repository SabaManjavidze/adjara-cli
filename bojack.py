from genericpath import exists
import os
import wget
from pathlib import Path
import requests
import json

boiler = "https://api.adjaranet.com/api/v1/"
search_url = "search?filters%5Btype%5D=movie%2C&keywords="

query = input("Enter query: ")

results_promise = requests.get(f'{boiler}{search_url}{query}&source=adjaranet')
results_data = results_promise.json()

print("\n")

for index,i in enumerate(results_data["data"]):
    print(f'[{index}] {i["secondaryName"]}')

index = int(input("Enter index: "))
print("\n")

selected_movie = results_data["data"][index]


def downloadfile(name,url):
        name=f'./Adventure_Time/{name}.mp4'
        r=requests.get(url)
        print("****Connected****")
        os.makedirs(os.path.dirname(name), exist_ok=True)
        output_file = open(name,"wb")
        print(f'-------------- {name} --------------')
        print("Donloading.....")
        for chunk in r.iter_content(chunk_size=255): 
            if chunk: # filter out keep-alive new chunks
                output_file.write(chunk)

        print("Done")
        output_file.close()

def getMovieFiles(js):
    for ind,i in enumerate(js["data"]):
        ind += 1
        for j in i["files"]:
            if(j["lang"] == "ENG"):
                for y in j["files"]:
                    if(y["quality"] == "HIGH"):
                        method = input("Download (d), Episode Links (l): ")
                        if(method=="d"):
                            downloadfile(js["title"],y["src"])
                        if(method=="l"):
                            print(y["src"]+"\n"+str(ind))

if selected_movie["isTvShow"] == False:
   movie_req = requests.get(f'{boiler}movies/{selected_movie["id"]}/season-files/1?source=adjaranet') 
   movie_data = movie_req.json()
   getMovieFiles(movie_data)
else:
    season = int(input("Enter season: "))
    print("\n")
    tv_show_url = f'{boiler}movies/{selected_movie["id"]}/season-files/{season}?source=adjaranet'
    tv_show_req = requests.get(tv_show_url)
    tv_show_data = tv_show_req.json()
    # print(tv_show_url)
    # print(f'tv show data : {json.dumps(tv_show_data,indent=2)}')
    getMovieFiles(tv_show_data)


