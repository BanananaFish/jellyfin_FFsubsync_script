import os
import subprocess
from tqdm import tqdm

movies_path = '/path/to/your/lib'

for movie in tqdm(os.listdir(movies_path)):
    now_path = os.path.join(movies_path, movie)
    files = os.listdir(now_path)
    sub_files = [sub for sub in files if sub.endswith(('.srt', '.ass'))] # select sub file
    
    # select media file
    for file in files:
        if file.endswith(('.mp4', '.mkv')):
            movie_file = file
            break
        else:
            movie_file = None
            
    if movie_file:
        for sub in sub_files:
            sub_path = os.path.join(now_path, sub)
            synced_sub = f'{sub[:-4]}.同步中文.{sub[-3:]}'
            if synced_sub in sub_files:
                print(f'[INFO] {synced_sub}已存在')
                break
            synced_path = os.path.join(now_path, synced_sub)
            movie_path = os.path.join(now_path, movie_file)
            # call FFsubsync
            subprocess.call(f'ffs "{movie_path}" -i "{sub_path}" -o "{synced_path}"', shell=True)
            print(f'[INFO] done with: {sub}')
    elif movie_file is None:
        print(f'[ERR] cant find movie in {movie}')
    elif not sub_files:
        print(f'[ERR] cant find sub in {movie}')
    