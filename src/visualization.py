import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from write_csv import get_current_csv
import matplotlib


def convert_k_m_to_number(s):
    if 'K' in s:
        return float(s.replace('K', '')) * 1000
    elif 'M' in s:
        return float(s.replace('M', '')) * 1000000
    else:
        return s


def preprocess_info_dict(info):

    keys_to_convert = ['viewed_number', 'likes_number',
                       'comments_number', 'saved_number', 'shared_number']
    max_length = max(len(info[key]) for key in keys_to_convert if key in info)

    for key in keys_to_convert:
        if key in info:
            info[key] = [convert_k_m_to_number(val) for val in info[key]] + [
                info[key][-1] if info[key] else 0] * (max_length - len(info[key]))

    if 'record_time' in info:
        info['record_time'] = info['record_time'] + \
            [''] * (max_length - len(info['record_time']))

    return info


def draw_metrics_separate_axes(object_data):
    object_data['record_time'] = pd.to_datetime(
        object_data['record_time'], format='%m/%d %H:%M', errors='coerce')
    raw_numbers = object_data['viewed_number']
    int_viewed_numbers = [None] * len(raw_numbers)

    for i in range(len(raw_numbers)):
        if isinstance(raw_numbers[i],  float):
            int_viewed_numbers[i] = int(raw_numbers[i])
        elif isinstance(raw_numbers[i],  str) and 'K' in raw_numbers[i]:
            int_viewed_numbers[i] = int(
                float(raw_numbers[i][:-1]) * 1000)
        elif isinstance(raw_numbers[i], int):
            int_viewed_numbers[i] = raw_numbers[i]
        else:
            int_viewed_numbers[i] = ''

    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:blue'
    ax1.set_xlabel('Record Time')
    ax1.set_ylabel('Views', color=color)
    ax1.plot(object_data['record_time'], int_viewed_numbers,
             label='Views', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    metrics = ['likes_number',
               'comments_number', 'shared_number', 'saved_number']
    colors = ['tab:green', 'tab:red', 'tab:purple', 'tab:brown']
    labels = ['Likes',  'Comments', 'Shares', 'Saves']

    axes = [ax1.twinx() for _ in metrics]
    for metric, ax, color, label in zip(metrics, axes, colors, labels):
        ax.plot(object_data['record_time'], object_data[metric],
                label=label, color=color, marker='o')
        ax.set_ylabel(label, color=color)
        ax.tick_params(axis='y', labelcolor=color)

    for i, ax in enumerate(axes):
        ax.spines['right'].set_position(('outward', i * 60))

    fig.tight_layout()
    fig.legend(loc='upper left', bbox_to_anchor=(0.1, 0.9))
    plt.subplots_adjust(top=0.9, bottom=0.1)
    char_title = object_data['video_title']
    plt.title(f'{char_title}')
    plt.show()


def get_video_by_title(video_infos, video_title):
    for video_info in video_infos:
        if video_info['video_title'] == video_title:
            return video_info
    return None


def plot_by_video_title(video_infos, video_title):
    video_info = get_video_by_title(video_infos, video_title)
    processed_info = preprocess_info_dict(video_info)
    draw_metrics_separate_axes(processed_info)


load_dotenv()
matplotlib.rcParams['font.family'] = 'Heiti TC'
matplotlib.rcParams['axes.unicode_minus'] = False
csv_dir = os.getenv('CSV_DIR')
video_infos = get_current_csv(csv_dir)
video_title = input('please enter the video title you want to search: \n')
try:
    plot_by_video_title(video_infos, video_title)
except Exception as e:
    print(f'plot error: {e}')

# preprocess_infos = [None] * len(video_infos)

# for i in range(len(video_infos)):
#     try:
#         preprocess_infos[i] = preprocess_info_dict(video_infos[i])
#         draw_metrics_separate_axes(preprocess_infos[i])
#     except Exception as e:
#         print(f"Error processing video '{video_infos[i]['video_title']}': {e}")
#         continue
