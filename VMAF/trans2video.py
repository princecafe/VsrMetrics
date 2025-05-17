import cv2
import os
import os.path as osp

def images_to_video(image_folder, video_path, fps=30):

    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    image_files.sort()

    if not image_files:
        print("未找到图片文件。")
        return

    first_image = cv2.imread(os.path.join(image_folder,image_files[0]))
    #height, width = 720,1272
    height, width,_ = first_image.shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)
        if image is not None:
            image = cv2.resize(image, (width, height))
            out.write(image)
    out.release()

    print(f"视频已保存到 {video_path}")

for i in range(0,50):
    if i <10:
        image_folder = '/home/Cheny/input/VideoLQ/HR_rbv/00'+str(i)
        video_path = '/home/Cheny/input/VideoLQ/HR_rbv_video/0'+str(i)+'.mp4' 
    else:
        image_folder = '/home/Cheny/input/VideoLQ/HR_rbv/0'+str(i)
        video_path = '/home/Cheny/input/VideoLQ/HR_rbv_video/'+str(i)+'.mp4'    
    images_to_video(image_folder, video_path, fps=30)

#    # 遍历父文件夹下的子文件夹
# parent_folder = '/home/Cheny/input/udm10/LR'  # 替换为父文件夹路径
# for sub_folder in os.listdir(parent_folder):
#     sub_folder_path = os.path.join(parent_folder, sub_folder)
#     if os.path.isdir(sub_folder_path):
#         video_path = os.path.join('/home/Cheny/input/udm10/LR_video/', f"{sub_folder}.mp4")
#         images_to_video(sub_folder_path, video_path, fps=30)