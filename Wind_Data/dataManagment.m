close all
clear all
clc

% Load all forecast data:
% The tables have columns date, time, Starting_Time, Min_ConfInt,
% Max_ConfInt, Forecast, Real.

AWSTP_0100 = readtable('Wind_Data_AWSTP_0100.csv');
AWSTP_0700 = readtable('Wind_Data_AWSTP_0700.csv');
AWSTP_1300 = readtable('Wind_Data_AWSTP_1300.csv');
AWSTP_1900 = readtable('Wind_Data_AWSTP_1900.csv');

MTLOG_0100 = readtable('Wind_Data_MTLOG_0100.csv');
MTLOG_0700 = readtable('Wind_Data_MTLOG_0700.csv');
MTLOG_1300 = readtable('Wind_Data_MTLOG_1300.csv');
MTLOG_1900 = readtable('Wind_Data_MTLOG_1900.csv');

UTEP5_0100 = readtable('Wind_Data_UTEP5_0100.csv');
UTEP5_0700 = readtable('Wind_Data_UTEP5_0700.csv');
UTEP5_1300 = readtable('Wind_Data_UTEP5_1300.csv');
UTEP5_1900 = readtable('Wind_Data_UTEP5_1900.csv');

dataCell = {AWSTP_0100,AWSTP_0700,AWSTP_1300,AWSTP_1900,...
    MTLOG_0100,MTLOG_0700,MTLOG_1300,MTLOG_1900,...
    UTEP5_0100,UTEP5_0700,UTEP5_1300,UTEP5_1900};

% Compute the number of days for each set of data:

heights = [height(AWSTP_0100),
    height(AWSTP_0700),
    height(AWSTP_1300),
    height(AWSTP_1900),
    height(MTLOG_0100),
    height(MTLOG_0700),
    height(MTLOG_1300),
    height(MTLOG_1900),
    height(UTEP5_0100),
    height(UTEP5_0700),
    height(UTEP5_1300),
    height(UTEP5_1900)] / 72; % <<< Notice the / 72.

% We create a set of data for the forecast:

for i = 1:length(heights)
    
    auxCell  = {};
    auxTable = cell2table(cell(0,5));
    auxTable.Properties.VariableNames{'Var1'} = 'Date';
    auxTable.Properties.VariableNames{'Var2'} = 'Forecast';
    auxTable.Properties.VariableNames{'Var3'} = 'Real';
    auxTable.Properties.VariableNames{'Var4'} = 'Min_Conf';
    auxTable.Properties.VariableNames{'Var5'} = 'Max_Conf';
    
    for j = 0:heights(i)-1
        
        aux            = {dataCell{i}(1+j*72,1).Var1,...
            table2array(dataCell{i}(1+j*72:1+j*72+71,6))};
        aux2           = {aux{:},...
            table2array(dataCell{i}(1+j*72:1+j*72+71,7)),...
            table2array(dataCell{i}(1+j*72:1+j*72+71,4)),...
            table2array(dataCell{i}(1+j*72:1+j*72+71,5))};
        auxTable       = [auxTable;aux2];
        auxCell{end+1} = aux;
        
        disp(['i = ',num2str(i),' and j = ',num2str(j)]);
        
    end
        
    allPathsData{i}  = auxCell;
    allTablesData{i} = auxTable;
    
end

save('allPathsData.mat','allPathsData');
save('allTablesData.mat','allTablesData');

% We load real production data:

initialDate = '20161103';
currentDate = initialDate;
finalDate   = datestr(today-6,'yyyymmdd');

count = 1;

try
    load('allWindData.mat');
    currentDate = allWindData{end}{1};
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = length(allWindData) + 1;
end

while not(strcmp(currentDate,finalDate))
    
    disp(['Day ',currentDate]);
    % Each day starts at 00:00 and finishes at 23:50. This is 72 points.
    wind_data = loadods(['../ADME_Historicos_Corrected/',currentDate,'.ods'],'GPF','');
    wind_data = cell2mat(wind_data);
    wind_data = wind_data(1:end-1,5);
    allWindData{count,:} = {currentDate,wind_data};
    count = count + 1;
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    
    if mod(count,10) == 0
        save('allWindData.mat','allWindData');
    end
    
end

save('allWindData.mat','allWindData');