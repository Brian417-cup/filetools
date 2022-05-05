import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.Vector;

enum ExeProcessorType {
	PRINT, EXPORT, OTHERS
}

public class ExeProcessorPlus {
	//Windows进入cmd命令专用
	public static String CMD_INTRICATOR = "cmd /c ";
	//Windows系统单次多条命令顺序执行连接符
	public static String EXE_INTRICATOR_SEPERATE = " & ";
	
	
	private String exePath;
	private Process process = null;
	private Vector<String> argvs;

	public String getExePath() {
		return exePath;
	}

	public void setExePath(String exePath) {
		this.exePath = exePath;
	}

	public Vector<String> getCommandStr() {
		return argvs;
	}

	public void setCommandStr(Vector<String> commandStr) {
		this.argvs = commandStr;
	}

	private void dealPipeData(String data, ExeProcessorType type, BufferedWriter writer) {
		try {
			switch (type) {
			case PRINT:
				System.out.println(data);
				break;
			case EXPORT:
				writer.write(data);
				writer.newLine();
				break;
			case OTHERS:
				break;
			}
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}

	private void internalExecute(ExeProcessorType type,String exportPath) {
		try {
			// 内部使用对象，来完成可能的对外txt文件输出
			File dstFile = null;
			FileWriter dstFileWriter = null;
			BufferedWriter dstbWriter = null;

			if (type == ExeProcessorType.EXPORT) {
				dstFile = new File(exportPath);
				dstFile.createNewFile();
				dstFileWriter = new FileWriter(dstFile);
				dstbWriter = new BufferedWriter(dstFileWriter);
			}

			// 从管道中读出输出信息
			if (dstbWriter != null) {
				dstbWriter.write("输出信息");
				dstbWriter.newLine();
				dstbWriter.newLine();
			} else {
				System.out.println("输出信息");
			}
			BufferedReader stdOut = new BufferedReader(new InputStreamReader(process.getInputStream()));

			for (String line; null != (line = stdOut.readLine());)
				dealPipeData(line, type, dstbWriter);

			// 从管道中读错误信息
			if (dstbWriter != null) {
				dstbWriter.write("错误信息");
				dstbWriter.newLine();
				dstbWriter.newLine();
			} else {
				System.out.println("错误信息");
			}

			BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));

			for (String line; null != (line = stdError.readLine());)
				dealPipeData(line, type, dstbWriter);

			if (dstbWriter != null) {
				dstbWriter.close();
			}

			if (dstFileWriter != null) {
				dstFileWriter.close();
			}

			if (stdOut != null) {
				stdOut.close();
			}

			if (stdError != null) {
				stdError.close();
			}

		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}

	public boolean executeRun(String path, Vector<String> argvs, ExeProcessorType type, String exportPath,
			boolean isParallel) {
		try {
			/*if (path.contains(" ")) {
				path = "\"" + path + "\"";
			}*/

			this.setExePath(path);
			this.setCommandStr(argvs);
			String cmdStr = exePath;
			for (int i = 0; i < argvs.size(); i++) {
				cmdStr = cmdStr + " " + argvs.get(i);
			}

			System.out.println(cmdStr);

			this.process = Runtime.getRuntime().exec(cmdStr);

			if (!isParallel) {
				this.process.waitFor();
			}

			// 向管道中输入数据
			/*
			 * new Thread() { public void run() { OutputStream stdin =
			 * process.getOutputStream(); for (int i = 0; stdin!=null ; i++) { try {
			 * Thread.sleep(1); // 要休息片刻才看得到 I/O 的缓存效果。 stdin.write((i + " " + i +
			 * "\n").getBytes()); } catch (Exception ex) { ex.printStackTrace(); } } }
			 * }.start();
			 */
			
			if (isParallel) {
				new Thread() {
					public void run() {
						internalExecute(type, exportPath);
					};
				}.start();
			}
			else {
				internalExecute(type, exportPath);
			}
			

		} catch (Exception e) {
			// TODO: handle exception
			return false;
		}

		return true;
	}

	
	//该函数是Windows专用，为了保证有些exe的环境变量没有配置到全局从而需要逐步切入对应换环境中才能执行
	public boolean executeRunForWindows(Vector<String> prefixGroups,
			String path, Vector<String> argvs, ExeProcessorType type, String exportPath,
			boolean isParallel) {
		try {
			
			this.setExePath(path);
			this.setCommandStr(argvs);
			String cmdStr = "";
			if (prefixGroups.size()!=0) {
				cmdStr=CMD_INTRICATOR;
				
				for (int i = 0; i < prefixGroups.size(); i++) {
					cmdStr=cmdStr+prefixGroups.get(i)+EXE_INTRICATOR_SEPERATE;
				}
			}
			
			cmdStr=cmdStr+exePath;
			
			for (int i = 0; i < argvs.size(); i++) {
				cmdStr = cmdStr + " " + argvs.get(i);
			}

			System.out.println(cmdStr);

			this.process = Runtime.getRuntime().exec(cmdStr);

			if (!isParallel) {
				this.process.waitFor();
			}

			// 向管道中输入数据
			/*
			 * new Thread() { public void run() { OutputStream stdin =
			 * process.getOutputStream(); for (int i = 0; stdin!=null ; i++) { try {
			 * Thread.sleep(1); // 要休息片刻才看得到 I/O 的缓存效果。 stdin.write((i + " " + i +
			 * "\n").getBytes()); } catch (Exception ex) { ex.printStackTrace(); } } }
			 * }.start();
			 */
			
			if (isParallel) {
				new Thread() {
					public void run() {
						internalExecute(type, exportPath);
					};
				}.start();
			}
			else {
				internalExecute(type, exportPath);
			}
			

		} catch (Exception e) {
			// TODO: handle exception
			return false;
		}

		return true;
	}
	
	
	public static void main(String[] args) {
		// TODO 自动生成的方法存根
		ExeProcessorPlus exeProcessorPlus = new ExeProcessorPlus();
		
		
		//方式一:直接执行对应的Exe
		String exePath="./exeDemo/test.exe";
		Vector<String> argvs = new Vector<String>();
		argvs.add("12131");
		argvs.add("456464564");

		exeProcessorPlus.executeRun(exePath, argvs, ExeProcessorType.PRINT, "", true);
		
		//方式二：切换到对应的环境下再执行对应的EXE(针对Windows系统),为了保证有些局部变量能被正常的使用（这里调用的前提是f盘下有exeDemo中的test.exe）
		/*Vector<String> prefixGroups=new Vector<String>();
		prefixGroups.add("f:");
		prefixGroups.add("cd f:");
		String exePath="f:/test.exe";
		
		Vector<String> argvs = new Vector<String>();
		argvs.add("1545446");
		argvs.add("5959595");

		exeProcessorPlus.executeRunForWindows(prefixGroups, exePath, 
				argvs, ExeProcessorType.PRINT, "", true);*/
		
		while (true) {
			System.out.println("这是主线程");
		}
	}

}