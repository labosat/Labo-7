#include "/home/lucas/Desktop/Facultad/Labo7/libs/utilities.h"


int main(int argc, char* argv[])
{
	TApplication *myApp = new TApplication("myApp", &argc, argv , 0, -1);

	//DATA LOADING---------------------------------------------------------------------
	//---------------------------------------------------------------------------------

    std::vector<double> T;
	std::vector<double> T_err;
    std::vector<double> Rq;
    std::vector<double> Rq_err;
    
    double mrq = 3.815;
    
    std::ifstream ifs;
    ifs.open("/home/lucas/Desktop/Facultad/Labo7/Codigos/grapher/data_rq_final.txt");
    
    double a, b, c, d, e = 0;
    std::string h, i, j, k, l;
    
    if (ifs.is_open())
    {
        ifs >> h >> i >> j >> k >> l;
        while(!(ifs >> a >> b >> c >> d >> e) == 0)
        {
            T.push_back((d - 1000)/mrq);
            //T.push_back(e);
            T_err.push_back(e/mrq);
            
            Rq.push_back(b);
            //Rq.push_back(a);
            
            Rq_err.push_back(c);
            //Rq_err.push_back(b);
        }
	
	ifs.close();
    }
    
    else
    {
        std::cout << "Could not open specified file." << std::endl;        
    }
    
    for (int i = 0; i < Rq.size(); i++)
    {
        //Rq_err[i] = Rq_err[i];
    }


	//GRAPHS---------------------------------------------------------------------------
	//---------------------------------------------------------------------------------

	gStyle->SetOptFit(1111);
    
	TCanvas* canv = new TCanvas("graph", "graph", 700, 600);
    //canv->SetLogy();
       
	canv->SetGrid();
    
	TMultiGraph* mg = new TMultiGraph();

    TGraphErrors* graph = new TGraphErrors(T.size(), &T[0], &Rq[0], &T_err[0], &Rq_err[0]);
    //TGraphErrors* graph2 = new TGraphErrors(T.size(), &T[0], &Rq[0], &T_err[0], &Rq_err[0]);
    //TGraph* graph = new TGraph(T.size(), &T[0], &Rq[0]);
    
	graph->SetMarkerColor(kBlack);
	graph->SetMarkerStyle(21);
    //graphr->SetMarkerColor(kRed);
    //graphr->SetMarkerStyle(21);
    //graph->SetTitle("Mediciones realizadas a 2^{o} C");

    //Ajuste exponencial Rq
    TF1* function = new TF1("fit", "[0] + [1]*TMath::Exp(-[2]*x)", -40, 40);
    function->SetParameters(460000, 50000, 0.01);
    
    function->SetParLimits(0,470000, 500000);
    function->SetParLimits(1, 15000, 45000);
    function->SetParLimits(2, 0, 0.05);
    
    // Band Gap dependiente de T
    //TF1* function = new TF1("fit", "[0] + [1]*TMath::Exp(pow(x, (-1/[2])))", -40, 40);
    //function->SetParameters(480000, 50000, 3);
    
    //function->SetParLimits(0,470000, 500000);
    //function->SetParLimits(1, 15000, 45000);
    //function->SetParLimits(2, 0, 10);
    
    //TF1* function = new TF1("fit", "[0] + [1]*x", -33, 44);
    //function->SetParameters(0, 0);
    
    //Ajuste iDark
    //TF1* function = new TF1("fit", "1/([0] + [1]*TMath::Exp(-[2]*x))", -40, 40);
    //function->SetParameters(10000, 1000000, 0.1);
    
    //TF1* function2 = new TF1("fit", "[0] + [1]*TMath::Exp(-[2]*x)", -40, 40);
    //function2->SetParameters(0, -1, 0.1);
    

    TFitResultPtr r = graph->Fit(function, "M");
	mg->Add(graph);
    //mg->Add(graphr);
    
    //TFitResultPtr r2 = graph2->Fit(function2, "M");
	//mg->Add(graph2);


	mg->SetTitle("Grafico de la resistencia de quenching en funcion de T con ajuste; Temperatura [^{o}C]; Resistencia [#Omega]");
    //mg->SetTitle("asd; Tiempo de espera [s]; Resistencia [#Omega]");
    
	mg->Draw("ap");
    

	//Graphic Tweaks-------------------------------------------------------------------

	mg->GetXaxis()->SetTitleSize(0.042);
	mg->GetYaxis()->SetTitleSize(0.042);
	mg->GetXaxis()->SetLabelSize(0.045);
	mg->GetYaxis()->SetLabelSize(0.045);
	mg->GetYaxis()->SetTitleOffset(1.);
    mg->GetXaxis()->SetTitleOffset(1.);
    //mg->GetYaxis()->SetMaxDigits(3);
    
    
    //mg->GetXaxis()->SetLimits(1E-8, 1);
    //mg->SetMinimum(505000);
    //mg->SetMaximum(509000);

	//canv->BuildLegend();
	canv->Update();
 
	canv->Modified();


	//---------------------------------------------------------------------------------
	//---------------------------------------------------------------------------------

	myApp->Run();

	return 0;
}
