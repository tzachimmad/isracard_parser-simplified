//
//  Estab.hpp
//  Interview_prep
//
//  Created by Tzachi Lapidot on 27/02/2018.
//  Copyright © 2018 Tzachi Lapidot. All rights reserved.
//

#ifndef Estab_hpp
#define Estab_hpp
#include <array>
#include <string>

class Estab                      // begin declaration of the class
{
public:                      // begin public section
    Estab(std::string estab);       // constructor
    void add_expense(int mn, int year, int amount);
    ~Estab();                    // destructor
    static int year;
    
    
    
private:                      // begin private section
    std::string estab;
    std::array<int, 24> expenseArr;
};
#endif /* Estab_hpp */
