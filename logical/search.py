
# #!/usr/bin/python

# from apiclient.discovery import build
# from apiclient.errors import HttpError
# from oauth2client.tools import argparser


# # Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# # tab of
# #   https://cloud.google.com/console
# # Please ensure that you have enabled the YouTube Data API for your project.
# DEVELOPER_KEY = "AIzaSyBT_zMEst2Sz8bSFLU63OudONQUb77SnF0"
# YOUTUBE_API_SERVICE_NAME = "youtube"
# YOUTUBE_API_VERSION = "v3"

# def youtube_search(search_string, max_results=5):
#   youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#     developerKey=DEVELOPER_KEY)

#   # Call the search.list method to retrieve results matching the specified
#   # query term.
#   search_response = youtube.search().list(
#     q=search_string,
#     part="id,snippet",
#     maxResults=max_results
#   ).execute()

#   videos = []
#   channels = []
#   playlists = []
#   qset={}

#   # Add each result to the appropriate list, and then display the lists of
#   # matching videos, channels, and playlists.
#   for search_result in search_response.get("items", []):
#     if search_result["id"]["kind"] == "youtube#video":
#       qset['title']=search_result["snippet"]["title"]
#       qset['v_id']=search_result["id"]["videoId"]
#       videos.append(qset)
#     # elif search_result["id"]["kind"] == "youtube#channel":
#     #   channels.append("%s (%s)" % (search_result["snippet"]["title"],
#     #                                search_result["id"]["channelId"]))
#     # elif search_result["id"]["kind"] == "youtube#playlist":
#     #   playlists.append("%s (%s)" % (search_result["snippet"]["title"],
#     #                                 search_result["id"]["playlistId"]))

#   print ("Videos:\n", "\n".join(videos), "\n")
#   # print ("Channels:\n", "\n".join(channels), "\n")
#   # print ("Playlists:\n", "\n".join(playlists), "\n")



# def search_keyword(keyword):

 
#   # argparser.add_argument("--q", help=keyword, default=keyword)
#   # argparser.add_argument("--max-results", help="Max results", default=25)
#   # args = argparser.parse_args()

#   try:
#     youtube_search(keyword, 25)

#   except HttpError as e:
#     print ("An HTTP error %d occurred:\n %s" % (e.resp.status, e.content))

# # keyword="let me love you"
# # search_keyword(keyword)


import requests
import json 
from urllib.error import HTTPError

d_key = "AIzaSyBT_zMEst2Sz8bSFLU63OudONQUb77SnF0"



def get_y_content(content):
    videos = []
    qset={}

    for search_result in content.get("items", []):
      if search_result["id"]["kind"] == "youtube#video":
        qset={}
        qset['title']=search_result["snippet"]["title"]
        qset['v_id']=search_result["id"]["videoId"]
        videos.append(qset)
    return videos


def api_call(keyword, max_r):
  url = "https://www.googleapis.com/youtube/v3/search?q={k_w}&part=snippet&key={d_k}&type=video&videoCategoryId=10&maxResults={m_r}".format(k_w=keyword,d_k=d_key,m_r=max_r)
  content = json.loads(requests.get(url).text)

  return content




def search_keyword(keyword):
  content=""
  ls=[]

  try:
    content=api_call(keyword, 50)
    ls=get_y_content(content)
    return ls

  except HTTPError as e:
    print ("An HTTP error %d occurred:\n %s" % (e.resp.status, e.content))






    # id = []
    # kind=[]
    # description = []
    # title = []
    # time =[]
    # for i in content["items"]:
    #     a=i["id"]
    #     b=i["snippet"]
    #     id.append(a["videoId"])
    #     kind.append(a["kind"])
    #     description.append(b["description"])
    #     title.append(b["title"])
    #     time.append(b["publishedAt"])
    # data = pandas.DataFrame({"id":id, "type":kind,"description":description ,"title":title,"time":time })
    # return(data)

# data=get_youtoube_content(content)
# stat_url="https://www.googleapis.com/youtube/v3/videos?part=statistics&key="+key+"&maxResults=50&id="+str(list(data["id"])).replace("[","").replace("]","").replace("'","")
# stat_content = json.loads(requests.get(stat_url).text)

# def get_youtoube_content_stat(content):
#     id = []
#     commentCount=[]
#     dislikeCount = []
#     favoriteCount = []
#     likeCount=[]
#     viewCount=[]
#     for i in content["items"]:
#         id.append(i["id"])
#         b=i["statistics"]
#         commentCount.append(b["commentCount"])
#         dislikeCount.append(b["dislikeCount"])
#         favoriteCount.append(b["favoriteCount"])
#         likeCount.append(b["likeCount"])
#         viewCount.append(b["viewCount"])
#     data = pandas.DataFrame({"id":id, "commentCount":commentCount,"dislikeCount":dislikeCount ,"favoriteCount":favoriteCount,"likeCount":likeCount, "viewCount":viewCount })
#     return(data)

# data_stat=get_youtoube_content_stat(stat_content)

# data=pandas.merge(data, data_stat,"inner", on="id" )
