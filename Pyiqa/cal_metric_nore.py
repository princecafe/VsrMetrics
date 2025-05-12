import pyiqa
import os
import glob
from tqdm import tqdm  # 新增进度条库

# 初始化 IQA 模型
def initialize_metric(metric_name='niqe', device='cuda'):
    # 使用 GPU 加速，如果没有 GPU 可以改为 'cpu'
    return pyiqa.create_metric(metric_name, device=device)

def calculate_single_niqe(image_path, metric):
    # 计算单个图片的 IQA 值
    score = metric(image_path)
    return score

def calculate_image(subfolder, metric):
    # 获取子文件夹中所有 PNG 图片路径
    image_paths = glob.glob(os.path.join(subfolder, '*.png'))
    # 对图片路径进行排序
    image_paths.sort()
    scores = {}
    # 新增进度条
    for image_path in tqdm(image_paths, desc=f"Prossessing images in {subfolder}"):
        score = calculate_single_niqe(image_path, metric)
        # 将张量转换为标量值
        if hasattr(score, 'item'):  # 检查是否是张量
            score = score.item()
        scores[image_path] = score
    # 计算并打印每个子文件夹的平均值
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    print(f'Images in {subfolder}\'s Average {metric_name.upper()} score: {avg_score}')
    return scores

def calculate_subfolder(folder_path, metric):
    # 获取文件夹中所有子文件夹路径
    subfolders = [os.path.join(folder_path, subfolder) for subfolder in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, subfolder))]
    # 对子文件夹路径进行排序
    subfolders.sort()
    all_scores = {}
    all_avg_scores = {}
    # 新增进度条
    for subfolder in tqdm(subfolders, desc=f"Prossessing subfolders in {folder_path}"):
        scores = calculate_image(subfolder, metric)
        all_scores[subfolder] = scores

        all_avg_scores[subfolder] = sum(scores.values()) / len(scores) if scores else 0

    # 计算并打印所有子文件夹的平均值
    overall_avg_score = sum(all_avg_scores.values()) / len(all_avg_scores) if all_avg_scores else 0
    print(f'Overall Average {metric_name.upper()} score: {overall_avg_score}')
    return all_scores

# 示例调用
if __name__ == "__main__":
    folder_path = '/home/Wangzy/VSR/MGLD-VSR/output1/'
    metric_name = 'niqe'
    device = 'cuda'
    metric = initialize_metric(metric_name, device)
    niqe_scores = calculate_subfolder(folder_path, metric)