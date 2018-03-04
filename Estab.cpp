//
//  Expense.cpp
//  Interview_prep
//
//  Created by Tzachi Lapidot on 27/02/2018.
//  Copyright © 2018 Tzachi Lapidot. All rights reserved.
//

#include "Estab.hpp"
#include <array>
#include <iostream>            // for cout and cin
using namespace std;

int Estab::year = 2017;

Estab::Estab(string estab)
{
    this->estab = estab;
    for (int i =0; i<24;i++)
        expenseArr[i]=0;
}


Estab::~Estab()
{
}

// GetAge, Public accessor function
// returns value of itsAge member
void Estab::add_expense(int mn, int year, int amount)
{
    if (Estab::year==this->year)
        expenseArr[12+mn-1]+=amount;
    else if (Estab::year==this->year+1)
        expenseArr[mn-1]+=amount;
}

