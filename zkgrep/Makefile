CLASSPATH=libs/log4j-1.2.15.jar:libs/zookeeper-3.3.3.jar

ZkGrep.class : ZkGrep.java 
	javac ZkGrep.java -cp $(CLASSPATH)

test : ZkGrep.class
	java -cp $(CLASSPATH):. ZkGrep 

clean: 
	rm -f *.class *~
