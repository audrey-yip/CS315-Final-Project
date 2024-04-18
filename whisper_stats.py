import pandas as pd
import numpy as np
import json
import openai
from openai import OpenAI
from cs315project2datacollection.download_videos import download_tiktok_mp3s

def generate_video_id_list():
    # Read the CSV file containing cosine similarities
    df = pd.read_csv("cosinedata/overall_cosine_similarities.csv")
    df = df[df['cos_score'].notnull()]
    # Pandas DF Cols: video id, description, similarities
    df = df.sort_values(by=['cos_score'], ascending=False)

    # sort by cosine similarity, in order of greatest similarity
    files_to_transcribe = df.iloc[:30]['video_id']
    # print(files_to_transcribe)
    return files_to_transcribe.values.tolist(), df.iloc[:30]

def get_author_usernames_by_video_id(df):
    names = ["raw_tiktokData/pyktok_data/results_AL.csv",
             "raw_tiktokData/pyktok_data/results_AY.csv",
             "raw_tiktokData/pyktok_data/results_CF.csv",
             "raw_tiktokData/pyktok_data/results_JK.csv",
             "raw_tiktokData/pyktok_data/results_MG.csv",
             'raw_tiktokData/pyktok_data/results_MM.csv']

    author_df = pd.DataFrame()
    for name in names:
        df2 = pd.read_csv(name)
        author_df = pd.concat([author_df, df2])

    # Filter author_df to include only the rows with video_ids present in df1
    filtered_author_df = author_df[author_df['video_id'].isin(df['video_id'])]

    merged_df = pd.merge(df, filtered_author_df[['video_id', 'author_username']], on='video_id', how='left')
    # print(merged_df[['video_id', 'author_username']])
    return merged_df

def transcribe(identifiers):
    filenames = [f"@{username}_video_{id}.mp3" for (username,id) in identifiers]

    client = OpenAI(api_key='')

    responses = {}

    for filename in filenames:
        try:
            audio = open(filename, "rb")
            transcription = client.audio.transcriptions.create(
                model="whisper-1",
                response_format="verbose_json",
                file=audio
            )
            responses[filename] = transcription
        except openai.BadRequestError:
            continue
    return responses

if __name__ == "__main__":
    ids, df = generate_video_id_list()
    merged_df = get_author_usernames_by_video_id(df) # 'https://www.tiktok.com/@' + data_loc[v]['author'] + '/video/' + data_loc[v]['id']
    urls = []
    for id in ids:
        url = merged_df.loc[merged_df['video_id'] == id, 'author_username'].values[0] + '/video/' + str(id)
        urls.append('https://www.tiktok.com/@' + url)
    # download_tiktok_mp3s(urls)
    # print(merged_df)
    for _,row in merged_df.iterrows():
        print((row['author_username'], row['video_id']))
    responses = transcribe(list((row['author_username'], row['video_id']) for _, row in merged_df.iterrows()))
    
    r = {k: v.text for k,v in dict(responses).items()}
    with open("transcripts.json", "w") as outfile: 
        json.dump(r, outfile)

    

# Usage: python whisper_stats.py