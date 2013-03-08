import org.apache.zookeeper.*;
import org.apache.zookeeper.data.*;
import org.apache.log4j.* ; 
import java.util.HashSet; 
import java.nio.ByteBuffer; 
import java.nio.ByteOrder; 



      /**
       * Zkgrep finds out what you are looking for 
       */

public class ZkGrep implements Watcher {
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

    private final HashSet<String> visited = new HashSet<String> () ; 

    public void process(WatchedEvent evt) { 
    } 

    public void traverse(String path) throws Exception { 
        System.out.println( "Entered " + path ) ; 

        visited.add(path) ; 

        Stat status = zk.exists(path, false); 
        byte[] data = zk.getData(path, false, status) ;  
        if(status == null) 
            return ; 

        if( data != null ) {
            System.out.println( "path=" + path + " data=" + new String(data) + " of length " + status.getDataLength());
        }

        for( String child : zk.getChildren(path, false) ) {     
            String fullpath = path + "/" + child ; 
            if( !visited.contains( fullpath ) ) {
                Thread.sleep(1000); 
                traverse(fullpath); 
            } 
        }
        return; 

    }
    

    public static void main(String [] args) {
        try { 
            String server = "localhost" ; 
            if( args.length > 0 )
                server = args[0] ;

            zk = new ZooKeeper(server, 60000, null ) ;
            ZkGrep g = new ZkGrep() ; 
            System.out.println( "Started!!!" ) ;
            g.traverse("/consumers") ; 
        } catch( Exception ex ) {
            ex.printStackTrace(); 
        }
    }    
}   
