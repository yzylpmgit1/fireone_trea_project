# import pandas as pd
# print(pd.__version__)  # 应输出 2.2.2



# import matplotlib
# print(matplotlib.__version__)  # 应输出 3.9.2
# # 或
# import matplotlib.pyplot as plt
# print(plt.__version__)



# import torch
# print(torch.__version__)
# # 检查CUDA是否可用（如需要GPU支持）
# print(torch.cuda.is_available())



# import gensim
# print(gensim.__version__)


# import sklearn
# print(sklearn.__version__)  # 应输出 1.5.1



# import peft
# print(peft.__version__)  # 应输出 0.15.0



# import transformers
# print(transformers.__version__)



packages = {
    'pandas': '2.2.2',
    'matplotlib': '3.9.2',
    'torch': None,        # 版本根据安装方式不同
    'gensim': None,
    'sklearn': '1.5.1',
    'peft': '0.15.0',
    'transformers': None
}

for pkg, expected in packages.items():
    try:
        if pkg == 'sklearn':
            module = __import__('sklearn')
        else:
            module = __import__(pkg)
        version = getattr(module, '__version__', 'unknown')
        status = f"✓ 版本: {version}"
        if expected and version != expected:
            status += f" (⚠️ 期望: {expected})"
        print(f"{pkg:15} {status}")
    except ImportError:
        print(f"{pkg:15} ✗ 未安装")