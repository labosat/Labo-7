#include "/home/lucas/Desktop/Facultad/Labo7/libs/libs.h"

template<typename T>
class ROOTDATA
{
public:
	ROOTDATA(std::string p, uint n, uint skiprows = 0);
	ROOTDATA(std::string p, uint n, std::string f, uint skiprows = 0);
	//~ROOTDATA();

	std::string GetFlag();
    std::vector<T>* Load();
	void SetLabel(int index, std::string label);
    std::string* GetLabels();
	void Log(int index);
	void Sqrt(int index);	
	//void Smooth(int degree);

	void Graph(int x, int y);
	//void Fit(TF1 *f, n_params, function_to_minimize);

private:
	std::string path;
	uint num_data;
	std::vector<T>* data;
	std::string* data_labels;
	std::string flag;
};


template <typename T>
ROOTDATA<T>::ROOTDATA(std::string p, uint n, uint skiprows)
{
	data = new std::vector<T>[n];
	data_labels = new std::string[n];
	
    num_data = n;
	path = p;
	flag = "Direct Load";

	for (uint i = 0; i < n; i++)
	{
		data_labels[i] = "p" + std::to_string(i);
	}

	std::ifstream ifs;
	ifs.open(path);
	
	if (ifs.is_open())
	{
		T a = 0;
		if (skiprows != 0)
		{
			char b = '0';
			for (uint i = 0; i < skiprows; i++)
			{
				for (uint j = 0; j < num_data; j++)
				{
					ifs >> b;
				}
			}
		}
		
		while(!(ifs >> a) == 0)
		{
			for (uint i = 0; i < num_data; i++)
			{
				if (i == 0)
				{
					data[i].push_back(a);			
				}
				else 
				{
					ifs >> a;
					data[i].push_back(a);
				}
			}	
		}
	}
	else
	{
		std::cout << "Could not open file in " << path << "\n";
	}
	return;
}

//flags can be: "Source V" or "Source I" ("Measure I" is implied in the former and "Measure V" is implied in the latter)
template <typename T>
ROOTDATA<T>::ROOTDATA(std::string p, uint n, std::string f, uint skiprows)
{
	data = new std::vector<T>[2*n];
	data_labels = new std::string[2*n];
    
	num_data = 2*n;
	path = p;
	flag = f;

	for (uint i = 0; i < num_data; i++)
	{
		if (i < n)
			data_labels[i] = "p" + std::to_string(i);
		else
			data_labels[i] = "p" + std::to_string(i) + "_err";
	}

	std::ifstream ifs;
	ifs.open(path);
	
	if (ifs.is_open())
	{
		T a = 0;
		if (skiprows != 0)
		{
			char b = '0';
			for (uint i = 0; i < skiprows; i++)
			{
				for (uint j = 0; j < n; j++)
				{
					continue;
				}
			}
		}
		
		while(!(ifs >> a) == 0)
		{
			for (uint i = 0; i < n; i++)
			{
				if (i == 0)
				{
					data[i].push_back(a);			
				}
				else 
				{
					ifs >> a;
					data[i].push_back(a);
				}
			}	
		}
	}
	else
	{
		std::cout << "Could not open file in " << path << "\n";
	}

	if (f == "Source V")
	{
		//assignement of errors in source V, measure I
		
	}
	else if (f == "Source I")
	{
		//assignement of errors in source I, measure V
		
	}
	return;
}

// template <typename T>
// ROOTDATA<T>::~ROOTDATA()
// {
// 	data.reset();
//     data_labels.reset();
// }

template <typename T>
std::string ROOTDATA<T>::GetFlag()
{
	return flag;
}

template <typename T>
std::vector<T>* ROOTDATA<T>::Load()
{
	return data;
}

template <typename T>
void ROOTDATA<T>::SetLabel(int index, std::string label)
{
	data_labels[index] = label;
    return;
}

template <typename T>
std::string* ROOTDATA<T>::GetLabels()
{
    return data_labels;
}

template <typename T>
void ROOTDATA<T>::Log(int index)
{
	if (flag == "Direct Load")
	{
		std::vector<T> temp_data = data[index];
		for (uint i = 0; i < temp_data.size(); i++)
		{
			temp_data[i] = Log(temp_data[i]);
		}
		data[index] = temp_data;		
	}
	else
	{
		std::vector<T> temp_data = data[index];
		std::vector<T> temp_data_err = data[index + num_data/2];

		for (uint i = 0; i < temp_data.size(); i++)
		{
			temp_data[i] = Log(temp_data[i]);
			temp_data_err[i] = abs(temp_data_err[i]/temp_data[i]);
		}
		data[index] = temp_data;
		data[index + num_data/2] = temp_data_err;
	}
	return;
}

template <typename T>
void ROOTDATA<T>::Sqrt(int index)
{
	if (flag == "Direct Load")
	{
		std::vector<T> temp_data = data[index];
		for (uint i = 0; i < temp_data.size(); i++)
		{
			temp_data[i] = sqrt(temp_data[i]);
		}
		data[index] = temp_data;		
	}
	else
	{
		std::vector<T> temp_data = data[index];
		std::vector<T> temp_data_err = data[index + num_data/2];

		for (uint i = 0; i < temp_data.size(); i++)
		{
			temp_data[i] = sqrt(temp_data[i]);
			temp_data_err[i] = abs(temp_data_err[i]/(2*sqrt(temp_data[i])));
		}
		data[index] = temp_data;
		data[index + num_data/2] = temp_data_err;
	}
	return;
}


// 20 value in x_err or y_err means 
template <typename T>
void ROOTDATA<T>::Graph(int x, int y)
{
	std::vector<double> x_data = data[x];
	std::vector<double> y_data = data[y];
	std::vector<double> x_err_data;
	std::vector<double> y_err_data;

	TCanvas *c = new TCanvas("quick graph", "quick graph", 600, 600);

	for (uint i = 0; i < num_data; i++)
	{
		if (data_labels[i] == data_labels[x] + "_err")
			x_err_data = data[i];
		else if (data_labels[i] == data_labels[y] + "_err")
			y_err_data = data[i];
	}

	if (x_err_data.size() == 0 and y_err_data.size() == 0)
	{
		TGraph *graph = new TGraph(x_data.size(), &x_data[0], &y_data[0]);
        graph->Draw("AP");
	}
	else if (x_err_data.size() == 0 and y_err_data.size() != 0)
	{
		TGraphErrors *graph = new TGraphErrors(x_data.size(), &x_data[0], &y_data[0], 0, &y_err_data[0]);
        graph->Draw("AP");
	}
	else if (x_err_data.size() != 0 and y_err_data.size() == 0)
	{
		TGraphErrors *graph = new TGraphErrors(x_data.size(), &x_data[0], &y_data[0], &x_err_data[0], 0);
        graph->Draw("AP");
	}
	else if (x_err_data.size() != 0 and y_err_data.size() != 0)
	{
		TGraphErrors *graph = new TGraphErrors(x_data.size(), &x_data[0], &y_data[0], &x_err_data[0], &y_err_data[0]);
        graph->Draw("AP");
	}
	c->Update();
	return;
}


//--------------------------------------------------------------------------

// class FITTER
// {
// public:
// 	FITTER(TF1 *f, int p);
// 	~FITTER();
// 
// 	void SetFunction(TF1 *f);
// 	void SetMinimizer(TMinuit t);
// 	void Run();
// 
// 	RUN();
// private:
// 	TMinuit *minimizer;
// 	TF1 *function;
// 	int parameters;
// 	
// };
// 
// 
// FITTER::FITTER(TF1 *f, int p)
// {
// 	self->minimizer = new TMinuit(parameters);
// 	self-> function = f;
// 	self->parameters = p;
// }
// 
// FITTER::~FITTER()
// {
// 	delete minimizer;
// 	delete function;
// }
// 
// 
// void FITTER::SetFunction(TF1 *f)
// {
// 	function = f;
// 	return;
// }
// 
// void FITTER::SetMinimizer(TMinuit *t)
// {
// 	minimizer = t;
// 	return;
// }
