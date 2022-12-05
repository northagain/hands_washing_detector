"""
@Project: Input video to detecte the hands-washing status.
@File: hands-washing_detector.py
@Date: 22/08/09 
"""
import json
import cv2
import os

# get_scope函数：输出检测矩形坐标


def get_scope(keypoints):
    x1, y1, x2, y2 = keypoints[2*3], keypoints[2 *
                                               3+1], keypoints[5*3], keypoints[3*3+1]
    return x1, y1, x2, y2

# detector函数：输出当前帧状态


def detector(json_data):
    for v in json_data['people']:
        temp = v['pose_keypoints_2d']
        # 获得矩形区域
        x1, y1, x2, y2 = get_scope(temp)
        # 获得手掌坐标
        lx, ly = temp[4*3], temp[4*3+1]
        rx, ry = temp[7*3], temp[7*3+1]
        # 检测算法有待优化
        if(lx <= x2 and rx <= x2 and lx >= x1 and rx >= x1 and ly >= y1 and ry >= y1 and ly <= y2 and ry <= y2):
            cv2.putText(frame, 'Status: Washing hands!', (0, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5)
        else:
            cv2.putText(frame, 'Status: ===========', (0, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 5)


if __name__ == '__main__':
    json_dir = "C:/Users/25102/Desktop/openpose/output_jsons/"
    json_list = os.listdir(json_dir)
    json_list.sort()

    video = cv2.VideoCapture(
        "C:/Users/25102/Desktop/openpose/output/result.avi")
    # video_writer = cv2.VideoWriter(os.path.join(
    #     out_path, out_name), fourcc, 50, (1080, 1920))

    # frame_fps = video.get(cv2.CAP_PROP_FPS)
    # frame_height = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # frame_width = video.get(cv2.CAP_PROP_FRAME_WIDTH)
    # fps = frame_fps
    # size = (1080, 1920)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('final.mp4', fourcc, 50, (1080, 1920))

    if video.isOpened():
        openn, frame = video.read()
    else:
        openn = False

    i = 0

    while openn:
        ret, frame = video.read()
        if frame is None:
            break
        if ret == True:
            with open(json_dir+json_list[i], 'r', encoding='utf8') as fp:
                json_data = json.load(fp)
                detector(json_data)
                # 显示状态
                cv2.namedWindow('Detector', 0)
                cv2.resizeWindow('Detector', 600, 800)
                cv2.imshow('Detector', frame)
                out.write(frame)
                i = i+1
                # 按下 ESC 键即可退出该窗口
                if cv2.waitKey(1) & 0xFF == 27:
                    break

    video.release()
    cv2.destroyAllWindows
