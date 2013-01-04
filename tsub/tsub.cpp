/**
 * author: vivek pathak
 * licence : apache 2; see http://www.apache.org/licenses/LICENSE-2.0.html
 */

#include <ctype.h>
#include <stdio.h>
#include <iostream>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>


#define NAMELEN      (1024)
#define LINE_BUF_SIZ (64*1024)


const int ts = 4;
char * inbuf;
char * outbuf;


using namespace std; 


int getnextts(int currpos)
{
   if( currpos%ts == 0 )
      return currpos + ts;
   return currpos + ts - (currpos%ts);
}


void trim(char * line)
{
   int len = strlen(line);

   char * e = line + len - 1;
   char * p = e;

   while(isspace(*p) && p >= line)
      p--;

   if(p < e)
      p[1] = 0;
}



bool reformat(char * infile, char * outfile)
{
   FILE * in = fopen( infile, "r" ) ;
   FILE * out = fopen( outfile , "w" ) ;
   if(!in || !out)
   {
      cerr << "Failed to open files " << infile << " or " << outfile << endl ;
      if(in)
         fclose(in) ;
      if(out)
         fclose(out) ;
      return -1;
   }

   memset( inbuf, 0, LINE_BUF_SIZ );
   while( fgets( inbuf, LINE_BUF_SIZ, in ) != NULL )
   {
      int linesz = strlen(inbuf);
      int i = 0;
      int lastpos = 0;
      int currpos = 0;

      memset( outbuf, 0, LINE_BUF_SIZ );
      for( ; i < linesz ; )
      {
         lastpos = currpos;
         while(inbuf[i] && isspace(inbuf[i]))
         {
            if( inbuf[i] == '\t' )
               currpos = getnextts(currpos);
            else
               currpos++;
            i++;
         }
         if((currpos - lastpos) > 2*ts)
         {
            if((currpos%ts))
               currpos = getnextts(currpos);
            while(lastpos < currpos)
               outbuf[lastpos++] = ' ' ;
         }
         else
         {
            while(lastpos < currpos)
               outbuf[lastpos++] = ' ' ;
         }
         while(inbuf[i] && !isspace(inbuf[i]))
         {
            outbuf[currpos] = inbuf[i];
            i++;
            currpos++;
         }
      }
      trim(outbuf);
      fprintf( out, "%s\n", outbuf );
   }
   fclose(in) ;
   fclose(out) ;
   return 0;
}

int copy(char * from, char * to)
{
   FILE * fpto = fopen(to, "w" );
   FILE * fpfrom = fopen(from , "r" ) ;

   if(!fpto || !fpfrom)
   {
      cerr << "Cannot open files " << to << " or " << from << endl;
      return -1;
   }

   int c;
   while( EOF != (c = fgetc(fpfrom)))
      fputc(c, fpto) ;
   fclose(fpto) ;
   fclose(fpfrom) ;
   return 0;
}


void tempfilename( char * buf)
{
   static int seed = 0;
   if(!seed)
      srand(seed = getpid());
   sprintf( buf, "%s%d" , "/tmp/tsub_f_" , rand()) ;
}

int main( int argc, char * argv[] )
{
   if( argc == 1 )
   {
      cerr << "Usage " << argv[0] << " Files to untabify" << endl;
      return -1;
   }

   inbuf = new char  [LINE_BUF_SIZ + 128];
   outbuf = new char  [LINE_BUF_SIZ + 128];
   if(!inbuf || !outbuf)
   {
      cerr << "No memory" << endl;
      return -2;
   }


   for( int i = 1; i < argc; i++ )
   {
      char tempf1[NAMELEN] , tempf2[NAMELEN] ;

      tempfilename(tempf1) ;
      tempfilename(tempf2) ;

      cout << "Converting " << argv[i] << " using tempfiles f1=" << tempf1 <<
         " and f2=" << tempf2 << endl ;

      if(copy(argv[i], tempf1) || reformat(tempf1, tempf2) || copy(tempf2,argv[i]))
            cerr << "Error in converting file " << argv[i]
                  << "check temporary files for recovery" << endl ;
   }

   delete inbuf;
   delete outbuf;
   return 0;
}
