using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Diagnostics;
using System.IO;

namespace ExeProcessor
{
    public enum ExeProcessorType
    {
        PRINT, EXPORT, OTHERS
    }


    class ExeProcessorPlus
    {

        //Windows进入cmd命令专用
        public static String CMD_INTRICATOR = "cmd.exe ";
        //Windows系统单次多条命令顺序执行连接符
        public static String EXE_INTRICATOR_SEPERATE = " & ";


        //Exe的路径设置
        private String exePath="";

        public String ExePath
        {
            get { return exePath; }
            set { exePath = value; }
        }

        private Process process = null;

        //传入参数
        private List<String> argvs=null;
        public List<String> Argvs
        {
            get { return argvs; }
            set { argvs = value; }
        }

        ExeProcessorPlus()
        {
            ExePath = "";
            process = null;
            if (Argvs!=null)
            {
                Argvs.Clear();
            }
        }

        //对数据的方法判定
        private void dealPipeData(String data, ExeProcessorType type, StreamWriter dstWriter)
        {
            try
            {
                switch (type)
                {
                    case ExeProcessorType.PRINT:
                        Console.WriteLine(data);
                        break;
                    case ExeProcessorType.EXPORT:
                        dstWriter.WriteLine(data);
                        break;
                    case ExeProcessorType.OTHERS:
                        //自定义处理方法


                        break;
                }
            }
            catch (System.Exception ex)
            {
                Console.WriteLine(ex.Data);
            }
        }

        //对输出流和错误流是否与主线程并行的处理方法
        private void internalExecute(ExeProcessorType type, String exportPath, Process exeProcessor)
        {
            try
            {
                StreamWriter dstWriter = null;

                //从管道中输出信息
                if (type == ExeProcessorType.EXPORT)
                {
                    dstWriter = new StreamWriter(exportPath);
                }

                if (dstWriter != null)
                {
                    dstWriter.WriteLine("输出信息");
                    dstWriter.WriteLine();
                }
                else
                {
                    Console.WriteLine("输出信息");
                }

                while (!exeProcessor.StandardOutput.EndOfStream)
                {
                    String line = exeProcessor.StandardOutput.ReadLine();
                    dealPipeData(line, type, dstWriter);
                }

                //从管道中读错误信息
                if (dstWriter != null)
                {
                    dstWriter.WriteLine("错误信息");
                    dstWriter.WriteLine();
                }
                else
                {
                    Console.WriteLine("错误信息");
                }

                while (!exeProcessor.StandardError.EndOfStream)
                {
                    String line = exeProcessor.StandardError.ReadLine();
                    dealPipeData(line, type, dstWriter);
                }

                if (dstWriter != null)
                {
                    dstWriter.Close();
                }
            }
            catch (System.Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }

        private String getArgvStr(List<String> argvs)
        {
            Argvs = argvs;
            String argvStr = "";
            for (int i = 0; i < Argvs.Count; i++)
            {
                argvStr =argvStr+ Argvs[i];
                if (i != Argvs.Count - 1)
                {
                    argvStr = argvStr + " ";
                }
            }
            return argvStr;
        }

        //对外封装的执行exe方法
        public bool executeRun(String path, List<String> argvs, ExeProcessorType type,
            String exportPath,bool isParallel)
        {
            try
            {
                ExePath = path;
                String argvStr = getArgvStr(argvs);

                //输出最终的指令
                Console.WriteLine(ExePath + " " + argvStr);

                //声明Exe调用对象
                Process exeProcessor = new Process();
                //设置Exe路径和输入参数
                exeProcessor.StartInfo.FileName = ExePath;
                exeProcessor.StartInfo.Arguments = argvStr;
                exeProcessor.StartInfo.CreateNoWindow = true;
                exeProcessor.StartInfo.UseShellExecute = false;


                //输出流和错误流设置
                exeProcessor.StartInfo.RedirectStandardOutput = true;
                exeProcessor.StartInfo.RedirectStandardError = true;
                //输入流设置
                exeProcessor.StartInfo.RedirectStandardInput = true;
                //p.StandardInput.AutoFlush = true;

                exeProcessor.Start();

                if (!isParallel)
                {
                    internalExecute(type, exportPath, exeProcessor);
                }
                else
                {
                    Thread parallelThread = new Thread(delegate()
                    {
                        internalExecute(type, exportPath, exeProcessor);
                    });
                    parallelThread.Start();
                }
            }
            catch (System.Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            return true;
        }

        //对外封装的执行exe方法
        public bool executeRunForWindows(List<String> prefixGroup,String path, List<String> argvs, ExeProcessorType type,
            String exportPath, bool isParallel)
        {
            try
            {
                ExePath = path;
                String cmdStr = "";
                foreach (var item in prefixGroup)
                {
                    cmdStr = cmdStr + item + EXE_INTRICATOR_SEPERATE;
                }

                cmdStr=cmdStr+ExePath+" "+getArgvStr(argvs);

                //输出最终的指令
                Console.WriteLine(cmdStr);

                //声明Exe调用对象
                Process exeProcessor = new Process();
                //设置Exe路径和输入参数，这里是要先调用cmd.exe再去把其他的当作传参的
                exeProcessor.StartInfo.FileName = CMD_INTRICATOR;
                exeProcessor.StartInfo.CreateNoWindow = true;
                exeProcessor.StartInfo.UseShellExecute = false;


                //输出流和错误流设置
                exeProcessor.StartInfo.RedirectStandardOutput = true;
                exeProcessor.StartInfo.RedirectStandardError = true;
                //输入流设置
                exeProcessor.StartInfo.RedirectStandardInput = true;
                //p.StandardInput.AutoFlush = true;

                exeProcessor.Start();

                exeProcessor.StandardInput.WriteLine(cmdStr);
                exeProcessor.StandardInput.AutoFlush = true;

                if (!isParallel)
                {
                    internalExecute(type, exportPath, exeProcessor);
                }
                else
                {
                    Thread parallelThread = new Thread(delegate()
                    {
                        internalExecute(type, exportPath, exeProcessor);
                    });
                    parallelThread.Start();
                }
            }
            catch (System.Exception ex)
            {
                Console.WriteLine(ex.Message);
            }

            return true;
        }

        static void Main(string[] args)
        {
            ExeProcessorPlus exeRuntime = new ExeProcessorPlus();
            
            //方式一:直接执行对应的Exe
            List<String> argvs = new List<string>();
            argvs.Add("123");
            argvs.Add("456");
            String exePath="./exeDemo/test.exe";
            exeRuntime.executeRun(exePath, argvs, ExeProcessorType.PRINT, "", true);

            //方式二：切换到对应的环境下再执行对应的EXE(针对Windows系统),为了保证有些局部变量能被正常的使用
            //List<String> prefixGroups = new List<String>();
            //prefixGroups.Add("f:");
            //prefixGroups.Add("cd f:");
            //String exePath = "test.exe";

            //List<String> argvs = new List<String>();
            //argvs.Add("1545446");
            //argvs.Add("5959595");
            //exeRuntime.executeRunForWindows(prefixGroups, exePath, argvs, ExeProcessorType.PRINT, "",true);

            while (true)
            {
                Console.WriteLine("这是主线程");
            }

            Console.ReadLine();
        }
    }
}
