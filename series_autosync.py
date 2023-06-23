import os
import subprocess
from tqdm import tqdm

series_path = '/mnt/nas/media/series'

for series in tqdm(os.listdir(series_path)):
    season_path = os.path.join(series_path, series)
    for season in os.listdir(season_path):
        if 'Season' not in season:
            continue
        now_path = os.path.join(season_path, season)
        season_idx = int(season.split(' ')[-1])
        files = os.listdir(now_path)
        epi_files = [epi for epi in files if epi.endswith(('.mp4', 'mkv'))]
        sub_files = [sub for sub in files if sub.endswith(('.srt', '.ass'))]
        for epi_idx in range(1, len(epi_files)+1):
            format_name = f'S{season_idx:02d}E{epi_idx:02d}'
            now_subs = [sub for sub in sub_files if format_name in sub]
            now_epi = [epi for epi in epi_files if format_name in epi]
            if now_epi:
                for sub in now_subs:
                    sub_path = os.path.join(now_path, sub)
                    
                    synced_sub = f'{sub[:-4]}.同步中文.{sub[-3:]}'
                    if synced_sub in sub_files:
                        print(f'[INFO] {synced_sub}已存在')
                        break
                    synced_path = os.path.join(now_path, synced_sub)
                    
                    epi_path = os.path.join(now_path, now_epi[0])
                    
                    subprocess.call(f'ffs "{epi_path}" -i "{sub_path}" -o "{synced_path}"', shell=True)
                    print(f'[INFO] done with: {sub}')
            elif now_epi is []:
                print(f'[ERR] there is no {format_name} in {series}')
        print(f'[INFO] done with: {season}')
    print(f'[INFO] done with: {series}')
    