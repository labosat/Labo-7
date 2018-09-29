#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"

int main(int argc, char* argv[])
{
    double a, b = 0;
    
    int measurements = 33;
    
    std::string path = "./data33/";
    std::string ext = ".txt";
    
    std::string temp = " (iv)";
    
    int N = 18980;
    std::ofstream ofs;
    ofs.open("data.txt");
    ofs << "N\tRq\tdRq\tR\tdR\tchi2\tp-value\n";
    
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
    
    std::cout << dR[4];
    
    
    for(int i = 1; i <= measurements; i++)
    {
        std::string s = std::to_string(i);
        std::vector<double> V;
        std::vector<double> I;
        Load(path + s + temp + ext, V, I);
        
        
        int end = V.size() - 1;
        int datapoints = V.size();
    
        //V is in Volts and A is in Amperes
        std::vector<std::string> ranges = DetermineRange(V, I);
   
        std::vector<double> V_err = SourceError(V, 'V', ranges[0]);
        std::vector<double> I_err = MeasureError(I, 'I', ranges[1]);
    
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
//         std::cout << std::endl << std::endl;
//         std::cout << "Fit performed between index " << result << " and " << datapoints << " with " << datapoints - result << " points used" << std::endl;
//         std::cout << "chi2: " << chi2[result] << ", " << "p-value: " << pvalue[result] << std::endl; 
//         std::cout << "auto ranges: " << ranges[0] << " and " << ranges[1] << std::endl;
//         std::cout << "p0 = " << slope[result] << " \pm " << slope_err[result] << std::endl;
//         std::cout << "T = " << parse<double>(T[0]) << " \pm " << parse<double>(T[1]) << " ºC" << std::endl;
//         std::cout << "R = " << (N)/(slope[result]) << " \pm " << (N*slope_err[result])/(pow(slope[result], 2)) << " ohms" << std::endl;
        
        ofs << std::to_string(i) << "\t" << N/(slope[result]) << "\t" << (N*slope_err[result])/(pow(slope[result], 2)) << "\t" << R[i - 1] << "\t" << dR[i - 1] << "\t" << chi2[result] << "\t" << pvalue[result] << "\n";
    
    }
    ofs.close();
    
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
// 	
//         //GRAPHS---------------------------------------------------------------------------
//         //---------------------------------------------------------------------------------
// 
//     
//         gStyle->SetOptFit(1111); 
//         TCanvas* c = new TCanvas("rq", "rq", 700, 600);
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
//         mg->SetTitle("Curva de I(V) con SiPM en directa; Tension [V]; Corriente [mA]");
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
//     }

    //---------------------------------------------------------------------------------
    
    return 0;
}
