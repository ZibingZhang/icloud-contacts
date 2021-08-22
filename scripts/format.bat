@echo off
rem https://stackoverflow.com/questions/58732724/turn-on-echo-for-a-single-command-in-a-batch-file
call :define_macro

%+@% echo Format pyicloud
python -m black pyicloud

%+@% echo.
%+@% echo Format app
python -m black app

exit /b

:define_macro
(set \n=^^^

)
set ^"+@=for %%# in (1 2) do if %%#==2 (%\n%
    setlocal EnableDelayedExpansion %\n%
    for /F "tokens=1,*" %%1 in ("!time: =0! !argv!") do (%\n%
        %%2%\n%
      )%\n%
    ) ELSE set argv="

exit /b
