# file_op_tools  

# 一、操作对象  


# 1.普通文件和文件夹
这是一个简单的文件操作封装


# 目前的命令  
# 注：部分命令支持了普通文件和文件夹的操作，所有的命令操作都将支持导出过程性txt中间文件
  ## 查
  find -src=... -base=... -export=...(将查询结果导出成指定路径下的txt文件中)
  ## 改名
  add_tail -src=... -tail=...  -base=...  
  add_head -src=... -head=...  -base=...
  ## 拷贝
  copy -src=... -dst=...(这里指目标的文件夹)  
  copydir -src=... -dst=...(这里指目标的文件夹)
  ##  剪切
  move -src=... -dst=...(这里指目标文件夹)  
  movedir -src=... -dst=...(这里指目标文件夹)
  ##  删除
  delete -src=...  
  deletedir -src=...  

# 2.压缩包

  ## 列举压缩包下一级的所有文件(包括文件夹)
  findzip -src=... -base=...  -export=将所有文件名称导出到目标txt中
  ## 打包压缩
  package -src=... -dst=...
  ## 解压
  unpackage -src=... -dst=...

# 二、依赖库
    pip install shutilwhich
    pip install glob3
    pip install click


# 三、运行方式(Windows)
    以fileop.py为例:
    在对应的文件目录下进入，dos输入:  python fileop.py 命令名  -参数名1=参数值1  -参数名2=参数值2  ......
  
