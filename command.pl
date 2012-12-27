#!/usr/bin/perl

my $commandline;
for( $i = 0; $i <= $#ARGV; $i++ )
{
   $commandline = join " ", $ARGV[$i] , $commandline ;
}

while( $server = <STDIN> )
{
   chomp $server;
   $command = "ssh -n $server \"$commandline\"" ;
   print "$command\n";
   system($command);
}

