#include "IOParams.h"

IOParams::IOParams(int argc, char **argv){
  
  // 0. Boost options initialize.

  // Declare a group of options that will be 
  // allowed only on command line
  po::options_description generic("Generic options");
  generic.add_options()
      ("version,v", "print version string")
      ("help", "produce help message")
      ("config,c", po::value<string>(&prmfilename)->default_value("InputParams.prm"),
            "name of a file of a configuration.")
      ;
      
  // Declare a group of options that will be 
  // allowed both on command line and in
  // config file
  po::options_description config("Configuration");
  config.add_options()
    ("Npart,N", 
         po::value< string >(&strN)->default_value("0000000002"), 
         "Number of particles")
    ("U0,u", 
         po::value< string >(&strU0)->default_value("1.00"), 
         "Total Energy of the system without reservatories.")
    ("T1,1", 
         po::value< string >(&strT1)->default_value("0.00"), 
         "Temperature reservoir 1")     
    ("T2,2", 
         po::value< string >(&strT2)->default_value("0.00"), 
         "Temperature reservoir 2")     
    ("job_id,j", 
         po::value< string >(&strJob_id)->default_value("00000"), 
         "id of the job (trial)") 
    ("eps", 
         po::value< double >(&eps)->default_value(1.0), 
         "epsilon (interaction coefficient)")
    ("gamma1", 
         po::value< double >(&gamma1)->default_value(1.0), 
         "viscosity constant for the reservatory 1")
    ("gamma2", 
         po::value< double >(&gamma2)->default_value(1.0), 
         "viscosity constant for the reservatory 2")
    ("total_time", 
         po::value< int >(&total_time)->default_value(1000), 
         "simulation time steps.")
    ("timeDim", 
         po::value< int >(&timeDim)->default_value(10), 
         "save value every [timeDim] steps.")
    ("dt", 
         po::value< double >(&dt)->default_value(0.001), 
         "dt for the numerical integration.")
    ("alpha,A", 
         po::value< string >(&strAlpha)->default_value("0.00"), 
         "dt for the numerical integration.")
    ("partID_flux,i", 
         po::value< int >(&partID_flux)->default_value(3), 
         "The id of the particle to get the flux.")
    ("printTVR", 
         po::value< int >(&printTVR)->default_value(0), 
         "save trajectories in .tvr file 0=false(don't print), 1=true (print).")
      ;
        
  
  po::options_description cmdline_options;
  cmdline_options.add(generic).add(config);

  po::options_description config_file_options;
  config_file_options.add(config);
      
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).
              options(cmdline_options).run(), vm);
  po::notify(vm);
  
  strAlpha="INFT";
  this->basename="N_"+strN+"__U0_"+strU0+"__T1_"+strT1+"__T2_"+strT2+"__A_"+strAlpha+"__id_"+strJob_id;
  
  ifstream ifs(prmfilename.c_str());
  if (!ifs)
  {   
      cout << "----Warning!----: can not open config file: " << prmfilename << " Hard core default options are set."<<endl;
//      return 0;
  }   
  else
  {   
      po::store(po::parse_config_file(ifs, config_file_options), vm);
      po::notify(vm);
  }
  
  // Convert to corresponding type.
  if (vm.count("Npart")) {
    cout << "Npart = ";
    cout << vm["Npart"].as< string >() << "=";
    N=atoi(vm["Npart"].as< string >().c_str());
    cout << N <<endl;
  }
  if (vm.count("U0")) {
    cout << "U0 = ";
    cout << vm["U0"].as< string >() << "=";
    U0=atof(vm["U0"].as< string >().c_str());
    cout << U0 <<endl;
  }
  if (vm.count("T1")) {
    cout << "T1 = ";
    cout << vm["T1"].as< string >() << "=";
    T1=atof(vm["T1"].as< string >().c_str());
    cout << T1 <<endl;
  }
  if (vm.count("T2")) {
    cout << "T2 = ";
    cout << vm["T2"].as< string >() << "=";
    T2=atof(vm["T2"].as< string >().c_str());
    cout << T2 <<endl;
  }
  if (vm.count("job_id")) {
    cout << "job_id = ";
    cout << vm["job_id"].as< string >() << "=";
    job_id=atoi(vm["job_id"].as< string >().c_str());
    cout << job_id <<endl;
  }
  if (vm.count("alpha")) {
    cout << "alpha = ";
    cout << vm["alpha"].as< string >() << "=";
    alpha=atof(vm["alpha"].as< string >().c_str());
    cout << alpha <<endl;
  }
  
  
//  basename="N_"+strN+"__U0_"+strU0+"__T1_"+strT1+"__T2_"+strT2+"__id_"+strJob_id;
  
  cout<< this->basename <<endl;
  this->inifilename  = this->basename+".ini";
  this->outfilename  = this->basename+".dat";
  this->outfilename2 = this->basename+".tvr";
  this->outfilename3 = this->basename+".end";
  this->outfilename4 = this->basename+".Tpt";
  

  this->ttime = 0;
  cout<< "timeDim = " << this->timeDim <<endl;
  if (this->total_time > this->timeDim){
  	this->taux = (this->total_time)/this->timeDim;
  }else{
  	this->taux = 1;
  }

  this->dt2 = this->dt * this->dt;
  cout<<"dt2 = "<<this->dt2<<endl;
  

}

IOParams::~IOParams(){

}
