# 将指纹库改为组合形式: label: 'video_fp', 'video_timeline', 'audio_fp', 'audio_timeline'
import time
import csv
import re
import os

def process_fp_file(file_path, processed_file_path):
    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        first_row = next(reader)
        pattern = r'^\d+x\d+$'
        if re.match(pattern, first_row['quality']):
            current_category_video = [first_row]
            current_category_audio = []
        else:
            current_category_audio = [first_row]
            current_category_video = []
            
        for row in reader:
            if row['ID'] == first_row['ID']:
                if re.match(pattern, row['quality']):
                    current_category_video.append(row)
                else:
                    current_category_audio.append(row)
            else:
                # 处理上一个url的视频/音频指纹
                with open(processed_file_path, 'a', newline='') as processed_file:
                    writer = csv.writer(processed_file)
                    for video_row in current_category_video:
                        for audio_row in current_category_audio:
                            writer.writerow([video_row['ID'], video_row['url'],video_row['itag'], video_row['quality'], video_row['format'], video_row['end'], audio_row['itag'], audio_row['quality'], audio_row['format'], video_row['fingerprint'], video_row['timeline'], audio_row['fingerprint'], audio_row['timeline']])
                            # writer.writerow([video_row['ID'], video_row['url'], video_row['fingerprint'], video_row['timeline'], audio_row['fingerprint'], audio_row['timeline']])
                
                # 当前url
                first_row = row
                if re.match(pattern, first_row['quality']):
                    current_category_video = [first_row]
                    current_category_audio = []
                else:
                    current_category_audio = [first_row]
                    current_category_video = []

        # 处理最后一个URL
        with open(processed_file_path, 'a', newline='') as processed_file:
            writer = csv.writer(processed_file)
            # 处理上一个url的视频/音频指纹
            for video_row in current_category_video:
                for audio_row in current_category_audio:
                    writer.writerow([video_row['ID'], video_row['url'],video_row['itag'], video_row['quality'], video_row['format'], video_row['end'], audio_row['itag'], audio_row['quality'], audio_row['format'], video_row['fingerprint'], video_row['timeline'], audio_row['fingerprint'], audio_row['timeline']])
                    # writer.writerow([video_row['ID'], video_row['url'], video_row['fingerprint'], video_row['timeline'], audio_row['fingerprint'], audio_row['timeline']])
                

if __name__ == '__main__':
    start = time.time()
    
    fp_file = 'data/yt_fp/yt_fp_wongkim728_202406181700.csv'
    final_fp_file = 'data/final_fp/final_fp_wongkim728_202406181700.csv'

    # fp_file_folder = 'data/yt_fp'
    # for filename in os.listdir(fp_file_folder):
        # fp_file = os.path.join(fp_file_folder, filename).replace('\\', '/')
    # final_fp_file = 'data/final_fp/final_' + filename.split('_', 1)[1]
    if not os.path.exists(final_fp_file):
        with open(final_fp_file, 'w', newline='') as processed_file:
            writer = csv.writer(processed_file)
            writer.writerow(['ID', 'url', 'video_itag', 'video_quality', 'video_format', 'video_header_end', 'audio_itag','audio_quality', 'audio_format', 'video_fp', 'video_timeline', 'audio_fp', 'audio_timeline'])
            # writer.writerow(['ID', 'url', 'video_fp', 'video_timeline', 'audio_fp', 'audio_timeline'])
        process_fp_file(fp_file, final_fp_file)
    
    print(f'###一共{time.time()-start}s###')

