
@ECHO OFF

SET VER=341
IF NOT DEFINED PYTHON_PATH_DEFINED  SET PATH=c:\Python%VER%;%PATH%;
SET PYTHON_PATH_PATH_DEFINED=1

@ECHO ---GOOD LOCK PYTHON(%VER%)---

