function [resultado] = mifuncion(entrada1,entrada2,entrada3)

elmayor = 0;
	if (entrada1 > entrada2 && entrada1 > entrada3)
    	elmayor = entrada1;
	end
    if (entrada2 > entrada1 && entrada2 > entrada3)
    	elmayor = entrada2;
	end
    if (entrada3 > entrada1 && entrada3 > entrada2)
		elmayor = entrada3;
	end
resultado = elmayor;

end