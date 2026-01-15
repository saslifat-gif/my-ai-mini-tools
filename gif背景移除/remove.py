import os
import glob
from PIL import Image

def remove_background(input_path, output_path, tolerance=30):
    """
    GIF去底工具 (稳定兼容版)
    回归到最简单的逻辑，但强化了对微信透明格式的兼容性。
    :param tolerance: 容差 (0-255)。越大则去除的范围越广。
    """
    
    print(f"🔍 正在处理: {input_path}")
    
    try:
        im = Image.open(input_path)
    except Exception as e:
        print(f"❌ 无法打开文件: {e}")
        return

    # 获取GIF基本信息
    duration = im.info.get('duration', 100)
    loop = im.info.get('loop', 0) 
    
    # 尝试获取左上角颜色作为背景色参考
    try:
        bg_ref = im.convert("RGB").getpixel((0, 0))
        print(f"🎨 参考背景色: {bg_ref} (左上角)")
    except:
        bg_ref = (255, 255, 255) # 获取失败就默认白色

    output_frames = []
    
    # 遍历每一帧
    try:
        while True:
            # 1. 转为 RGBA
            frame = im.convert('RGBA')
            datas = frame.getdata()
            new_data = []

            # 2. 像素级去底 (使用容差判断)
            # 计算像素与参考背景色的差异，或者直接判断是否足够白
            for item in datas:
                # item 是 (R, G, B, A)
                
                # 判断1: 是否接近纯白 (之前的逻辑)
                is_white = item[0] > (255 - tolerance) and item[1] > (255 - tolerance) and item[2] > (255 - tolerance)
                
                # 判断2: 是否接近左上角的背景色 (针对非纯白背景)
                # 计算欧氏距离的简化版
                diff = abs(item[0] - bg_ref[0]) + abs(item[1] - bg_ref[1]) + abs(item[2] - bg_ref[2])
                is_bg_color = diff < (tolerance * 3)

                if is_white or is_bg_color:
                    # 设为全透明
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            
            frame.putdata(new_data)

            # 3. 转换为 GIF 兼容模式 (P模式)
            # 为了防止画质变差，我们使用 'WEB' 调色板或者自适应
            # 关键：dither=None 防止噪点
            alpha = frame.split()[3]
            frame_p = frame.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)
            
            # 将透明区域的索引设为 255
            mask = Image.eval(alpha, lambda a: 255 if a <= 128 else 0)
            frame_p.paste(255, mask)
            
            output_frames.append(frame_p)
            
            im.seek(im.tell() + 1)

    except EOFError:
        pass 

    print(f"✅ 处理完成，共 {len(output_frames)} 帧。")

    if output_frames:
        # 4. 保存 (关键参数设置)
        output_frames[0].save(
            output_path,
            save_all=True,
            append_images=output_frames[1:],
            optimize=False,
            duration=duration,
            loop=loop,
            disposal=2,      # 🌟 关键：2 表示"恢复背景色"，这是透明GIF必须的，否则会重影
            transparency=255 # 🌟 关键：指定255号颜色为透明
        )
        print(f"🎉 已保存至: {output_path}")
        print("💡 如果边缘有白边，可以尝试把代码里的 tolerance 改大一点 (比如 50)。")
    else:
        print("❌ 失败：没有提取到帧。")

if __name__ == "__main__":
    # --- 参数调整区 ---
    # 容差值：默认 30。
    # 如果觉得背景去不干净，改大 (比如 60)
    # 如果觉得把主体抠坏了，改小 (比如 10)
    tolerance_value = 30

    # 自动查找并处理
    if os.path.exists("input.gif"):
        remove_background("input.gif", "output_final.gif", tolerance_value)
    else:
        gif_files = glob.glob("*.gif")
        # 排除之前生成的 output
        input_gifs = [f for f in gif_files if "output" not in f and "transparent" not in f and "fixed" not in f]
        
        if input_gifs:
            target = input_gifs[0]
            print(f"👉 自动选择文件: {target}")
            remove_background(target, f"final_{target}", tolerance_value)
        else:
            print("❌ 未找到GIF文件")