import csv
import pandas as pd


def write_video_infos_into_csv(video_infos, csv_file_path):
    video_info_df = pd.DataFrame(video_infos)
    video_info_df.to_csv(csv_file_path, index=False)


def get_current_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)

    transformed_data = []

    for index, row in df.iterrows():
        video_info = {
            "video_title": row['video_title'],
            "video_link": row['video_link'],
            "viewed_number": row['viewed_number'],
            "likes_number": row['likes_number'].split(','),
            "comments_number": row['comments_number'].split(','),
            "saved_number": row['saved_number'].split(','),
            "shared_number": row['shared_number'].split(','),
            "record_time": row['record_time'].split(',')
        }

        transformed_data.append(video_info)
    print(transformed_data)


get_current_csv('../geevideo_video_stats2.csv')
