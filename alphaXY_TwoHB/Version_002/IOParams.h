#include <stdlib.h>

#include <iostream>
#include <fstream>
#include <sstream>

#include <string>

#include <boost/program_options.hpp>
namespace po = boost::program_options;

using namespace std;

class IOParams{
  public:
    // input parameters
    int N;
    double U0;
    double T1;
    double T2;
    int total_time;
    double eps;
    double gamma1;
    double gamma2;
    int job_id;
    double alpha;
    int partID_flux;
    
    //var to name the file
    string strN;
    string strU0;
    string strT1;
    string strT2;
    string strJob_id; // job_id
    string strAlpha;
    

    string prmfilename; //Default parameters file
        
    string basename;        
    string inifilename;
    
    // output variables
    string outfilename;
    string outfilename2;
    string outfilename3;
    string outfilename4;
    
    // auxiliar variables
    int ttime;
    int timeDim;
    int taux;
    double dt;
    double dt2;  
    
    
    IOParams(int argc, char **argv);
    bool existInifile();
    ~IOParams();
    
};
