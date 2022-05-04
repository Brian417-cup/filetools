import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.util.Vector;

public class ExeProcessorPlus{
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
	
	public boolean executeRun(String path, Vector<String> argvs,boolean isParallel) {
		try {
			if (path.contains(" ")) {
				path="\""+path+"\"";
			}
			
			this.setExePath(path);
			this.setCommandStr(argvs);
			String cmdStr=exePath;
			for (int i = 0; i < argvs.size(); i++) {
				cmdStr=cmdStr+" "+argvs.get(i);
			}
			
			System.out.println(cmdStr);
			
			this.process = Runtime.getRuntime().exec(cmdStr);
			
			if (!isParallel) {
				this.process.waitFor();	
			}
			
			
			 // 向管道中输入数据
	        /*new Thread() {
	            public void run() {
	                OutputStream stdin = process.getOutputStream();
	                for (int i = 0; stdin!=null ; i++) {
	                    try {
	                        Thread.sleep(1);   // 要休息片刻才看得到 I/O 的缓存效果。
	                        stdin.write((i + " " + i + "\n").getBytes());
	                    } catch (Exception ex) {
	                        ex.printStackTrace();
	                    }
	                }
	            }
	        }.start();*/
			
	        // 从管道中读出输出信息
			new Thread() {
				public void run() {
					BufferedReader stdOut = new BufferedReader(new InputStreamReader(process.getInputStream()));
			        try {
						for (String line; null != (line = stdOut.readLine()); )
						    System.out.println(line);
					} catch (IOException e) {
						// TODO 自动生成的 catch 块
						e.printStackTrace();
					}		
				};
			}.start();
	        
	    
			//从管道中读错误信息
			new Thread() {
				public void run() {
					BufferedReader stdError = new BufferedReader(new InputStreamReader(process.getErrorStream()));
			        try {
						for (String line; null != (line = stdError.readLine()); )
						    System.out.println(line);
					} catch (IOException e) {
						// TODO 自动生成的 catch 块
						e.printStackTrace();
					}		
				};
			}.start();
			
		} catch (Exception e) {
			// TODO: handle exception
			return false;
		}
		
		return true;
	}
	

	
	public static void main(String[] args) {
		// TODO 自动生成的方法存根
		ExeProcessorPlus exeProcessorPlus=new ExeProcessorPlus();
		Vector<String> argvs=new Vector<String>();
		argvs.add("123");
		argvs.add("456");
		
		
		exeProcessorPlus.executeRun("./exeDemo/test.exe", argvs,true);
		
		while (true) {
			System.out.println("这是主线程");
		}
	}

}
