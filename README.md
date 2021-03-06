# file_op_tools  
#### 这是一个简单的文件操作封装

# 一、操作对象  


## 1.普通文件和文件夹
## --目前支持ide命令操作  
## 注：部分命令支持了普通文件和文件夹的操作，所有的命令操作都将支持导出过程性txt中间文件
  ### 查
  find -src=... -base=... -export=...(将查询结果导出成指定路径下的txt文件中)
  ### 改名
  add_tail -src=... -tail=...  -base=...  
  add_head -src=... -head=...  -base=...
  ### 拷贝
  copy -src=... -dst=...(这里指目标的文件夹)  
  copydir -src=... -dst=...(这里指目标的文件夹)
  ###  剪切
  move -src=... -dst=...(这里指目标文件夹)  
  movedir -src=... -dst=...(这里指目标文件夹)
  ###  删除
  delete -src=...  
  deletedir -src=...  

## 2.压缩包

  ### 列举压缩包下一级的所有文件(包括文件夹)
  findzip -src=... -base=...  -export=将所有文件名称导出到目标txt中
  ### 打包压缩
  package -src=... -dst=...
  ### 解压
  unpackage -src=... -dst=...

## 3.exe文件
  
  ### 调用exe，并将缓冲区中的信息打印或者保存到指定txt文件中(Python、Java、C#版本)  
# 二、依赖库
    pip install shutilwhich
    pip install glob3
    pip install click


# 三、运行方式(Windows)
----------
   ## 1.普通文件模块(fileop.py)和压缩包模块(zipfileop.py)
      以fileop.py为例:
      在对应的文件目录下进入，dos输入:  python fileop.py 命令名  -参数名1=参数值1  -参数名2=参数值2  ......  
----------    
  ## 2.exe模块
  -------------
  ## (1)exe输出结果的处理方式解释说明  
    enum ExeProcessorType {
      //打印  按行打印  
      PRINT,
      //导出  导出到指定的txt文件中  
      EXPORT,
      //其他  按照自定义方式对取得的字符串在源码中进行操作即可  
      OTHERS
    } 
  ---------------------
  ### (2)Python版本(定义和样例说明见exeop.py)使用
      在自己的调用函数中声明并调用:
      调用对象名=CustomExeProcessor(threadID=线程号,name=子线程名,exepPath=exe完整路径,
                                 argv=[传入参数1,传入参数2，...,传入参数n]，type=输出结果的处理方式,export=缓冲需要保存到txt文件中，这里要填完整的txt文件路径名,
                                 ,parallel=True(默认选择的是和主线程并行的方式调用exe))  
      调用对象名.execute()  
----------------      
   ### (3)Java版本(定义和样例说明见ExeProcessorPlus.java)使用
   #### 方式一:
    在自己的调用函数中声明并调用:  
    
    //设置参数  
    ExeProcessorPlus exeProcessorPlus=new ExeProcessorPlus();  
    //传参信息  
    Vector<String> argvs=new Vector<String>();  
    argvs.add(参数1);    
    ...  
    argvs.add(参数n);  
    //开始执行  
    exeProcessorPlus.executeRun(可执行文件的路径名, argvs,type=输出结果的处理方式,export=缓冲需要保存到txt文件中，这里要填完整的txt文件路径名,
                                 ,parallel=True(默认选择的是和主线程并行的方式调用exe));  
                                 
   #### 方式二(只针对Windows系统下的局部exe调用方式，具体见.java文件中的main函数):  
    在自己的调用函数中声明并调用:  
    
    ExeProcessorPlus exeProcessorPlus=new ExeProcessorPlus();  
    //设置前置命令
    Vector<String> prefixGroups=new Vector<String>();
    prefixGroups.add(前置命令1);
    ...
    prefixGroups.add(前置命令n);
    
    //目标的exe路径
    String exePath=目标的exe路径;
    
    //设置参数
    Vector<String> argvs = new Vector<String>();
    argvs.add(参数1);    
    ...  
    argvs.add(参数n);  

    exeProcessorPlus.executeRunForWindows(前置命令组,可执行文件的路径名, argvs,type=输出结果的处理方式,export=缓冲需要保存到txt文件中，这里要填完整的txt文件路径名,
                                 ,parallel=True(默认选择的是和主线程并行的方式调用exe));

   ----------------      
   ### (4)C#版本(定义和样例说明见ExeProcessorPlus.cs)使用
   #### 方式一:
    在自己的调用函数中声明并调用:  
    
    //设置参数  
    ExeProcessorPlus exeProcessorPlus=new ExeProcessorPlus();  
    //传参信息  
    List<String> argvs=new List<String>();  
    argvs.Add(参数1);    
    ...  
    argvs.Add(参数n);  
    //开始执行  
    exeProcessorPlus.executeRun(可执行文件的路径名, argvs,type=输出结果的处理方式,export=缓冲需要保存到txt文件中，这里要填完整的txt文件路径名,
                                 ,parallel=True(默认选择的是和主线程并行的方式调用exe));  
                                 
   #### 方式二(只针对Windows系统下的局部exe调用方式，具体见.cs文件中的main函数):  
    在自己的调用函数中声明并调用:  
    
    ExeProcessorPlus exeProcessorPlus=new ExeProcessorPlus();  
    //设置前置命令
    List<String> prefixGroups=new List<String>();
    prefixGroups.Add(前置命令1);
    ...
    prefixGroups.Add(前置命令n);
    
    //目标的exe路径
    String exePath=目标的exe路径;
    
    //设置参数
    List<String> argvs = new List<String>();
    argvs.Add(参数1);    
    ...  
    argvs.Add(参数n);  

    exeProcessorPlus.executeRunForWindows(前置命令组,可执行文件的路径名, argvs,type=输出结果的处理方式,export=缓冲需要保存到txt文件中，这里要填完整的txt文件路径名,
                                 ,parallel=True(默认选择的是和主线程并行的方式调用exe));
