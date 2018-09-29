#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    TApplication *myApp = new TApplication("myApp", &argc, argv , 0, -1);

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
    ofs << "N\tVbr\tdVbr\tR\tdR\tp2\tdp2\n";
    //ofs << "V\tI\tdV\tdI\n";
    
//test starts here
    
//     std::vector<double> V, V2;
//     std::vector<double> I, I2;
//                 
//     Load("/home/lucas/Desktop/Facultad/Labo7/Codigos/vbr estacionario/data/Estacionario 7/iv/27 (iv).txt", V2, I2);
//     Load("/home/lucas/Desktop/Facultad/Labo7/Codigos/vbr estacionario/test_v.txt", V);
//     Load("/home/lucas/Desktop/Facultad/Labo7/Codigos/vbr estacionario/test_i.txt", I);
//     
//                 
//     //V is in Volts and A is in Amperes. Beware if not using optimal range (program will select optimal range)
//     std::vector<std::string> ranges = DetermineRange(V2, I2);
//                 
//     std::vector<double> V_err = SourceError(V2, 'V', ranges[0]);
//     std::vector<double> I_err = MeasureError(I2, 'I', ranges[1]);
//                 
//                 
//     LogData(I2, I_err);
//     DeriveData2(V, I, V_err, I_err);
//     
//     //int degree = 7;
//     //Smooth(V, I, V_err, I_err);
//     
//     TCanvas* canvas = new TCanvas("canvas", "canvas", 700, 700);
//     canvas->SetGrid();
//     
// 
//     TGraphErrors* graph_s = new TGraphErrors(V.size(), &V[0], &I[0], &V_err[0], &I_err[0]);
//     graph_s->SetMarkerColor(kBlack);
// 	graph_s->SetMarkerStyle(25);
//     //TF1* function3 = new TF1("Vbr", "[0]/(x - [1])", 25, 30);
//     
//     graph_s->Draw("ap");
//     
//     int index_max = FindMaxIndex(I);
//                 
//     Reverse(V, I);
//     Reverse(V_err, I_err);
//                 
//     for (int i = 0; i < index_max; i++)
//     {
//         V.pop_back();
//         I.pop_back();
//         V_err.pop_back();
//         I_err.pop_back();
//     }
//                 
//     Reverse(V, I);
//     Reverse(V_err, I_err);
//                 
//     std::vector<double> chi2;
//     std::vector<double> pvalue;
//                 
//     std::vector<double> breakdown;
//     std::vector<double> breakdown_err;
//     std::vector<double> numerator;
//     std::vector<double> numerator_err;
//     int parameters = 2;
//                 
//                 
//     //n determines how much points are removed from the maximum side of the data to get a better fit 
//     int n = 5;
//     for (int j = 0; j < n; j++)
//     {
//         std::vector<double> V_temp;
//         std::vector<double> I_temp;
//         std::vector<double> V_temp_err;
//         std::vector<double> I_temp_err;
//         for (int k = 0; k < V.size(); k++)
//         {
//             V_temp.push_back(V[k]);
//             V_temp_err.push_back(V_err[k]);
//             I_temp.push_back(I[k]);
//             I_temp_err.push_back(I_err[k]);
//         }
//         
//         
//         int end = V.size() - 1;
//         
//         for (int i = 0; i < end; i++)
//         {
//             if (i != 0)
//             {
//                 V_temp.pop_back();
//                 I_temp.pop_back();
//                 V_temp_err.pop_back();
//                 I_temp_err.pop_back();
//             }
//             
//             TGraphErrors* graph = new TGraphErrors(V_temp.size(), &V_temp[0], &I_temp[0], &V_temp_err[0], &I_temp_err[0]);
//             TF1* function = new TF1("Vbr", "[0]/(x - [1])", V_temp[0], 30.1);
//             //function->SetParameters(2, 25);
//             
//             TFitResultPtr r = graph->Fit(function, "S");
//             Double_t x2 = r->Chi2(); // to retrieve the fit chi2
//             Double_t pval = r->Prob(); //to retrieve pvalue
//             Double_t m = r->Parameter(1);
//             Double_t m_err = r->ParError(1);
//             Double_t p0 = r->Parameter(0);
//             Double_t p0_err = r->ParError(0);
//             int ndf = V_temp.size() - parameters;		
//             
//             chi2.push_back(x2/ndf);
//             pvalue.push_back(pval);	
//             
//             breakdown.push_back(m);
//             breakdown_err.push_back(m_err);
//             numerator.push_back(p0);
//             numerator_err.push_back(p0_err);
//             
//             delete graph;
//         }
//         
//         Reverse(V, I);
//         Reverse(V_err, I_err);
//         V.pop_back();
//         I.pop_back();
//         V_err.pop_back();
//         I_err.pop_back();
//         Reverse(V, I);
//         Reverse(V_err, I_err);
//         
//     }
//     
//     double result = FindClosestToOne(chi2);    
//     std::cout << breakdown[result];
//  
//     myApp->Run();

    
    for (int j = 14; j <= folders; j++)
    {
        std::string path = "/data/Estacionario " + std::to_string(j) + "/iv/";
        std::vector<double> Vbr_temp;
        std::vector<double> Vbr_err_temp;
        std::vector<double> p2_temp;
        std::vector<double> p2_err_temp;
        
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
                
                std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
                std::vector<double> I_err = MultiRangeError(I);
                
                
                LogData(I, I_err);
                DeriveData2(V, I, V_err, I_err);
                
                
                int index_max = FindMaxIndex(I);
                
                Reverse(V, I);
                Reverse(V_err, I_err);
                
                for (int i = 0; i < index_max; i++)
                {
                    V.pop_back();
                    I.pop_back();
                    V_err.pop_back();
                    I_err.pop_back();
                }
                
                Reverse(V, I);
                Reverse(V_err, I_err);
                
                std::vector<double> chi2;
                std::vector<double> pvalue;
                
                std::vector<double> breakdown;
                std::vector<double> breakdown_err;
                std::vector<double> numerator;
                std::vector<double> numerator_err;
                int parameters = 2;
                
                
                //n determines how much points are removed from the maximum side of the data to get a better fit 
                int n = 5;
                for (int j = 0; j < n; j++)
                {
                    std::vector<double> V_temp;
                    std::vector<double> I_temp;
                    std::vector<double> V_temp_err;
                    std::vector<double> I_temp_err;
                    for (int k = 0; k < V.size(); k++)
                    {
                        V_temp.push_back(V[k]);
                        V_temp_err.push_back(V_err[k]);
                        I_temp.push_back(I[k]);
                        I_temp_err.push_back(I_err[k]);
                    }
                    
                    
                    int end = V.size() - 1;
                    
                    for (int i = 0; i < end; i++)
                    {
                        if (i != 0)
                        {
                            V_temp.pop_back();
                            I_temp.pop_back();
                            V_temp_err.pop_back();
                            I_temp_err.pop_back();
                        }
                        
                        TGraphErrors* graph = new TGraphErrors(V_temp.size(), &V_temp[0], &I_temp[0], &V_temp_err[0], &I_temp_err[0]);
                        TF1* function = new TF1("Vbr", "[0]/(x - [1])", V_temp[0], 30.1);
                        //function->SetParameters(2, 25);
                        
                        TFitResultPtr r = graph->Fit(function, "S");
                        Double_t x2 = r->Chi2(); // to retrieve the fit chi2
                        Double_t pval = r->Prob(); //to retrieve pvalue
                        Double_t m = r->Parameter(1);
                        Double_t m_err = r->ParError(1);
                        Double_t p0 = r->Parameter(0);
                        Double_t p0_err = r->ParError(0);
                        int ndf = V_temp.size() - parameters;		
                        
                        chi2.push_back(x2/ndf);
                        pvalue.push_back(pval);	
                        
                        breakdown.push_back(m);
                        breakdown_err.push_back(m_err);
                        numerator.push_back(p0);
                        numerator_err.push_back(p0_err);
                        
                        delete graph;
                    }
                    
                    Reverse(V, I);
                    Reverse(V_err, I_err);
                    V.pop_back();
                    I.pop_back();
                    V_err.pop_back();
                    I_err.pop_back();
                    Reverse(V, I);
                    Reverse(V_err, I_err);
                    
                }
                
                double result = FindClosestToOne(chi2);    
                Vbr_temp.push_back(breakdown[result]);
                Vbr_err_temp.push_back(breakdown_err[result]);    
                p2_temp.push_back(numerator[result]);
                p2_err_temp.push_back(numerator_err[result]);
            }
            
        }
        
        double Vbr = 0;
        double Vbr_err = 0;
        double p2 = 0;
        double p2_err = 0;
        for (int l = 0; l < Vbr_temp.size(); l++)
        {
            Vbr += Vbr_temp[l];
            Vbr_err += Vbr_err_temp[l];
            p2 += p2_temp[l];
            p2_err += p2_err_temp[l];
        }
    
        ofs << std::to_string(j) << "\t" << Vbr/(permitted_indeces.size()) << "\t" << Vbr_err/(permitted_indeces.size()) << "\t" << R[j - 1] << "\t" << dR[j - 1] << "\t" << p2/(permitted_indeces.size()) << "\t" << p2_err/(permitted_indeces.size()) << "\n";
        
                
    }
    
    ofs.close();
    
    return 0;
}
