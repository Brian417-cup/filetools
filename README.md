# file_op_tools
这是一个简单的文件操作封装


# 目前的命令
  ## 查
  find -src=... -base=...
  ## 改名
  add_tail -src=... -tail=...  -base=...  
  add_head -src=... -head=...  -base=...
  ## 拷贝
  copy -src=... -dst=...(这里指目标的文件夹)
  ##  剪切
  move -src=... -dst=...(这里指目标文件夹)

# 依赖库
    pip install shutilwhich
    pip install glob3
    pip install click


# 运行方式(Windows)
    以fileop.py为例:
    在对应的文件目录下进入，dos输入:  python fileop.py 命令名  -参数名1=参数值1  -参数名2=参数值2  ......
  
