import pandas as pd


def write_video_infos_into_csv(video_infos, csv_file_path):
    df = pd.DataFrame(video_infos)
    df['viewed_number'] = df['viewed_number'].apply(
        lambda x: ','.join(map(str, x)))
    df['likes_number'] = df['likes_number'].apply(
        lambda x: ','.join(map(str, x)))
    df['comments_number'] = df['comments_number'].apply(
        lambda x: ','.join(map(str, x)))
    df['saved_number'] = df['saved_number'].apply(
        lambda x: ','.join(map(str, x)))
    df['shared_number'] = df['shared_number'].apply(
        lambda x: ','.join(map(str, x)))
    df['record_time'] = df['record_time'].apply(
        lambda x: ','.join(map(str, x)))
    df.to_csv(csv_file_path, index=False)


def get_current_csv(csv_file_path):
    df = pd.read_csv(csv_file_path)

    transformed_data = []

    for index, row in df.iterrows():
        video_info = {
            "video_title": row['video_title'],
            "video_link": row['video_link'],
            "viewed_number": row['viewed_number'].split(',') if isinstance(row['viewed_number'], str) else [row['viewed_number']],
            "likes_number": row['likes_number'].split(',') if isinstance(row['likes_number'], str) else [row['likes_number']],
            "comments_number": row['comments_number'].split(',') if isinstance(row['comments_number'], str) else [row['comments_number']],
            "saved_number": row['saved_number'].split(',') if isinstance(row['saved_number'], str) else [row['saved_number']],
            "shared_number": row['shared_number'].split(',') if isinstance(row['shared_number'], str) else [row['shared_number']],
            "record_time": row['record_time'].split(',') if isinstance(row['record_time'], str) else [row['record_time']],
        }

        transformed_data.append(video_info)
    return transformed_data
