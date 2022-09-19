#!/bin/bash 
pushd ~
for dir in research code misc source system 
do 
	pushd $dir 
	echo working on $(pwd)
	svn -q status 
	svn update 
	popd 
done 
popd
