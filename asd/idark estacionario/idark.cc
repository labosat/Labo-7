#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    double a, b, c = 0;
    int N = 18980;
    int folders = 18;
    std::vector<double> R;
    std::vector<double> dR;
    std::ifstream ifs1;
    std::ifstream ifs2;
    std::ifstream ifs3;
    ifs1.open("R.txt");
    ifs2.open("Rerr.txt");
    
    //MAKE SURE 30 IS INCLUDED IN MEASUREMENT! (USUALLY MEASUREMENT IS DONE UP T0 29.9)
    double polarizationV = 30;
    
    std::vector<std::vector<int>> filtered_indeces;
    
    std::string home_path = "/home/lucas/Desktop/Facultad/Labo7/Codigos/vbr estacionario";
    
    std::vector<int> num_measurements_iv = {50, 59, 41, 50, 50, 50, 50, 50, 50, 50, 50, 50, 26, 50, 50, 50, 50, 50};

    if (ifs1.is_open())
    {
        while(!(ifs1 >> a) == 0)
        {
            R.push_back(a);
                
        }
        ifs1.close();
    }
    
        
    if (ifs2.is_open())
    {
        while(!(ifs2 >> b) == 0)
        {
            dR.push_back(b);
        }
        
        ifs2.close();
    }
    
    for(int k = 1; k <= folders; k++)
    {
        ifs3.open(home_path + "/index/array " + std::to_string(k) + ".txt");
        int c = 0;
        std::vector<int> temp;
        filtered_indeces.push_back(temp);
        if (ifs3.is_open())
        {
            while(!(ifs3 >> c) == 0)
            {
                filtered_indeces[k - 1].push_back(c);
            }
            
            ifs3.close();
        }
        
    }       
            
    std::ofstream ofs;
    ofs.open("data.txt");
    ofs << "N\tIdark\tdIdark\tR\tdR\n";
    
    for (int j = 1; j <= folders; j++)
    {
        std::string path = "/data/Estacionario " + std::to_string(j) + "/iv/";
        std::vector<double> Idark_temp;
        std::vector<double> Idark_err_temp;
        
        std::vector<int> permitted_indeces = filtered_indeces[j - 1];
    
        for (int k = 1; k <= num_measurements_iv[j - 1]; k++)
        {
            if (ElementInVector(k, permitted_indeces))
            {
                std::string s = std::to_string(k) + " (iv).txt";
                
                std::vector<double> V;
                std::vector<double> I;
                
                Load(home_path + path + s, V, I);
                
                //V is in Volts and A is in Amperes. Beware if not using optimal range (program will select optimal range)
                std::vector<std::string> ranges = DetermineRange(V, I);
                
                //std::cout << ranges[1];
                
                std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
                std::vector<double> I_err = MultiRangeError(I);
                
                int index = IndexInVector(polarizationV, V);
            
                Idark_temp.push_back(I[index]);
                Idark_err_temp.push_back(I_err[index]);
                
            }
            
        }
        
        double Idark = 0;
        double Idark_err = 0;
        for (int l = 0; l < Idark_temp.size(); l++)
        {
            Idark += Idark_temp[l];
            Idark_err += Idark_err_temp[l];
        }
    
        ofs << std::to_string(j) << "\t" << Idark/(permitted_indeces.size()) << "\t" << Idark_err/(permitted_indeces.size()) << "\t" << R[j - 1] << "\t" << dR[j - 1] << "\n";
    }
    
    ofs.close();
    
    return 0;
}
