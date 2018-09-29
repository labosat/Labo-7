#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    double a, b, c = 0;
    int N = 18980;
    int folders = 7;
    std::vector<double> R;
    std::vector<double> dR;
    std::ifstream ifs1;
    std::ifstream ifs2;
    std::ifstream ifs3;
    ifs1.open("R_auto.txt");
    ifs2.open("Rerr_auto.txt");
    
    std::string home_path = "/home/lucas/Desktop/Facultad/Labo7/Codigos/wait time";

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
            
    std::ofstream ofs;
    ofs.open("data.txt");
    ofs << "N\tRq\tdRq\twait time\n";
    
    std::vector<double> wait_time = {0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001};
    
    for (int j = 1; j <= folders; j++)
    {
        std::string path = "/data/1e-" + std::to_string(j) + "/iv/";
        std::string ext = ".txt";
        std::vector<double> Rq_temp;
        std::vector<double> Rq_err_temp;
        
        for (int k = 1; k <= 15; k++)
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
    
        double Rq = 0;
        double Rq_err = 0;
        for (int l = 0; l < Rq_temp.size(); l++)
        {
            Rq += Rq_temp[l];
            Rq_err += pow(Rq_err_temp[l], 2);
        }
    
        ofs << std::to_string(j) << "\t" << Rq/15 << "\t" << sqrt(Rq_err)/15 << "\t" << wait_time[j - 1] << "\n";
        
    }      
            
            
    ofs.close();

    
    return 0;
}
