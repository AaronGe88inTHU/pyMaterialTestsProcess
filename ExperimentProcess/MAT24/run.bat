@echo off
 
set ENV_PATH=%PATH%
@echo ====current environment:
@echo %ENV_PATH%


set MY_PATH=H:\Project6\DFMC\Experiments\FEW\SAE0340_100mm_min\0_1MM\1
set ENV_PATH=%PATH%;%MY_PATH%
@echo ====new environment:
@echo %ENV_PATH%
 
pause
call python PostProcess.py force.xlsx 5.036 1.972 u_c 50 250