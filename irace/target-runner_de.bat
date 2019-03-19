::##############################################################################
:: BAT version of target-runner for Windows.
:: Contributed by Andre de Souza Andrade <andre.andrade@uniriotec.br>.
:: Check other examples in examples/
::
:: This script is run in the execution directory (execDir, --exec-dir).
::
:: PARAMETERS:
:: %%1 is the candidate configuration number
:: %%2 is the instance ID
:: %%3 is the seed
:: %%4 is the instance name
:: The rest are parameters to the target-algorithm
::
:: RETURN VALUE:
:: This script should print one numerical value: the cost that must be minimized.
:: Exit with 0 if no error, with 1 in case of error
::##############################################################################
@echo off

:: Please change the EXE and FIXED_PARAMS to the correct ones
SET "exe=python .\call_de.py"

%exe% --nfe 1e+5 --n %5 --beta %6 --pr %7 --bbob "function_indices:1,15 dimensions:10 instance_indices:1-10"

exit 0