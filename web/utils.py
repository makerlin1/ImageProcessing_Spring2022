# -*- coding: utf-8 -*-
from multiprocessing import Process
import os
# import paddlehub as hub

# 加载模型
# 可根据需要更换上述模型中的任何一个
# module_name = 'falsr_c'
# sr_model = hub.Module(name=module_name)
# print('[+] 模型加载完成')
    
def convert_(filename):
    input_path = f"./input/{filename}"
    output_dir = f"./output/"
    
    command = ' '.join(['hub run', 'falsr_c', '--input_path', input_path,  '--output_dir', output_dir])
    cwd = './'
    
    os.system(f"cd {cwd}&&{command}")
    
    # 调用预测接口
    # res = sr_model.reconstruct(
        # images=None,
        # paths=[input_path],
        # use_gpu=False,
        # visualization=True,
        # output_dir=output_dir
    # )
    
def convert(filename):
    Process(target=convert_,kwargs={"filename": filename}).start()
    

if __name__ == '__main__':
    filename = 'test.jpg'
    convert(filename)