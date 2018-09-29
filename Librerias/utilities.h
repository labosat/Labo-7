#include "libs.h"

void Load(std::string s, std::vector<double>& A)
{
    double a = 0;
    std::ifstream file;
    file.open(s);
    if (file.is_open())
    {
        while(!(file >> a) == 0)
        {
            A.push_back(a);
        }
    }
    return;
}

//vector data Loader, graph using pointer &A[0] as argument in TGraph
//removes zeros on vectors
void Load(std::string s, std::vector<double>& A, std::vector<double>& B)
{
	double a, b = 0;
    //std::string c, d;
    std::ifstream file; 
	file.open(s);
    if (file.is_open())
    {
        //file >> c >> d;
        while(!(file >> a >> b) == 0)
        {
            if(a != 0 && b != 0)
            {
                A.push_back(a);
                B.push_back(b);
            }
	
        }
	file.close();
    }
    else
    {
        std::cout << "Could not open specified file." << std::endl;        
    }

    return;
}


void Load(std::string s, std::vector<double>& A, std::vector<double>& B, std::vector<double>& A_err, std::vector<double>& B_err)
{
	double a, b, c, d = 0;
	std::ifstream file; 
	file.open(s);
    if (file.is_open())
    {
        while(!(file >> a >> b >> c >> d) == 0)
        {
            if(a != 0 && b != 0)
            {
                A.push_back(a);
                B.push_back(b);
                A_err.push_back(c);
                B_err.push_back(d);
            }
	
        }
	file.close();
    }
    else
    {
        std::cout << "Could not open specified file." << std::endl;        
    }

    return;
}

void Multiply(std::vector<double>& A, std::vector<double>& B, double n, double m)
{
	for (int i = 0; i < A.size(); i++)
	{
		A[i] = n*A[i];
		B[i] = m*B[i];
	}
	return;
}


//inverts order of elements of vector
void Reverse(std::vector<double>& A, std::vector<double>& B)
{
    std::vector<double> A_temp;
    std::vector<double> B_temp;
    for (int i = 0; i < A.size(); i++)
    {
        A_temp.push_back(A[A.size() - i - 1]);
        B_temp.push_back(B[B.size() - i - 1]);
    }
    
    A.clear();
    B.clear();
    
    for (int i = 0; i < A_temp.size(); i++)
    {
        A.push_back(A_temp[i]);
        B.push_back(B_temp[i]);
    }

    return;
}


//returns vector of errors according to SMU range
std::vector<double> SourceError(std::vector<double>& A, char type, std::string scale)
{
	double percentage;
	double offset;
	if (type == 'I')
	{
		if (scale == "10uA")
		{
			percentage = 0.0003;
			offset = 5*pow(10, -9);
		}
		else if (scale == "100uA")
		{
			percentage = 0.0003;
			offset = 60*pow(10, -9);
		}
		else
		{
			std::cout << scale << " is not a valid range." << std::endl;
		}
	}
	else if (type == 'V')
	{
		if (scale == "2V")
		{
			percentage = 0.0002;
			offset = 600*pow(10, -6);
		}
		else if (scale == "20V")
		{
			percentage = 0.0002;
			offset = 5*pow(10, -3);
		}
		else if (scale == "200V")
		{
			percentage = 0.0002;
			offset = 50*pow(10, -3);
		}
		else
		{
			std::cout << scale << " is not a valid range." << std::endl;
		}
	}
	else
	{
		std::cout << "type specified not understood" << std::endl;
	}

	std::vector<double> temp;
	for (int i = 0; i < A.size(); i++)
	{
		double result = A[i]*percentage + offset;
		temp.push_back(result);
	}
	return temp;
}


//returns vector of errors according to SMU range
std::vector<double> MeasureError(std::vector<double> A, char type, std::string scale)
{
	double percentage = 0;
	double offset = 0;
	if (type == 'I')
	{
        if (scale == "100nA")
		{
			percentage = 0.0006;
			offset = 100*pow(10, -12);
		}
        else if (scale == "1uA")
		{
			percentage = 0.00025;
			offset = 500*pow(10, -12);
		}
		else if (scale == "10uA")
		{
			percentage = 0.00025;
			offset = 1.5*pow(10, -9);
		}
		else if (scale == "100uA")
		{
			percentage = 0.0002;
			offset = 25*pow(10, -9);
		}
		else if (scale == "10mA")
		{
			percentage = 0.0002;
			offset = 2.5*pow(10, -6);
		}
		else if (scale == "100mA")
        {
            percentage = 0.0002;
			offset = 20*pow(10, -6);
        }

        else
		{
			std::cout << scale << " is not a valid range." << std::endl;
		}
	}
	else if (type == 'V')
	{
        if (scale == "200mV")
        {
            percentage = 0.00015;
            offset = 225*pow(10, -6);
        }
		else if (scale == "2V")
		{
			percentage = 0.0002;
			offset = 350*pow(10, -6);
		}
		else if (scale == "20V")
		{
			percentage = 0.00015;
			offset = 5*pow(10, -3);
		}
		else if (scale == "200V")
		{
			percentage = 0.00015;
			offset = 50*pow(10, -3);
		}
		else
		{
			std::cout << scale << " is not a valid range." << std::endl;
		}
	}
	else
	{
		std::cout << "type specified not understood" << std::endl;
	}

    std::vector<double> temp;
    for (int i = 0; i < A.size(); i++)
    {
        double number = A[i]*percentage + offset;
        temp.push_back(number);
    }
    return temp;
}


//applies sqrt to dataset and propagates errors accordingly
void SqrtData(std::vector<double>& A, std::vector<double>& A_err)
{
	std::vector<double> A_temp;
	std::vector<double> A_temp_err;
	for (int i = 0; i < A.size(); i++)
	{
		A_temp.push_back(sqrt(A[i]));
		A_temp_err.push_back((A_err[i])/(2*sqrt(A[i])));
	}
	A = A_temp;
	A_err = A_temp_err;
	return;
}


//applies log to dataset and propagates errors accordingly
void LogData(std::vector<double>& A, std::vector<double>& A_err)
{
	std::vector<double> A_temp;
	std::vector<double> A_temp_err;
	for (int i = 0; i < A.size(); i++)
	{
        A_temp.push_back(log(A[i]));
        A_temp_err.push_back((A_err[i])/(A[i]));
	}
	A = A_temp;
	A_err = A_temp_err;
	return;
}


//returns derivative of dataset. Returns vector that is same size as original
void DeriveData(std::vector<double>& A, std::vector<double>& A_err)
{
	std::vector<double> A_temp;
	std::vector<double> A_temp_err;
	double step = A[2] - A[1];
    double dy = 0;
    double dy_err;
    double term1 = 0;
	for (int i = 0; i < A.size(); i++)
	{
        if (i == 0)
        {
            dy = A[i + 2] - A[i + 1];
            dy_err = A_err[i];
            A_temp.push_back(A[i] + dy*step);
            
            A_temp_err.push_back(dy_err);
        }
        else if (i == A.size() - 1)
        {
            dy = A[i] - A[i - 1];
            dy_err = A_err[i];
            A_temp.push_back(A[i] + dy*step);
                        
            A_temp_err.push_back(dy_err);
        }
        else
        {
            A_temp.push_back((A[i + 1] - A[i - 1])/(2*step));
    		
            term1 = pow((A_err[i + 1] - A_err[i - 1])/(2*step), 2);
            A_temp_err.push_back(sqrt(term1));
        }

	}

	A = A_temp;
	A_err = A_temp_err;
	return;
}


//returns a vector that is 2 entries shorter (1 on both sides)
void DeriveData2(std::vector<double>& A, std::vector<double>& B, std::vector<double>& A_err, std::vector<double>& B_err)
{
	std::vector<double> V_temp;
	std::vector<double> I_temp;
	std::vector<double> V_temp_err;
	std::vector<double> I_temp_err;
	double step = A[2] - A[1];
	for (int i = 1; i <  B.size() - 1; i++)
	{

		I_temp.push_back((B[i + 1] - B[i - 1])/(2*step));
		V_temp.push_back(A[i]);

		
		double term1 = pow((B_err[i + 1] - B_err[i - 1])/(2*step), 2);

		I_temp_err.push_back(sqrt(term1));

		V_temp_err.push_back(A_err[i]);

	}
	A.pop_back();
	A.pop_back();

	B.pop_back();
	B.pop_back();

	A_err.pop_back();
	A_err.pop_back();

	B_err.pop_back();
	B_err.pop_back();


	A = V_temp;
	B = I_temp;
	A_err = V_temp_err;
	B_err = I_temp_err;
	return;
}

//returns maximum element of vector
double FindMax(std::vector<double> v)
{
	double max = -1000;
	int index = 0;
	for (int i = 0 ; i < v.size(); i++)
	{
		if (v[i] > max)
		{
			max = v[i];
			index = i;
		}
	}
	return max;
}


//returns index of maximum element of vector
int FindMaxIndex(std::vector<double> v)
{
	double max = -1000;
	int index = 0;
	for (int i = 0 ; i < v.size(); i++)
	{
		if (v[i] > max)
		{
			max = v[i];
			index = i;
		}
	}
	return index;
}


//returns element of vector closest to one
double FindClosestToOne(std::vector<double> chi2)
{
	double compliance = 1;
	int i = 0;
	for (int j = 0; j < chi2.size(); j++)
	{
		if (abs(chi2[j] - 1) < compliance)
		{
			i = j;
			compliance = abs(chi2[j] - 1);
		}
	}
	
	double result = i;
	return result;
}


template <typename T> 
bool ElementInVector(T a, std::vector<T> v)
{
    for (int i = 0; i < v.size(); i++)
    {
        if (a == v[i])
            return true;
    }
    return false;
}


std::vector<double> MultiRangeError(std::vector<double> A, char ch)
{
    std::vector<double> temp;
    double percentage, offset = 0;
    for (int i = 0; i < A.size(); i++)
    {
        if (ch == 'I')
        {
            if (A[i] < pow(10, -7))
            {
                percentage = 0.0006;
                offset = 100*pow(10, -12);
            }
            else if(A[i] > pow(10, -7) && A[i] < pow(10, -6))
            {
                percentage = 0.00025;
                offset = 500*pow(10, -12);
            }
            else if(A[i] > pow(10, -6) && A[i] < pow(10, -5))
            {
                percentage = 0.00025;
                offset = 1.5*pow(10, -9);
            }
            
            else if(A[i] > pow(10, -5) && A[i] < pow(10, -4))
            {
                percentage = 0.0002;
                offset = 25*pow(10, -9);
            }
            else if(A[i] > pow(10, -4) && A[i] < pow(10, -3))
            {
                percentage = 0.0002;
                offset = 200*pow(10, -9);
            }
            else if(A[i] > pow(10, -3) && A[i] < pow(10, -2))
            {
                percentage = 0.0002;
                offset = 2.5*pow(10, -6);
            }
            
            else if(A[i] > pow(10, -2) && A[i] < pow(10, -1))
            {
                percentage = 0.0002;
                offset = 20*pow(10, -6);
            }
            
            double number = A[i]*percentage + offset;
            temp.push_back(number);
        }
        
    }
    return temp;
}

//Determines range of measurements automatically
std::vector<std::string> DetermineRange(std::vector<double> v, std::vector<double> s)
{
	std::vector<std::string> output;
    std::vector<double> count;
	//in V
	double range_lib_v[4] = {0.2, 2, 20, 200};
	//in A
	double range_lib_i[6] = {pow(10, -7), pow(10, -6), pow(10, -5), pow(10, -4), 0.01, 0.1};
	
    double max_v = FindMax(v);
	double max_i = FindMax(s);

	std::string range_v;
	std::string range_i;
    double number_v = 1;
    double number_i = 1;
    double output_range_v = 0;
    double output_range_i = 0;

	for (int i = 0; i < 4; i++)
	{
		double comparison_v = abs(max_v - range_lib_v[i])/range_lib_v[i];

		if (comparison_v < number_v && range_lib_v[i] >= max_v)
		{
			number_v = comparison_v;
            output_range_v = range_lib_v[i];
		}
	}
	
	for (int i = 0; i < 6; i++)
	{
		double comparison_i = abs(max_i - range_lib_i[i])/range_lib_i[i];		
		if (comparison_i < number_i && range_lib_i[i] >= max_i)
		{
			number_i = comparison_i;
            output_range_i = range_lib_i[i];
		}
	}

	
    if (output_range_v == 0.2)
	{
		range_v = "200mV";
	}
	else if (output_range_v == 2)
	{
		range_v = "2V";
	}
	else if (output_range_v == 20)
	{
		range_v = "20V";
	}
	else if (output_range_v == 200)
	{
		range_v = "200V";
	}
	
    if (count.size() > 1)
    {   
        output.push_back(range_v);
        output.push_back("multirange");
        std::cout << "multirange detected: " << "\n";
        return output;
    }
	
    if (output_range_i == pow(10, -7))
	{
		range_i = "100nA";
	}
	
    if (output_range_i == pow(10, -6))
	{
		range_i = "1uA";
	}
	
	if (output_range_i == pow(10, -5))
	{
		range_i = "10uA";
	}
	else if (output_range_i == pow(10, -4))
	{
		range_i = "100uA";
	}
	else if (output_range_i == 0.01)
	{
		range_i = "10mA";
	}
	else if (output_range_i == 0.1)
	{
		range_i = "100mA";
	}

	output.push_back(range_v);
	output.push_back(range_i);

	return output;
}


//NOT WORKING
//automatically calculates degree of roughness, which is an int that indicates the degree that is needed to smooth the data
int RoughnessDegree(std::vector<double> v)
{
    int counter = 0;
    
	for (int i = 1; i < v.size() - 1; i++)
	{
        if (abs(abs(v[i]) - abs(v[i + 1])) > 1.8 && abs(abs(v[i]) - abs(v[i - 1])) > 1.8)
        {
            counter += 1;
        }

	}
	std::cout << counter;
    return counter;
}


//NOT WORKING
//smoothes dataset when there is a noisy signal (runs function "degree" times on dataset)
void Smooth(std::vector<double>& v, std::vector<double>& s, std::vector<double>& v_err, std::vector<double>& i_err)
{
	std::vector<double> v_temp;
	std::vector<double> i_temp;
	std::vector<double> v_temp_err;
	std::vector<double> i_temp_err;

    for (int i = 0; i < s.size(); i++)
    {
        if (i == 0)
        {
            i_temp.push_back(s[i]);
            i_temp_err.push_back(i_err[i]);
            v_temp.push_back(v[i]);
            v_temp_err.push_back(v_err[i]);
        }
        else if (i == 1)
        {
            i_temp.push_back((1/3)*(s[i + 1] + s[i] + s[i - 1]));
            i_temp_err.push_back(i_err[i]);
            v_temp.push_back(v[i]);
            v_temp_err.push_back(v_err[i]);
        }
        else if (i >= 2 && i < s.size() - 2)
        {
            i_temp.push_back((1/5)*(s[i + 2] + s[i + 1] + s[i] + s[i - 1] + s[i - 2]));
            i_temp_err.push_back(i_err[i]);
            v_temp.push_back(v[i]);
            v_temp_err.push_back(v_err[i]);
        }
        else if (i == s.size() - 2)
        {
            i_temp.push_back((1/3)*(s[i + 1] + s[i] + s[i - 1]));
            i_temp_err.push_back(i_err[i]);
            v_temp.push_back(v[i]);
            v_temp_err.push_back(v_err[i]);   
        }
        else if (i == s.size() - 1)
        {
            i_temp.push_back(s[i]);
            i_temp_err.push_back(i_err[i]);
            v_temp.push_back(v[i]);
            v_temp_err.push_back(v_err[i]);
        }

    }
    
    v.clear();
    s.clear();
    v_err.clear();
    i_err.clear();
    
    v = v_temp;
    s = i_temp;
    v_err = v_temp_err;
    i_err = i_temp_err;
    
	return;
}


//parse string to T
template <class T>
T parse(const std::string& s)
{
  T out;
  std::stringstream ss(s);
  ss >> out;
  return out;
}

std::vector<std::string> SeparateStrings(std::string s)
{
    std::vector<std::string> output;
    std::string string1;
    std::string string2;
    bool check = false;
    
    for (char ch : s)
    {
        if (!check)
        {
            if (isdigit(ch) || ch == '.')
            {
                string1 += ch;
            }
        }
        else if (check)
        {
            if (isdigit(ch) || ch == '.')
            {
                string2 += ch;
            }
        }
        
        if (ch == '%')
        {
            check = true;
        }
    }
    output.push_back(string1);
    output.push_back(string2);
    
    return output;
}


void CalibrateT(std::vector<double>& R, std::vector<double>& R_err, double R_amb, double m)
{
    double T = 0;
    double Tamb = (R_amb - 1000)/m;
    for (int i = 0; i < R.size(); i++)
    {
        T = (R_amb - R[i] - 1000)/m;
        R[i] = T;
    }
    return;
}

//use caution. This can only be used if a occurs only once in v
int IndexInVector(double a, std::vector<double> v)
{
    int index = 0;
    for (int i = 0; i <  v.size(); i++)
    {
        if (v[i] == a)
            index = i;
    }
    return index;
}





