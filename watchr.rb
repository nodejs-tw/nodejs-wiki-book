watch( '(.*)\.rst' )  {|md| system("sphinx-cook -f pdf .") }
