#!/bin/bash

REF_VIDEO_FOLDER="D:/Users/CY/Desktop/Diffusion_Model/udm10/GT_video"

DIST_VIDEO_FOLDER="D:/Users/CY/Desktop/Diffusion_Model/udm10/output2_video"

VMAF_MODEL_PATH="C:/ffmpeg/vmaf_v0.6.1neg.json"

OUTPUT_FOLDER="D:/Users/CY/Desktop/Diffusion_Model/udm10/vmaf_results"

mkdir -p "$OUTPUT_FOLDER"

for ref_video in "$REF_VIDEO_FOLDER"/*.mp4; do
    
    filename=$(basename "$ref_video")

    dist_video="$DIST_VIDEO_FOLDER/$filename"

    if [ ! -f "$dist_video" ]; then
        echo "视频 $dist_video 不存在，跳过处理。"
        continue
    fi

    output_file="$OUTPUT_FOLDER/${filename%.mp4}.json"

    ffmpeg-quality-metrics "$dist_video" "$ref_video" -m vmaf --vmaf-model-path "$VMAF_MODEL_PATH" --output-format json > "$output_file"

    echo "处理完成：$filename，结果已保存到 $output_file"
done

echo "所有视频处理完成！"