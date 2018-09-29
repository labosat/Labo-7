#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    double a, b, c = 0;
    int N = 18980;
    int folders = 12;
    std::vector<double> R;
    std::vector<double> dR;
    std::ifstream ifs1;
    std::ifstream ifs2;
    std::ifstream ifs3;
    ifs1.open("R.txt");
    ifs2.open("Rerr.txt");
    
    std::vector<std::vector<int>> filtered_indeces;
    
    std::string home_path = "/home/lucas/Desktop/Facultad/Labo7/Codigos/rq estacionario";
    
    //sin autorange
    //std::vector<int> num_measurements_iv = {156, 109, 38, 47, 51, 50, 50, 50, 50, 23, 34, 50, 50, 50, 28, 50, 50, 50, 50, 50};
    
    //con autorange
    //std::vector<int> num_measurements_iv = {33, 36, 45, 48, 45, 48, 42, 50, 50, 50, 36, 44, 37, 26, 30, 23, 17, 14, 35};
    
    //mediciones post 40º
    std::vector<int> num_measurements_iv = {42, 24, 26, 25, 34, 26, 21, 20, 17, 30, 19, 19};

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
    ofs << "N\tRq\tdRq\tR\tdR\n";
    
    for (int j = 1; j <= folders; j++)
    {
        std::string path = "/data/Estacionario " + std::to_string(j) + "/iv/";
        std::string ext = ".txt";
        std::vector<double> Rq_temp;
        std::vector<double> Rq_err_temp;
        
        std::vector<int> permitted_indeces = filtered_indeces[j - 1];
        
        for (int k = 1; k <= num_measurements_iv[j - 1]; k++)
        {
            if (ElementInVector(k, permitted_indeces))
            {
                std::string s = std::to_string(k) + " (iv)";
                
                std::vector<double> V;
                std::vector<double> I;
                
                
                Load(home_path + path + s + ext, V, I);
                
                int end = V.size() - 1;
                int datapoints = V.size();
                
                //V is in Volts and A is in Amperes
                std::vector<std::string> ranges = DetermineRange(V, I);
                
                std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
                std::vector<double> I_err = MultiRangeError(I, 'I');
                
                //this ensures that pop_back() in the fitting section removes lower voltage elements first
                //this was done this way because there is no "pop_front()"
                Reverse(V, I);
                
                std::vector<double> chi2;
                std::vector<double> pvalue;
                std::vector<double> slope;
                std::vector<double> slope_err;
                int parameters = 2;
                
                for (int i = 0; i < end; i++)
                {
                    if (i != 0)
                    {
                        V.pop_back();
                        I.pop_back();
                        V_err.pop_back();
                        I_err.pop_back();
                    }
                    
                    TGraphErrors* graph = new TGraphErrors(V.size(), &V[0], &I[0], &V_err[0], &I_err[0]);
                    TFitResultPtr r = graph->Fit("pol1", "S");
                    Double_t x2 = r->Chi2(); // to retrieve the fit chi2
                    Double_t pval = r->Prob(); //to retrieve pvalue
                    Double_t m = r->Parameter(1);
                    Double_t m_err = r->ParError(1);
                    int ndf = V.size() - parameters;		
                    
                    chi2.push_back(x2/ndf);
                    pvalue.push_back(pval);
                    slope.push_back(m);
                    slope_err.push_back(m_err);
                    delete graph;
                }
                
                double result = FindClosestToOne(chi2);
                Rq_temp.push_back(N/(slope[result]));
                Rq_err_temp.push_back((N*slope_err[result])/(pow(slope[result], 2)));
            }
        }
    
        double Rq = 0;
        double Rq_err = 0;
        for (int l = 0; l < Rq_temp.size(); l++)
        {
            Rq += Rq_temp[l];
            Rq_err += pow(Rq_err_temp[l], 2);
        }
    
        ofs << std::to_string(j) << "\t" << Rq/(permitted_indeces.size()) << "\t" << sqrt(Rq_err)/(permitted_indeces.size()) << "\t" << R[j - 1] << "\t" << dR[j - 1] << "\n";
        
    }      
            
            
    ofs.close();

    
    return 0;
}
