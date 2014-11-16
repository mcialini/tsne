@echo off
echo.
echo Beginning spider crawl
echo.
echo **** VT DOI ***
call scrapy crawl --nolog vtdoi
echo **** END VT DOI ***
echo.
echo **** VT DFR ***
call scrapy crawl --nolog vtdfr
echo **** END VT DFR ***
echo.
echo **** NH DOI ***
call scrapy crawl --nolog nhdoi
echo **** END NH DOI ***
echo.
echo **** ME DOI ***
call scrapy crawl --nolog medoi
echo **** END ME DOI ***
echo.
echo **** RI DOI ***
call scrapy crawl --nolog ridoi
echo **** END RI DOI ***
echo.
echo **** CT DOI ***
call scrapy crawl --nolog ctdoi
echo **** END CT DOI ***
echo.
echo **** CT DOI MED***
call scrapy crawl --nolog ctdoimed
echo **** END CT DOI MED ***
echo.
echo **** MA DOI ***
call scrapy crawl --nolog madoi
echo **** END MA DOI ***
echo.
echo Completed spider crawl
echo.