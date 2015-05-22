#include <iostream>
#include <fstream>
#include <gsl/gsl_math.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_rng.h>
#include <sstream>

#include <sys/stat.h>

#include "HeatBath.h"

//#include "IOParams.h"
#define DIM 2
#ifndef GAS_H_
#define GAS_H_

using namespace std;

int indx(int , int );
class Gas{
    public:
        int N;
        double *theta;
        double *omega;
        double *vec_m;
        double *vec_M;
        double *force;
        double *Ek_n;
        double Ek;
        double Ep;
        double *vec_flux;
        double Flux;
		
    Gas(int const);
    ~Gas();
    
    void initCoord();
    void initVeloc();
    
    void initCoord2();
    void initVeloc2(double Temp);
    
    void initCoord3();
    bool initCondFromFile(string filename);
    
    // Calculate functions
    void calculateVec_m();
    void calculateVec_M();
    void calculateForce(double eps);
    void calculateForceFNB(double eps);
    
    
    
    // Heat reservatories.
    void addHeatBathTo(int partID, double Temp, double dt, double gamma, gsl_rng *r);
    
    // Energy
    void calculateEkin_n();
    void calculateEkin();
    void calculateEpot(double eps);
    void calculateEpotFNB(double eps);
    void calculateVec_flux();
    void calculateFlux();       // First calculateForce and updateVeloc
    
    // Update functions
    void updateCoord(Gas*, double dt, double dt2, HeatBath* hb1, HeatBath* hb2);
    void updateCoordHBLangevinTo(int part_id, Gas* oldgas, double dt, double dt2, HeatBath* hb);
    void updateCoordWhitoutHBTo(int part_id, Gas* oldgas, double dt, double dt2);
    void removeCyclesCoord();
    
    void updateVeloc(Gas*, double dt, HeatBath* hb1, HeatBath* hb2);
    void updateVelocHBLangevinTo(int part_id, Gas* oldgas, double dt, HeatBath* hb);
    void updateVelocWhitoutHBTo(int part_id, Gas* oldgas, double dt);
    

		// Save data to file
    void writeMacroState(ofstream *ptrfile, int ttime, double dt);
    void writeMicroState(ofstream *ptrfile, int ttime, double dt);
    
    // print functions
    void printCoord();
    void printVeloc();
    void printVec_m();
    void printVec_M();
    void printForce();
};

#endif /* GAS_H_ */