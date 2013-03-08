import org.apache.zookeeper.*;
import org.apache.zookeeper.data.*;
import org.apache.log4j.* ; 
import java.util.HashSet; 
import java.nio.ByteBuffer; 
import java.nio.ByteOrder; 
import java.util.regex.Pattern;
import java.util.regex.Matcher;



      /**
       * Zkgrep finds out what you are looking for 
       */

public class ZkGrep implements Watcher 
{
    static private ZooKeeper zk = null; 
    static private Logger logger = Logger.getLogger(ZkGrep.class);
    static { 
        try { 
            BasicConfigurator.configure();
            Logger.getLogger("org.apache.zookeeper").setLevel((Level) Level.ERROR);
            logger.removeAllAppenders() ; 
            logger.setLevel((Level) Level.ERROR); 
            logger.addAppender( new FileAppender(new SimpleLayout(), "/tmp/ZkGrep.log") ) ;
        } catch(Exception ex) {
            ex.printStackTrace(); 
        } 
    }

          // what are we looking for? 
    private Pattern pattern; 
    private String regex; 

          // keep track of zk paths we visited 
    private final HashSet<String> visited = new HashSet<String> () ; 

          // keep track of timestamps (in ms) in order to decide when to back off
    private long startTs = System.currentTimeMillis() ; 
    private long endTs = 0 ;
    private long recentLatency = 80 ; 
    final private long minLatency = 80 ; 
    final private double ALPHA = 0.8 ; 

    protected void backOff() throws InterruptedException { 
        Thread.sleep(minLatency + recentLatency * 2) ; 
        startTs = System.currentTimeMillis() ; 
        logger.debug( "times = " + startTs ) ; 
    } 


    protected void emitIfNeeded(String path, String data) { 
        if( pattern == null ) 
            System.out.println( path + "\t" + data ) ; 
        else { 
                  //System.out.println( "matching " + path + " to " + regex ) ; 
            Matcher matcher = pattern.matcher(path);
            if (matcher.find())
                System.out.println( path + "\t" + data ) ; 
        }  
    } 


    public void process(WatchedEvent evt) {   
        endTs = System.currentTimeMillis() ;
        logger.debug( "times = " + startTs + " to " + endTs + " recent = " + recentLatency ) ;
        recentLatency = (long) ( ALPHA * recentLatency + (1-ALPHA) * (endTs - startTs) ) ;   
        logger.debug( "new latency " + recentLatency ) ;
    } 


    public void traverse(String path) throws Exception { 
        logger.info( "Entering " + path ) ; 
        visited.add(path) ; 

        backOff() ; 
        Stat status = zk.exists(path, false); 
        if(status == null) 
            return ; 

        byte[] data = zk.getData(path, false, status) ;  
        if( data != null ) {
            String datastr = new String(data); 
            emitIfNeeded( path, datastr ) ; 
            logger.debug( "path=" + path + " data=" + datastr + " of length " + status.getDataLength() );
        }

        for( String child : zk.getChildren(path, false) ) {     
            String fullpath = path + "/" + child ; 
            if( !visited.contains( fullpath ) ) {
                traverse(fullpath); 
            } 
        }
        return; 
    }
    

    public ZkGrep(String _regex) {
        regex = _regex ;
        if( regex != null ) { 
            pattern = Pattern.compile(regex);
            logger.debug( "compiled pattern " + regex ) ; 
        }
    }


    public static void main(String [] args) {
        try { 
            String server = args[0] ; 
            String regextosearch = null ; 
            if( args.length > 1 )  
                regextosearch = args[1] ; 
            ZkGrep g = new ZkGrep(regextosearch) ; 
            zk = new ZooKeeper(server, 60000, g ) ;
            g.traverse("/consumers") ; 

        } catch( Exception ex ) {
            ex.printStackTrace(); 
        }
    }    
}   
