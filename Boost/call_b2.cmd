@echo off

REM C++Boost as a Python package
REM
REM Copyright (C) 2017 Stefan Zimmermann <user@zimmermann.co>
REM
REM This is free software: you can redistribute it and/or modify
REM it under the terms of the GNU Lesser General Public License as published
REM by the Free Software Foundation, either version 3 of the License, or
REM (at your option) any later version.
REM
REM This is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU Lesser General Public License for more details.
REM
REM You should have received a copy of the GNU Lesser General Public License
REM along with this.  If not, see <http://www.gnu.org/licenses/>.

setlocal EnableExtensions EnableDelayedExpansion || exit

if "%1" == "/?" (
   echo Call Boost's .\b2 in current working directory.
   echo.
   echo CALL_B2 [b2args ...]
   echo.
   echo This wrapper script is necessary to run b2 as subprocess from Python.
   echo It fixes the case of the %%ProgramFiles%% variable name.
   exit /b 0
)

set "_ProgramFiles=%PROGRAMFILES%"
REM explicitly unset variable to enable recreation of name with proper case
set ProgramFiles=
set "ProgramFiles=%_ProgramFiles%"

call .\b2 %* || exit

endlocal
