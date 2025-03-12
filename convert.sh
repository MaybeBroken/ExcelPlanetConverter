
echo Converting %1 to %2...
java -jar excelToCsv.jar --input %1 --sheet-name "System Builder" >> %2
echo Finished conversion, file saved to %2
