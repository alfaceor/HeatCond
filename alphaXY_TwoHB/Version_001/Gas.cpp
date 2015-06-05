#include "Gas.h"

int indx(int i, int j){
  return (i*DIM+j);
};

Gas::Gas(int const N, double alpha){
	this->N = N;
  this->theta = new double[N];
  this->omega = new double[N];
  
  this->vec_m = new double[N*DIM];
  this->vec_M = new double[DIM];
  this->force = new double[N];
  
  this->Ek_n = new double[N];
  this->Ek =0.0;
  this->Ep =0.0;
  
  this->vec_flux = new double[N];
  this->Flux = 0.0;
	
  this->alpha = alpha;
  this->inv_ijalpha = new double[N];
  this->calculateInvIJalpha();
  this->Ntilde = N;
  this->calculateNtilde();
  cout<<"Ntilde = "<< this->Ntilde<<endl; 
  
};

Gas::~Gas(){
  delete[] theta;
  delete[] omega;
  delete[] vec_M;
  delete[] vec_m;
  delete[] force;
  delete[] vec_flux;
};

void Gas::initCoord(){
  double pi=3.14159;
  for (int i=0; i<this->N ; i++){
    this->theta[i]=(2.0*(i+0.5)/(this->N) -1 )*pi ;
  }
};

void Gas::initVeloc(){
  for (int i=0; i<this->N ; i++){
    this->omega[i]=0.0;
  }
};

void Gas::initCoord2(){
  for (int i=0; i<this->N ; i++){
    this->theta[i]=0.0;
  }
};

void Gas::initCoord3(){
  //TODO:RANDOM POSITIONS
	const gsl_rng_type *T; T = gsl_rng_default;
  gsl_rng *r; r = gsl_rng_alloc(T);
  long unsigned int seed;
  seed = (long unsigned int) time(NULL); // Get the time of the system as seed
  gsl_rng_set(r,seed);
  
  for (int i=0; i<this->N ; i++){
    //this->theta[i]=(2*gsl_rng_uniform (r)-1)*M_PI;
    this->theta[i]=2.0*gsl_rng_uniform (r)*M_PI;
  }
  gsl_rng_free (r);
};


// alpha stuffs
void Gas::calculateNtilde(){  // depend of on the value of \alpha
//  calculateInvIJalpha();
  Ntilde =0.0;
  for (int i=0; i<N-1; i++){
    Ntilde += inv_ijalpha[i];
  }
}  
void Gas::calculateInvIJalpha(){  // r_{i,j}^\alpha = |i-j|^\alpha
  cout<<" inv_ijalpha[delta_ij] "<<endl;
  this->inv_ijalpha[0] = 0.0;
  cout<<inv_ijalpha[0]<<endl;
  for (int delta_ij=1; delta_ij<N; delta_ij++){
    this->inv_ijalpha[delta_ij] = 1.0/pow(fabs(delta_ij), alpha);
    cout<<inv_ijalpha[delta_ij]<<" ";
  }
  cout<<endl;
  cout<<"***************"<<endl;
}


// TODO: Read initial conditions from file
bool Gas::initCondFromFile(string filename){
	struct stat buffer;   
	// Check if file exist
  if (stat (filename.c_str(), &buffer) != 0){
//    cout<<filename+" doesn't Exist!"<<endl;
    return false;
  }else{
    ifstream iniCondFile;
	  iniCondFile.open(filename.c_str()); //"xxxxxx.ini"
	  string line;
	  getline(iniCondFile,line);
//	  cout<<line<<endl;
	  stringstream linestream(line);
	  string key;
	  getline(linestream,key,' ');
	  double time=atof(key.c_str());
    int i=0;
    while( getline(linestream,key,' ') ){
      this->omega[i] = atof(key.c_str());
      getline(linestream,key,' ');
      this->theta[i] = atof(key.c_str());
      i++;
    }

    if(i>this->N or i<this->N){
      cout<<"Caralho! Deu merda! o numero de particulas nao coincide! FDP"<<endl;
    }

	  iniCondFile.close();
    return true;
  }

}

void Gas::initVeloc2(double Temp){
	// TODO: Make a gaussian random distribution (with momentum =0)
	double sqrtTemp = sqrt(Temp);
	const gsl_rng_type *T; T = gsl_rng_default;
  gsl_rng *r; r = gsl_rng_alloc(T);
  long unsigned int seed;
  seed = 100;//(long unsigned int) time(NULL); // Get the time of the system as seed
  gsl_rng_set(r,seed);
  
  double omega_mean=0.0;
  for (int i=0; i<this->N; i++){
    this->omega[i] = sqrtTemp*gsl_ran_gaussian(r, 1);
    omega_mean+= this->omega[i];
  }
  omega_mean = omega_mean/this->N;
  
  for (int i=0; i<this->N; i++){
    this->omega[i] = this->omega[i]-omega_mean;
  }
  
  this->calculateEkin();
//  cout<<this->Ek<<endl;
  double TempFactor=sqrt(0.5*this->N*Temp/this->Ek);
//  cout<<TempFactor<<endl;
  for (int i=0; i<this->N; i++){
    this->omega[i] = TempFactor*this->omega[i];
  }
  gsl_rng_free (r);
}


// Calculate functions
void Gas::calculateVec_m(){
  for (int i=0; i< this->N; i++){
    this->vec_m[indx(i,0)] = cos(this->theta[i]);
    this->vec_m[indx(i,1)] = sin(this->theta[i]);
  }
}

void Gas::calculateVec_M(){
  this->vec_M[0]=0;
  this->vec_M[1]=0;
  for (int i=0; i<this->N; i++){
    this->vec_M[0] += this->vec_m[indx(i,0)];
    this->vec_M[1] += this->vec_m[indx(i,1)];
  }

  this->vec_M[0] = this->vec_M[0]/this->N;
  this->vec_M[1] = this->vec_M[1]/this->N;
//  cout<<this->vec_M[0]<<" "<<this->vec_M[1]<<endl;
}

void Gas::calculateForce(double eps){
  for (int i=0; i<this->N; i++){
    this->force[i] = -1.0*eps*( this->vec_m[indx(i,1)]*this->vec_M[0] - this->vec_m[indx(i,0)]*this->vec_M[1] );
  }
}

/*
 First neighboors
 */
void Gas::calculateForceFNB(double eps){
  
  force[0] = -1.0*eps*( 
              -vec_m[indx(1,1)]*vec_m[indx(0,0)] + vec_m[indx(1,0)]*vec_m[indx(0,1)]
              );
  for (int i=1; i<N-1; i++){
    force[i] = -1.0*eps*( 
              -vec_m[indx(i+1,1)]*vec_m[indx(i  ,0)] + vec_m[indx(i+1,0)]*vec_m[indx(i  ,1)]
              +vec_m[indx(i  ,1)]*vec_m[indx(i-1,0)] - vec_m[indx(i  ,0)]*vec_m[indx(i-1,1)]
              );
  }
  force[N-1] = -1.0*eps*( 
              +vec_m[indx(N-1,1)]*vec_m[indx(N-2,0)] - vec_m[indx(N-1,0)]*vec_m[indx(N-2,1)]
              );
}

void Gas::calculateForceAlpha(double eps){
  double sinthetaij=0.0;
  for (int i=0; i<N; i++){
    force[i] = 0.0;
    for (int j=0; j<i; j++){
//        sinthetaij = sin(theta[i]-theta[j]); 
        sinthetaij = vec_m[indx(i,1)]*vec_m[indx(j,0)] - vec_m[indx(i,0)]*vec_m[indx(j,1)];
        force[i] += -sinthetaij*inv_ijalpha[abs(i-j)];
    }
    
    
    for (int j=i+1; j<N; j++){
//        sinthetaij = sin(theta[i]-theta[j]); 
        sinthetaij = vec_m[indx(i,1)]*vec_m[indx(j,0)] - vec_m[indx(i,0)]*vec_m[indx(j,1)];
        force[i] += -sinthetaij*inv_ijalpha[abs(i-j)];
    }
    
    force[i] = eps*force[i]/Ntilde;
//    cout<<"force["<<i<<"]="<<force[i]<<endl;
  }
//  cout<<"-----"<<endl;
}

// Heat reservatories
void Gas::addHeatBathTo(int partID, double Temp, double dt, double gamma, gsl_rng *r){

  double factor=sqrt(2*Temp*dt);
  gamma=1.0; // FIXME
  double randomgauss=gsl_ran_gaussian(r, 1);
  cout<<"FORCE"<<endl;
  cout<<this->force[partID]<<endl;
  this->force[partID] += -gamma*this->omega[partID];
  cout<<this->force[partID]<<endl;
  this->force[partID] += factor*randomgauss;
  cout<<this->force[partID]<<endl;
//  cout<<randomgauss<<endl;
  
}


// Energy
void Gas::calculateEkin_n(){
  for (int i=0; i<N; i++){
		this->Ek_n[i]= 0.5*this->omega[i]*this->omega[i];
	}
}

void Gas::calculateEkin(){
	this->Ek=0.0;
	for (int i=0; i<this->N; i++){
		this->Ek += this->Ek_n[i];
	}
}

void Gas::calculateEpot(double eps){
	this->Ep=0.0;
  double M2 = this->vec_M[0]*this->vec_M[0] +this->vec_M[1]*this->vec_M[1];
	this->Ep = (eps*this->N/2.0)*(1-M2);
}

void Gas::calculateEpotFNB(double eps){
	Ep=0.0;
  for (int i=0; i<N-1; i++){
    Ep += eps*(
            1.0 -(vec_m[indx(i+1,0)]*vec_m[indx(i,0)] + vec_m[indx(i+1,1)]*vec_m[indx(i,1)])
            );
  }
}

void Gas::calculateEpotAlpha(double eps){
  Ep = 0.0;
  for (int i=0; i<N; i++){
    for (int j=0; j<i; j++){
      Ep += (1.0 -(vec_m[indx(i,0)]*vec_m[indx(j,0)] + vec_m[indx(i,1)]*vec_m[indx(j,1)]))*inv_ijalpha[abs(i-j)];
    }
  }
  Ep = eps*Ep/Ntilde;
}

void Gas::calculateVec_flux(double eps, int i){
  vec_flux[i] = 0.0;
  double sinthetaij = 0.0;
  double f_ij =0.0;
  for (int j=0; j<i; j++){
      sinthetaij = vec_m[indx(i,1)]*vec_m[indx(j,0)] - vec_m[indx(i,0)]*vec_m[indx(j,1)];
      f_ij = -(eps/Ntilde)*sinthetaij*inv_ijalpha[abs(i-j)];
      vec_flux[i] += 0.5*f_ij*(omega[i] + omega[j]);
//      vec_flux[i] = 0.5*(omega[i]+omega[j])*f_ij;
  }

}

void Gas::calculateFlux(){
  // TODO: Mean vec_flux over particles.
  Flux=0.0; // j_{l,l-1}
  
//  Flux = 0.5*(omega[0])*(force);
  
//  for (int i=0; i<N; i++){
//    Flux += vec_flux[i];
//  }
//  Flux = Flux/N;
}

// Update functions
void Gas::updateCoord(Gas* oldgas, double dt, double dt2, HeatBath* hb1, HeatBath* hb2){
	// Left reservatory.
  if(hb1->KT==0.0){
    this->updateCoordWhitoutHBTo(0, oldgas, dt, dt2);
  }else{
    this->updateCoordHBLangevinTo(0, oldgas, dt, dt2, hb1);
//    cout<<"----"<<hb1->KT<<endl;
  }
  // Without heat bath particles.
  for (int i=1; i<this->N-1; i++){
    this->updateCoordWhitoutHBTo(i, oldgas, dt, dt2);
  }
  // Right reservatory
  if(hb2->KT==0.0){
    this->updateCoordWhitoutHBTo(N-1, oldgas, dt, dt2);
  }else{
    this->updateCoordHBLangevinTo(N-1, oldgas, dt, dt2, hb2);
  }
}

void Gas::updateCoordHBLangevinTo(int part_id, Gas* oldgas, double dt, double dt2, HeatBath* hb){
  this->theta[part_id] = oldgas->theta[part_id]
        + hb->c[1]*oldgas->omega[part_id]*dt
        + hb->c[2]*dt2*oldgas->force[part_id]
        + hb->drG;  
}

void Gas::updateCoordWhitoutHBTo(int part_id, Gas* oldgas, double dt, double dt2){
  this->theta[part_id] = oldgas->theta[part_id]
        + oldgas->omega[part_id]*dt
        + 0.5*dt2*oldgas->force[part_id];
}

void Gas::removeCyclesCoord(){
  double twoM_PI = 2.0*M_PI;
  for (int i=0; i<this->N; i++){
    if (this->theta[i]< 0)
      this->theta[i] = fmod(this->theta[i],twoM_PI)+twoM_PI;
    else
      this->theta[i] = fmod(this->theta[i],twoM_PI);
  }
}


void Gas::updateVeloc(Gas* oldgas, double dt, HeatBath* hb1, HeatBath* hb2){
	// Left reservatory.
  if(hb1->KT==0.0){
    this->updateVelocWhitoutHBTo(0, oldgas, dt);
  }else{
    this->updateVelocHBLangevinTo(0, oldgas, dt, hb1);
  }
  // Without heat bath particles.
  for (int i=1; i<this->N-1; i++){
    this->updateVelocWhitoutHBTo(i, oldgas, dt);
  }
  // Right reservatory
  if(hb2->KT==0.0){
    this->updateVelocWhitoutHBTo(N-1, oldgas, dt);
  }else{
    this->updateVelocHBLangevinTo(N-1, oldgas, dt, hb2);
  }
}

void Gas::updateVelocHBLangevinTo(int part_id, Gas* oldgas, double dt, HeatBath* hb){

  this->omega[part_id] = hb->c[0]*oldgas->omega[part_id]
        + dt*( 
            (hb->c[1]-hb->c[2])*oldgas->force[part_id]
            + hb->c[2]*this->force[part_id]
        )
        + hb->dvG;
}

void Gas::updateVelocWhitoutHBTo(int part_id, Gas* oldgas, double dt){
  this->omega[part_id]=oldgas->omega[part_id]
        + 0.5*dt*(this->force[part_id]+oldgas->force[part_id]);
}

// Save data to file
void Gas::writeMacroState(ofstream *ptrfile, int ttime, double dt, int partID){
	(*ptrfile) << dt*ttime<<" ";
	(*ptrfile) << this->Ek << " ";
	(*ptrfile) << this->Ep << " ";
	(*ptrfile) << this->vec_M[0] << " ";
	(*ptrfile) << this->vec_M[1] << " ";
  (*ptrfile) << this->vec_flux[partID] << " ";
	(*ptrfile) << endl;
}

void Gas::writeMicroState(ofstream *ptrfile, int ttime, double dt){
	(*ptrfile) << dt*ttime<<" ";
	for (int i =0; i<this->N; i++){
		(*ptrfile) << this->omega[i] << " ";
		(*ptrfile) << this->theta[i] << " ";	
	}
	(*ptrfile) << endl;
}

// print functions
void Gas::printCoord(){
	for (int i=0; i<this->N ; i++){
    cout<<this->theta[i]<<" ";
  }
  cout<<endl;
}

void Gas::printVeloc(){
  for (int i=0; i<this->N ; i++){
    cout << this->omega[i]<<" ";
  }
  cout<<endl;
}

void Gas::printVec_m(){
  cout<<"_____ Begin printVec_m() "<<endl;
  for (int i=0; i< this->N; i++){
  	cout<< this->vec_m[indx(i,0)]<< ", " << this->vec_m[indx(i,1)] <<endl;
  }
  cout<<"_____ End printVec_m() "<<endl;
}

void Gas::printVec_M(){
  cout<<"_____ Begin printVec_M() "<<endl;
	cout<< this->vec_M[0]<< ", " << this->vec_M[1] <<endl;
  cout<<"_____ End printVec_M() "<<endl;
}

void Gas::printForce(){
	for (int i=0; i<this->N; i++){
		cout<< this->force[i] <<endl;
	}
}

