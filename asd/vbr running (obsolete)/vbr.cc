#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    double a,b = 0
    //number of measurements
    int N = 30;
    
    std::string path = "./data/";
    std::string ext = ".txt";
    
    std::ofstream ofs;
    ofs.open("data.txt")
    ofs >> "N\tVbr\tdVbr\tR\tdR\tchi2\tp-value\n"; 
    
    std::vector<double> R;
    std::vector<double> dR;
    std::ifstream ifs1;
    std::ifstream ifs2;
    ifs1.open("R.txt");
    ifs2.open("Rerr.txt");
    
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
    
    
    for (int i = 1; i <= N; i++)
    {
        std::vector<double> V;
        std::vector<double> I;
        std::string s = std::to_string(i);

        Load(path + s + ext, V, I);
    
        //V is in Volts and A is in Amperes
        std::vector<std::string> ranges = DetermineRange(V, I);

        std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
        std::vector<double> I_err = MeasureError(I, 'I', ranges[1]);

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
    
        //total datapoints before recursive fitting
        int datapoints = V.size();
    
        //Recursive fitting section--------------------------------------------------------
	
        std::vector<double> chi2;
        std::vector<double> pvalue;
    
        //the iterator1 vector is used to "label" each chi2 with an int number of the iteration in which the chi2 was calculated
        //this permits us to determine the first point used in the fit (labeled by the iteration number j)
        std::vector<int> iterator1;
    
        //the iterator2 vector is analogous to iterator1, but lets us know what is the fit upper bound
        std::vector<int> iterator2;
    
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
                TF1* function = new TF1("Vbr", "[0]/(x - [1])", V_temp[0], 30);

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
            
                iterator1.push_back(j);
                iterator2.push_back(datapoints - i);
            
                delete graph;
            }
        
            V_temp.clear();
            I_temp.clear();
            V_temp_err.clear();
            I_temp_err.clear();
        
            Reverse(V, I);
            Reverse(V_err, I_err);
            V.pop_back();
            I.pop_back();
            V_err.pop_back();
            I_err.pop_back();
            Reverse(V, I);
            Reverse(V_err, I_err);

        }   
	
        //---------------------------------------------------------------------------------
        //---------------------------------------------------------------------------------
    
         double result = FindClosestToOne(chi2);
//         std::cout << std::endl << std::endl;
//         std::cout << "Fit performed between index " << iterator1[result] << " (" << iterator1[result] << " point/s after maximum) and "     << iterator2[result] << " for a total of " << iterator2[result] - iterator1[result] << " points. For reference, there are " <<  datapoints << " points between first (maximum) and final measurement" << std::endl;
//         std::cout << "chi2: " << chi2[result] << ", " << "p-value: " << pvalue[result] << std::endl; 
//         std::cout << "auto ranges: " << ranges[0] << " and " << ranges[1] << std::endl;
//         std::cout << "T = " << parse<double>(T[0]) << " \pm " << parse<double>(T[1]) << " ºC" << std::endl;
//         std::cout << "Vbr = " << breakdown[result] << " \pm " << breakdown_err[result] << std::endl;
//         std::cout << "p0 = " << numerator[result] << " \pm " << numerator_err[result] << std::endl;
        
        ofs << std::to_string(i) << "\t" << breakdown[result] << "\t" << breakdown_err[result] << "\t" << R[i - 1] << "\t" << dR[i - 1] << "\t" << chi2[result] << "\t" << pvalue[result] << "\n";
        
    }
    ofs.close()
    
    
//     std::string path = "./data/";
//     std::string s = argv[1];
//     std::string ch = argv[2];
//     std::vector<std::string> T = SeparateStrings(s);
// 
//     std::vector<double> V;
//     std::vector<double> I;
//     	
//     Load(path + s, V, I);
//     
//     //V is in Volts and A is in Amperes
//     std::vector<std::string> ranges = DetermineRange(V, I);
// 
//     std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
//     std::vector<double> I_err = MeasureError(I, 'I', ranges[1]);
// 
//     LogData(I, I_err);
//     DeriveData2(V, I, V_err, I_err);
//     
//     
//     //determines dynamically if signal is "rough" and smoothes it if it is
//     //int degree = RoughnessDegree(I);
//     
//     int degree = 0;
//     
//     Smooth(V, I, V_err, I_err, degree);
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
//     //total datapoints before recursive fitting
//     int datapoints = V.size();
//     
//     //Recursive fitting section--------------------------------------------------------
// 	
// 	std::vector<double> chi2;
// 	std::vector<double> pvalue;
//     
//     //the iterator1 vector is used to "label" each chi2 with an int number of the iteration in which the chi2 was calculated
//     //this permits us to determine the first point used in the fit (labeled by the iteration number j)
//     std::vector<int> iterator1;
//     
//     //the iterator2 vector is analogous to iterator1, but lets us know what is the fit upper bound
//     std::vector<int> iterator2;
//     
//     std::vector<double> breakdown;
//     std::vector<double> breakdown_err;
//     std::vector<double> numerator;
//     std::vector<double> numerator_err;
// 	int parameters = 2;
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
//             TF1* function = new TF1("Vbr", "[0]/(x - [1])", V_temp[0], 30);
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
//             iterator1.push_back(j);
//             iterator2.push_back(datapoints - i);
//             
//             delete graph;
//         }
//         
//         V_temp.clear();
//         I_temp.clear();
//         V_temp_err.clear();
//         I_temp_err.clear();
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
// 	}   
// 	
//     //---------------------------------------------------------------------------------
//     //---------------------------------------------------------------------------------
// 
//     double result = FindClosestToOne(chi2);
//     std::cout << std::endl << std::endl;
//     std::cout << "Fit performed between index " << iterator1[result] << " (" << iterator1[result] << " point/s after maximum) and " << iterator2[result] << " for a total of " << iterator2[result] - iterator1[result] << " points. For reference, there are " << datapoints << " points between first (maximum) and final measurement" << std::endl;
//     std::cout << "chi2: " << chi2[result] << ", " << "p-value: " << pvalue[result] << std::endl; 
//     std::cout << "auto ranges: " << ranges[0] << " and " << ranges[1] << std::endl;
//     std::cout << "T = " << parse<double>(T[0]) << " \pm " << parse<double>(T[1]) << " ºC" << std::endl;
// 	std::cout << "Vbr = " << breakdown[result] << " \pm " << breakdown_err[result] << std::endl;
// 	std::cout << "p0 = " << numerator[result] << " \pm " << numerator_err[result] << std::endl;
    
//     if (ch == "y")
//     {
//         TApplication *myApp = new TApplication("myApp", &argc, argv , 0, -1);
// 
//         std::vector<double> V_graph;
//         std::vector<double> I_graph;
// 
//         Load(path + s, V_graph, I_graph);
//     
//         std::vector<std::string> ranges = DetermineRange(V_graph, I_graph);
//         std::vector<double> V_graph_err = SourceError(V_graph, 'V', ranges[0]);
//         std::vector<double> I_graph_err = MeasureError(I_graph, 'I', ranges[1]);
// 
//         LogData(I_graph, I_graph_err);
//         DeriveData2(V_graph, I_graph, V_graph_err, I_graph_err);
//         Smooth(V_graph, I_graph, V_graph_err, I_graph_err, degree);
//     
//         gStyle->SetOptFit(1111); 
//         TCanvas* c = new TCanvas("vbr", "vbr", 700, 600);
//        
//         c->SetGrid();
//     
//         TMultiGraph* mg = new TMultiGraph();
// 
//         TGraphErrors* graph2 = new TGraphErrors(V_graph.size(), &V_graph[0], &I_graph[0], &V_graph_err[0], &I_graph_err[0]);
//         graph2->SetMarkerColor(kBlack);
//         graph2->SetMarkerStyle(25);
//     	graph2->SetTitle("Mediciones");
// 
//         mg->Add(graph2);
// 
//         mg->SetTitle("Curva de I(V) con SiPM en inversa; Tension [V]; Corriente [A]");
// 
//         mg->Draw("ap");
// 
//         //Graphic Tweaks-------------------------------------------------------------------
// 
//         mg->GetXaxis()->SetTitleSize(0.042);
//         mg->GetYaxis()->SetTitleSize(0.042);
//         mg->GetXaxis()->SetLabelSize(0.045);
//         mg->GetYaxis()->SetLabelSize(0.045);
//         mg->GetYaxis()->SetTitleOffset(1);
// 
//         c->BuildLegend();
//         c->Update();
//  
//         c->Modified();
// 
// 
//         //---------------------------------------------------------------------------------
//         //---------------------------------------------------------------------------------
// 
//         myApp->Run();
    }


    return 0;
}
