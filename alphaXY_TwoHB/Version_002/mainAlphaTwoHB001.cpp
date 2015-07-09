#include <stdio.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <string>
#include <gsl/gsl_math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>

#include "IOParams.h"
#include "Gas.h"
#include "HeatBath.h"


using namespace std;
int main(int argc, char **argv){
  IOParams io(argc, argv);
  srand (time(NULL)*io.job_id);
  long unsigned int seed01_1=rand(), seed01_2=rand();
  long unsigned int seed02_1=rand(), seed02_2=rand();
  double mass=1.0;
  cout<<"seeds = "<< seed01_1<<" "<< seed01_2<<" "<< seed02_1<<" "<< seed02_2<<" " <<endl;
  HeatBath hb01(mass, io.gamma1, io.T1, io.dt, io.dt2, seed01_1, seed01_2);
  HeatBath hb02(mass, io.gamma2, io.T2, io.dt, io.dt2, seed02_1, seed02_2);
  
  hb01.RollTheDice();
  hb02.RollTheDice();
  
  Gas g_old(io.N, io.alpha);
  Gas g_new(io.N, io.alpha);
  
  // Initiate angles and velocities.
	if( !g_old.initCondFromFile(io.inifilename) ){
    cout<<io.inifilename<<" is missing!"<<endl;
    cout<<"fail!"<<endl;
    return EXIT_FAILURE;
  }
  if( !g_new.initCondFromFile(io.inifilename) ){
    cout<<io.inifilename<<" is missing!"<<endl;
    cout<<"fail!"<<endl;
    return EXIT_FAILURE;
  }
  
//  g_old.calculateInvIJalpha();
//  g_new.calculateInvIJalpha();
  
  g_old.calculateNtilde();
  g_new.calculateNtilde();

	
  ofstream ofile, ofile2;
  ofile.open((io.outfilename).c_str());
  ofile2.open((io.outfilename2).c_str()); 
	
  /**** ----------- Begin simulation   ----------- ****/
  
  // Begin Time Mean
  double *MeanTimeEk_n = new double[io.N];
  int time_mean;
  
  // Initiate MeanTimeEk_n
  for(int i=0; i<io.N; i++){ MeanTimeEk_n[i] = 0.0; }; time_mean=0;

	// 1. Calculate ___force_old___.
	g_old.calculateVec_m();	  			//--  1.1 Calculate m_old.
	g_old.calculateVec_M();					//--  1.2 Calculate M_old.  
	g_old.calculateForceAlpha3(io.eps);		//--  1.3 Calculate force_old with M_old

  
//  for (int i=0; i<io.N; i++)
//    cout<< g_old.force[i]<<endl;

  while (io.ttime < io.total_time){
  	if (io.ttime % 2 == 0){		
			// 1. Calculate ___force_old___.
			// XXX: Was calculated in a previous step
			
			// 2. Calculate ___theta_new___
      hb01.RollTheDice();
      hb02.RollTheDice();
      
			g_new.updateCoord( &g_old, io.dt, io.dt2, &hb01, &hb02);
			g_new.removeCyclesCoord();
				 
			// 3. Calculate ___force_new___
			g_new.calculateVec_m();					//--  3.1 Calculate m_new
			g_new.calculateVec_M();					//--  3.2 Calculate M_new
			g_new.calculateForceAlpha3(io.eps);		//--  3.3 Calculate force_new with M_new
				
			// 4. Calculate ___omega_new___
			g_new.updateVeloc(&g_old, io.dt, &hb01, &hb02);
      
  
      
			if (io.ttime % io.taux == 0){
				// Calculate system energy.
        g_old.calculateEkin_n();
				g_old.calculateEkin();
				g_old.calculateEpotAlpha2(io.eps);
//				g_old.calculateEpot(io.eps);
        g_old.calculateVec_flux2(io.eps, io.partID_flux);
//        g_old.calculateFlux();

        // Calculate kinetic energy mean
        for(int i=0; i<io.N; i++){ MeanTimeEk_n[i] += g_old.Ek_n[i];  }; time_mean++;
        
        // 5. Calculate ___flux_new___
        
				// Save data.	
				g_old.writeMacroState(&ofile, io.ttime, io.dt, io.partID_flux);
				g_old.writeMicroState(&ofile2, io.ttime, io.dt);
			}
		// -------------- End EVEN	---------------------------
  	}else{
  		// XXX: WARNING this is an INTERCHANGE
  		// 1. Calculate ___force_old___.
			// XXX: was calculated in the previous step
			
			// 2. Calculate ___theta_new___
      hb01.RollTheDice();
      hb02.RollTheDice();
			g_old.updateCoord(&g_new, io.dt, io.dt2, &hb01, &hb02);		
			g_old.removeCyclesCoord();
				 
			// 3. Calculate ___force_new___
			g_old.calculateVec_m();					//--  3.1 Calculate m_new
			g_old.calculateVec_M();					//--  3.2 Calculate M_new
			g_old.calculateForceAlpha3(io.eps);		//--  3.3 Calculate force_new with M_new
      
//			g_old.calculateForce(io.eps);		//--  3.3 Calculate force_new with M_new
				
			// 4. Calculate ___omega_new___
			g_old.updateVeloc(&g_new, io.dt, &hb01, &hb02);
			
			
			if (io.ttime % io.taux == 0){
				// Calculate system energy.
        g_new.calculateEkin_n();
				g_new.calculateEkin();
				g_new.calculateEpotAlpha2(io.eps);
//				g_new.calculateEpot(io.eps);
        g_new.calculateVec_flux(io.eps, io.partID_flux);
//        g_new.calculateFlux();
        
        // Calculate kinetic energy mean
        for(int i=0; i<io.N; i++){ MeanTimeEk_n[i] += g_new.Ek_n[i];  }; time_mean++;
        
        // 5. Calculate ___flux_new___
        
				// Save data.	
				g_new.writeMacroState(&ofile, io.ttime, io.dt, io.partID_flux);
				g_new.writeMicroState(&ofile2, io.ttime, io.dt);
			}
			
		// -------------- End ODD	---------------------------
  	}
  	io.ttime++;
  }
  cout<<endl;
  // End Time Mean
  for(int i=0; i<io.N; i++){ MeanTimeEk_n[i] = MeanTimeEk_n[i]/time_mean; }

  /****----------- End simulation   ----------- ****/  
	ofile.close();
  ofile2.close();
  
  ofstream ofile3, ofile4;
	ofile3.open((io.outfilename3).c_str());
  ofile4.open((io.outfilename4).c_str());
  for(int i=0; i<io.N; i++){ 
    // Temperature profile over time
    ofile4<<i<<" "<<2.0*MeanTimeEk_n[i]<<endl;
  }
  

  
	g_new.writeMicroState(&ofile3, io.ttime, io.dt);  
  ofile3.close();
  ofile4.close();
  cout<<"REALIZATION END!!! "<<io.outfilename3<<endl;
  return EXIT_SUCCESS;
}

