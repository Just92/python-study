@rem ver 1.0 
@set DT=%DATE:~0,4%-%DATE:~5,2%-%DATE:~8,2%

@if "%1" =="" goto USAGE
@if "%2" =="" goto USAGE

:start 
@set project_name=%2
@set project_version=%1
####
@echo good luck!
@goto END

:USAGE 
@echo usage: ant_htsc.bat [project.version] [project.name] [Environment]
@echo Example: ant_htsc.bat 2.1.0 csp uat/prod
@echo project.name about:
@echo [acrmserver\cbs\csp\ecif\ecifm\htesb\ibcrm\tokenServer\TTServer\tzpt\tzpt_load\infopubplat]

:END
@echo END.