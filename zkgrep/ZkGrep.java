import org.apache.zookeeper.*;
import org.apache.zookeeper.data.*;
import org.apache.log4j.* ; 
//import org.apache.log4j.BasicConfigurator;

       /**
	* Zkgrep finds out what you are looking for 
	*/

public class ZkGrep implements Watcher {

    static Logger logger = Logger.getLogger(ZkGrep.class);
    static Appender appender = new ConsoleAppender(new SimpleLayout()); 
    static { 
	logger.addAppender(appender); 
    }
    public void process(WatchedEvent evt) { 
	System.out.println( "event done " + evt ) ; 
    }

    public static void main(String [] args) {
	try { 
	    BasicConfigurator.configure();
	 
		
	    ZooKeeper z = new ZooKeeper(args[0], 60000, new ZkGrep() ) ;
	    System.out.println( "Started!!!" ) ;
	} catch( Exception ex ) {
	    ex.printStackTrace(); 
	}
    } 
} 
