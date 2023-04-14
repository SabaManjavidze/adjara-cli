import sys
import os
import requests
import json

boiler = "https://api.adjaranet.com/api/v1/"
search_url = "search?filters%5Btype%5D=movie%2C&keywords="

query = input("Enter query: ")

results_promise = requests.get(f"{boiler}{search_url}{query}&source=adjaranet")
results_data = results_promise.json()

print("\n")

for index, i in enumerate(results_data["data"]):
    print(f'[{index}] {i["secondaryName"]}')

index = int(input("Enter index: "))
print("\n")

selected_movie = results_data["data"][index]

method = input("Download (d), Episode Links (l): ")

def downloadfile(name, url):
    movie_dir = selected_movie["secondaryName"]
    file_name = f'./{movie_dir}/{name}.mp4'
    if (not os.path.exists(f'./{movie_dir}')):
        os.mkdir(f'./{movie_dir}')
    with open(file_name, "wb") as f:
        print("Downloading %s" % file_name)
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
                print("\n")


def getMovieFiles(js):
    for ind, i in enumerate(js["data"]):
        ind += 1
        if (ind < int(ep_start)):
            continue
        if (ind > int(ep_finish)):
            print("finished")
            break
        for j in i["files"]:
            if j["lang"] == "ENG":
                for y in j["files"]:
                    if y["quality"] == "HIGH":
                        if method == "d":
                            downloadfile(i["title"], y["src"])
                        if method == "l":
                            print(y["src"] + "\n" + str(ind))


ep_start = ""
ep_finish = ""

if selected_movie["isTvShow"] is False:
    movie_req = requests.get(
        f'{boiler}movies/{selected_movie["id"]}/season-files/1?source=adjaranet'
    )
    movie_data = movie_req.json()
    getMovieFiles(movie_data)
else:
    season = int(input("Enter season: "))
    print("\n")
    tv_show_url = (
        f'{boiler}movies/{selected_movie["id"]}/season-files/{season}?source=adjaranet'
    )
    tv_show_req = requests.get(tv_show_url)
    tv_show_data = tv_show_req.json()

    ep_range = input("Enter Episode Range: ")
    ep_range_split = ep_range.split("-")[0]
    ep_start = ep_range_split[0]
    ep_finish = ep_range.split("-")[1]
    # print(tv_show_url)
    # print(f'tv show data : {json.dumps(tv_show_data,indent=2)}')
    getMovieFiles(tv_show_data)


