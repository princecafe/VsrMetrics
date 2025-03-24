import pyiqa
import os
import glob
from tqdm import tqdm  # 新增进度条库

# 初始化 IQA 模型
def initialize_metric(metric_name='niqe', device='cuda'):
    # 使用 GPU 加速，如果没有 GPU 可以改为 'cpu'
    return pyiqa.create_metric(metric_name, device=device)

def calculate_single_niqe(ref_image_path, dist_image_path, metric):
    # 获取图片名称
    ref_image_name = os.path.basename(ref_image_path)
    dist_image_name = os.path.basename(dist_image_path)
    
    # 验证图片名称是否一致
    if ref_image_name != dist_image_name:
        raise ValueError(f"Image names must be the same: {ref_image_name} != {dist_image_name}")
    
    # 计算单个图片的 IQA 值
    score = metric(ref_image_path, dist_image_path)
    return score

def calculate_image(ref_subfolder, dist_subfolder, metric):
    # 获取子文件夹中所有 PNG 图片路径
    ref_image_paths = glob.glob(os.path.join(ref_subfolder, '*.png'))
    dist_image_paths = glob.glob(os.path.join(dist_subfolder, '*.png'))
    # 对图片路径进行排序
    ref_image_paths.sort()
    dist_image_paths.sort()
    scores = {}
    for ref_image_path, dist_image_path in zip(ref_image_paths, dist_image_paths):
        score = calculate_single_niqe(ref_image_path, dist_image_path, metric)
        # 将张量转换为标量值
        if hasattr(score, 'item'):  # 检查是否是张量
            score = score.item()
        scores[os.path.basename(ref_image_path)] = score
    # 计算并打印每个子文件夹的平均值
    avg_score = sum(scores.values()) / len(scores) if scores else 0
    print(f'Images in {dist_subfolder}\'s Average {metric_name.upper()} score: {avg_score}')
    return scores

def calculate_subfolder(ref_folder_path, dist_folder_path, metric):
    # 获取文件夹中所有子文件夹路径
    ref_subfolders = [os.path.join(ref_folder_path, subfolder) for subfolder in os.listdir(ref_folder_path) if os.path.isdir(os.path.join(ref_folder_path, subfolder))]
    dist_subfolders = [os.path.join(dist_folder_path, subfolder) for subfolder in os.listdir(dist_folder_path) if os.path.isdir(os.path.join(dist_folder_path, subfolder))]
    # 对子文件夹路径进行排序
    ref_subfolders.sort()
    dist_subfolders.sort()
    all_scores = {}
    all_avg_scores = {}
    for ref_subfolder, dist_subfolder in zip(ref_subfolders, dist_subfolders):
        scores = calculate_image(ref_subfolder, dist_subfolder, metric)
        all_scores[os.path.basename(ref_subfolder)] = scores

        all_avg_scores[os.path.basename(ref_subfolder)] = sum(scores.values()) / len(scores) if scores else 0

    # 计算并打印所有子文件夹的平均值
    overall_avg_score = sum(all_avg_scores.values()) / len(all_avg_scores) if all_avg_scores else 0
    print(f'Overall Average {metric_name.upper()} score: {overall_avg_score}')
    return all_scores

# 示例调用
if __name__ == "__main__":
    ref_folder_path = '/home/Wangzy/VSR/dataset/UDM10/BDx4'
    dist_folder_path = '/home/Wangzy/VSR/dataset/UDM10/BIx4'
    metric_name = 'vmaf'  # 修改为有参考指标
    device = 'cuda'
    metric = initialize_metric(metric_name, device)
    niqe_scores = calculate_subfolder(ref_folder_path, dist_folder_path, metric)