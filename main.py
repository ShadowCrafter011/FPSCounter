from pymediainfo import MediaInfo
from ProgressBar import PBar
import cv2
import os


def main():
    base_path = input("What directory would you like to analyze? ")

    if not os.path.isdir(base_path):
        print("This path doesn't seem to lead to a valid directory")
        main()
        return

    total_files = file_amount(base_path)
    print(f"Analyzing {total_files} files")

    pbar_counter, pbar = PBar.new(50, total_files, refresh_rate=.5)
    fps_results = recursive_fps_read(base_path, pbar_counter)
    pbar.wait_complete()
    total_video_files = fps_results.pop("total")
    fps_results = dict(sorted(fps_results.items(), key=lambda item: item[1], reverse=True))

    print(f"\nVideos grouped by FPS value ({total_video_files} total video files)\n")
    for fps, amount in fps_results.items():
        print(f"\t{fps} FPS\t{amount}\t{round((amount / total_video_files) * 100, 1)}%")


def recursive_fps_read(path: str, counter: any) -> dict:
    fps_amount = {"total": 0}
    for file_path in os.listdir(path):
        file_path = os.path.join(path, file_path)

        if os.path.isdir(file_path):
            fps_amount = merge_dict(fps_amount, recursive_fps_read(file_path, counter))
            continue

        counter.value += 1

        if not is_video(file_path):
            continue

        fps_amount["total"] += 1

        if (fps := str(round(get_fps(file_path), 2))) in fps_amount:
            fps_amount[fps] += 1
        else:
            fps_amount[fps] = 1

    return fps_amount


def file_amount(path: str) -> int:
    amount = 0
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isdir(file):
            amount += file_amount(file)
            continue
        amount += 1
    return amount


def merge_dict(*dicts: dict) -> dict:
    output_dict = {}
    for d in dicts:
        for key, value in d.items():
            if key in output_dict:
                output_dict[key] += value
            else:
                output_dict[key] = value
    return output_dict


def get_fps(path: str) -> float:
    cap = cv2.VideoCapture(path)
    return cap.get(cv2.CAP_PROP_FPS)


def is_video(path: str) -> bool:
    file_info = MediaInfo.parse(path)
    for track in file_info.tracks:
        if track.track_type == "Video":
            return True
    return False


if __name__ == '__main__':
    main()
