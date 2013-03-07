CLASSPATH=libs/log4j-1.2.15.jar:libs/zookeeper-3.3.3.jar

test : ZkGrep.class
	java -cp $(CLASSPATH):. ZkGrep localhost

ZkGrep.class : ZkGrep.java 
	javac ZkGrep.java -cp $(CLASSPATH)

clean: 
	rm -f *.class *~
