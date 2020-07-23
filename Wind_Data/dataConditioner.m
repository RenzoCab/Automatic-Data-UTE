close all;
clear all;
clc;

load('allWindData');
load('allPathsData');
load('allTablesData');

set(0,'defaultAxesFontSize',12);

% IMPORTANT: The first step is to run this cell.
% The second step is to run the cell below that you need.

% CELLS DESCRIPTION:
% (1) From each forecast source, we check that all of them share the real
% production. In particular, we do this for the 0100 data and only for one
% particular day.

% (2) We compare ADME and UTE real productions. We also plot the forecast
% with confidence intervals.

% (3) For 2019, we save real ADME, real UTE, and forecast from MTLOG_0100.
% We introduce a delay of 100 minutes in ADME, so the data match. We save
% the first 6 hours from 0100 to 0700.

% (4) We plot the real ADME (with the delay) and UTE real productions for
% 2019, in a way that we can compare them. We also save all the plots.

% (5) We plot and save the data created in (3). We also save it.

% (6) For 2019, we save real ADME, real UTE, and forecast from MTLOG_0100.
% We introduce a delay of 100 minutes in ADME, so the data match. We save
% the first 24 hours from 0100 to 0100 of the next day
% (MTLOG_0100_and_Real_24h.mat).

% (7) We plot and save the data created in (6). We also save it.

% (8) Statistical analysis and filtering of incorrect data from (6). We
% save the filtered data in MTLOG_0100_and_Real_24h_Corrected.mat.

% (9) We plot and save the data created in (8). We also save it.

% (10) We load the data from (8) and create $\dot{p}$, $\Delta V$, and all
% the data related with the Lamperti Transform. Also, we separate all the
% data in two tables, and we save them in .mat and .csv formats.

% (11) We plot and save all the data from (10). We also load the data from
% (6), so we can plot histograms with and without curtailing.

%% (1) We check that the data have sense:

% We compare all the real productions. They should be the same always.
% We do this for the data from UTE. All the data start at 0100.

AWSTP_0100 = allTablesData{1};
MTLOG_0100 = allTablesData{5};
UTEP5_0100 = allTablesData{9};

all_paths = {AWSTP_0100,MTLOG_0100,UTEP5_0100};

% We choose this particular day:
specialDay = datetime('20200101','InputFormat','yyyyMMdd');

% We find where is the data corresponding to that day:
special_index = [find(AWSTP_0100.Date == specialDay),...
    find(MTLOG_0100.Date == specialDay),...
    find(UTEP5_0100.Date == specialDay)];

figure;
hold on;
simbols = {'x','o','-'};
for i = 1:3
    
    path = all_paths{i};
    path = path(special_index(i),3);
    path = path.Real;
    path = path{1};
    plot([1:72],path,simbols{i});
    
end
legend('AWSTP_0100 real','MTLOG_0100 real','UTEP5_0100 real');

grid minor;
xlim([1,72]);

%% (2) Now we compare UTE Vs. ADME:

% From ADME we have 144 points, corresponding from 00:00 to 23:50 hrs.
% From UTE we have 72 points, from 01:00 hrs to 00:00 hrs (3 days after).

MTLOG_0100 = allTablesData{5};
MTLOG_0700 = allTablesData{6};
MTLOG_1300 = allTablesData{7};
MTLOG_1900 = allTablesData{8};

% We choose this particular day:
specialDay_string = '20180601';
specialDay = datetime(specialDay_string,'InputFormat','yyyyMMdd');

% We find the index corresponding to our special day.
for i = 1:length(allWindData)
    if strcmp(allWindData{i}{1},specialDay_string)
        break;
    end
end
path_ADME = allWindData{i}{2};
% We add an inf to make the plotting easier.
path_ADME = [path_ADME;inf];

% We find where is the data corresponding to that day:
special_index = [find(MTLOG_0100.Date == specialDay),...
                find(MTLOG_0700.Date == specialDay),...
                find(MTLOG_1300.Date == specialDay),...
                find(MTLOG_1900.Date == specialDay)];
% And we save the path:
path1 = MTLOG_0100(special_index(1),3).Real{1};
path2 = MTLOG_0700(special_index(2),3).Real{1};
path3 = MTLOG_1300(special_index(3),3).Real{1};
path4 = MTLOG_1900(special_index(4),3).Real{1};
% And we save the path:
fore1 = MTLOG_0100(special_index(1),2).Forecast{1};
min1  = MTLOG_0100(special_index(1),4).Min_Conf{1};
max1  = MTLOG_0100(special_index(1),5).Max_Conf{1};

figure;
hold on;
plot([1:24], path1(1:24));
plot([7:30], path2(1:24));
plot([13:36],path3(1:24));
plot([19:42],path4(1:24));
plot(linspace(0,24,145),path_ADME);
grid minor;
xlim([0,24]);
legend('UTE 0100','UTE 0700','UTE 1300','UTE 1900','ADME');
title(specialDay_string);

figure;
hold on;
plot([1:24], path1(1:24));
plot([7:30], path2(1:24));
plot([13:36],path3(1:24));
plot([19:42],path4(1:24));
plot(linspace(-1.5,22.5,145),path_ADME);
grid minor;
xlim([0,24]);
legend('UTE 0100','UTE 0700','UTE 1300','UTE 1900','ADME 1.5 hours delay');
title(specialDay_string);

figure;
hold on;
plot([1:24], path1(1:24));
plot([1:24], fore1(1:24));
plot([1:24], min1(1:24));
plot([1:24], max1(1:24));
plot(linspace(-1.5,22.5,145),path_ADME);
grid minor;
xlim([0,24]);
legend('UTE Real','UTE Forecast','UTE Min','UTE Max','ADME 1.5 hours delay');
title(specialDay_string);

figure;
hold on;
plot([1:24], path1(1:24));
plot(linspace(0,24,145),path_ADME);
grid minor;
xlim([1,22]);
legend('Real Production Source 1','Real Production Source 2');
title(['Date: ',specialDay_string]);
ylabel('Power (MW)');
xlabel('Time (hrs)');
box;
saveas(gcf,[pwd '/someResults/forPaper/curt_and_error'],'epsc');

figure;
hold on;
plot([1:24], path1(1:24));
plot(linspace(-1.5,22.5,145),path_ADME);
grid minor;
xlim([1,22]);
legend('Real Production Source 1','Real Production Source 2 (corrected)');
ylabel('Power (MW)');
xlabel('Time (hrs)');
box;
title(['Date: ',specialDay_string]);
saveas(gcf,[pwd '/someResults/forPaper/curt_and_error_corr'],'epsc');

%% (3) Preparing the data that we will use (6 hrs) (I corrected the delay):

% I have an error: When the data does not exist in forecast_MTLOG_0100, we
% save the data from the previous day. To correct this, check (6).

MTLOG_0100 = allTablesData{5};

initialDate = '20190101';
currentDate = initialDate;
finalDate   = '20200101';

Table = cell2table(cell(0,3));
Table.Properties.VariableNames{'Var1'} = 'Time';
Table.Properties.VariableNames{'Var2'} = 'Forecast';
Table.Properties.VariableNames{'Var3'} = 'Real';

while not(strcmp(currentDate,finalDate))

    try
        currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
        special_index = find(MTLOG_0100.Date == currentDate);
        forecast_MTLOG_0100 = MTLOG_0100(special_index,2).Forecast{1}(1:7); % Data from UTE.
        currentDate = datestr(currentDate,'yyyymmdd');
    end
    
    for i = 1:length(allWindData)
        if strcmp(allWindData{i}{1},currentDate)
            break;
        end
    end
%     real_ADME = allWindData{i}{2}(7:43); % Data from ADME.
    real_ADME = allWindData{i}{2}(17:53); % Data from ADME with the 100 minutes delay.
    
    forecast_time = linspace(1,7,7);
    real_time     = linspace(1,7,37);
    
    forecast_MTLOG_0100_inter = interp1(forecast_time,forecast_MTLOG_0100,real_time,'linear'); 
    
    aux   = {real_time,forecast_MTLOG_0100_inter,real_ADME};
    Table = [Table;aux];
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    
end

save('MTLOG_0100_and_Real_6h.mat','Table');

%% (4) Plot 22 hrs (from 01:00 to 23:00) for MTLOG_0100:

% We apply the delay in ADME (100 minutes) and save all the 365 plots.
% We do this so after we can join all of them in LaTeX.

MTLOG_0100 = allTablesData{5};

initialDate = '20190101';
currentDate = initialDate;
finalDate   = '20200101';
figure(50);
count = 1;

while not(strcmp(currentDate,finalDate))

    try
        currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
        special_index = find(MTLOG_0100.Date == currentDate);
        forecast_MTLOG_0100 = MTLOG_0100(special_index,2).Forecast{1}(1:23);
        real_MTLOG_0100 = MTLOG_0100(special_index,3).Real{1}(1:23);
        currentDate = datestr(currentDate,'yyyymmdd');
    catch
        currentDate = datestr(currentDate,'yyyymmdd');
    end
    
    for i = 1:length(allWindData)
        if strcmp(allWindData{i}{1},currentDate)
            break;
        end
    end
    real_ADME = allWindData{i}{2}(7:139);
    
    forecast_time = linspace(1,23,23);
    real_time     = linspace(1,23,133);
    
    forecast_MTLOG_0100_inter = interp1(forecast_time,forecast_MTLOG_0100,real_time,'linear'); 
    real_MTLOG_0100_inter = interp1(forecast_time,real_MTLOG_0100,real_time,'linear'); 
    
    set(0,'CurrentFigure',50); clf(50);
    plot(real_time(1:end-9),real_ADME(10:end));
    hold on;
    plot(real_time,real_MTLOG_0100_inter);
    plot(real_time,forecast_MTLOG_0100_inter);
    xlim([1 22]); ylim([0 1400]);
    grid minor; box;
    legend('ADME Real (corrected)','UTE Real','MTLOG\_0100');
    xlabel('Hours (01:00-22:00)'); ylabel('MW'); title(currentDate);
    
    saveas(gcf,[pwd '/someResults/MTLOG_0100_2019/',num2str(count)],'epsc');
    
    pause(0.1)
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = count + 1;
    
end

%% (5) We load the data from (3) to check:

load('MTLOG_0100_and_Real_6h.mat');

forecast = Table.Forecast;
real     = Table.Real;
time     = linspace(1,7,37);

figure(60);
currentDate = '20190101';
count = 1;

for i = 1:length(real)
    
    set(0,'CurrentFigure',60); clf(60);
    plot(time,real{i});
    hold on;
    plot(time,forecast(i,:));
    ylim([0 1400]); grid minor;
    xlabel('Hours (01:00-07:00)'); ylabel('MW'); title(currentDate);
    legend('Real','Forecast');
    
    saveas(gcf,[pwd '/someResults/dataToUse/',num2str(count)],'epsc');
    pause(0.1);
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = count + 1;
    
end

%% (6)-A Preparing the data that we will use (24 hrs) (I corrected the delay):

% It is needed to run the first cell before running this one.
MTLOG_0100 = allTablesData{5};

initialDate = '20190101';
currentDate = initialDate;
finalDate   = '20200101';
isEmpty     = 0;
delay = 9; % delay = 1 means 10 minutes.

Table = cell2table(cell(0,5));
Table.Properties.VariableNames{'Var1'} = 'Time';
Table.Properties.VariableNames{'Var2'} = 'Forecast';
Table.Properties.VariableNames{'Var3'} = 'Real_UTE';
Table.Properties.VariableNames{'Var4'} = 'Real_ADME';
Table.Properties.VariableNames{'Var5'} = 'Date';

while not(strcmp(currentDate,finalDate))

    try
        currentDate         = datetime(currentDate,'InputFormat','yyyyMMdd');
        special_index       = find(MTLOG_0100.Date == currentDate);
        isEmpty             = isempty(special_index); % We check if the date exists in the data.
        forecast_MTLOG_0100 = MTLOG_0100(special_index,2).Forecast{1}(1:25); % Data from UTE.
        real_MTLOG_0100     = MTLOG_0100(special_index,3).Real{1}(1:25); % Data from UTE.
        currentDate         = datestr(currentDate,'yyyymmdd');
    catch error
        disp(error);
        try
            currentDate = datestr(currentDate,'yyyymmdd');
        end
        disp(['Some error in day ',currentDate]);
    end
    
    for i = 1:length(allWindData)
        if strcmp(allWindData{i}{1},currentDate)
            break;
        end
    end
    % We start in the point 7 because we want to start at 01:00 hrs.
    real_ADME = allWindData{i}{2}(7 + delay:end);
    real_ADME = [real_ADME;allWindData{i+1}{2}(1:7 + delay)];
    
    forecast_time = linspace(1,25,25);
    real_time     = linspace(1,25,145);
    
    forecast_MTLOG_0100_inter = interp1(forecast_time,forecast_MTLOG_0100,real_time,'linear'); 
    real_MTLOG_0100_inter     = interp1(forecast_time,real_MTLOG_0100,real_time,'linear'); 
    
    if isEmpty
        % If it is empty, we save all zeros.
        aux = {real_time,0*forecast_MTLOG_0100_inter,0*real_MTLOG_0100_inter,0*real_ADME,currentDate};
    else
        aux = {real_time,forecast_MTLOG_0100_inter,real_MTLOG_0100_inter,real_ADME,currentDate};
    end
    Table = [Table;aux];
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    
end

save('MTLOG_0100_and_Real_24h.mat','Table');

%% (6)-B Preparing the data that we will use (24 hrs) (I corrected the delay):

% It is needed to run the first cell before running this one.
AWSTP_0100 = allTablesData{1};

initialDate = '20190423';
currentDate = initialDate;
finalDate   = '20200101';
isEmpty     = 0;
delay = 9; % delay = 1 means 10 minutes.

Table = cell2table(cell(0,5));
Table.Properties.VariableNames{'Var1'} = 'Time';
Table.Properties.VariableNames{'Var2'} = 'Forecast';
Table.Properties.VariableNames{'Var3'} = 'Real_UTE';
Table.Properties.VariableNames{'Var4'} = 'Real_ADME';
Table.Properties.VariableNames{'Var5'} = 'Date';

while not(strcmp(currentDate,finalDate))

    try
        currentDate         = datetime(currentDate,'InputFormat','yyyyMMdd');
        special_index       = find(AWSTP_0100.Date == currentDate);
        isEmpty             = isempty(special_index); % We check if the date exists in the data.
        forecast_AWSTP_0100 = AWSTP_0100(special_index,2).Forecast{1}(1:25); % Data from UTE.
        real_AWSTP_0100     = AWSTP_0100(special_index,3).Real{1}(1:25); % Data from UTE.
        currentDate         = datestr(currentDate,'yyyymmdd');
    catch error
        disp(error);
        try
            currentDate = datestr(currentDate,'yyyymmdd');
        end
        disp(['Some error in day ',currentDate]);
    end
    
    for i = 1:length(allWindData)
        if strcmp(allWindData{i}{1},currentDate)
            break;
        end
    end
    % We start in the point 7 because we want to start at 01:00 hrs.
    real_ADME = allWindData{i}{2}(7 + delay:end);
    real_ADME = [real_ADME;allWindData{i+1}{2}(1:7 + delay)];
    
    forecast_time = linspace(1,25,25);
    real_time     = linspace(1,25,145);
    
    forecast_AWSTP_0100_inter = interp1(forecast_time,forecast_AWSTP_0100,real_time,'linear'); 
    real_AWSTP_0100_inter     = interp1(forecast_time,real_AWSTP_0100,real_time,'linear'); 
    
    if isEmpty
        % If it is empty, we save all zeros.
        aux = {real_time,0*forecast_AWSTP_0100_inter,0*real_AWSTP_0100_inter,0*real_ADME,currentDate};
    else
        aux = {real_time,forecast_AWSTP_0100_inter,real_AWSTP_0100_inter,real_ADME,currentDate};
    end
    Table = [Table;aux];
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    
end

save('AWSTP_0100_and_Real_24h.mat','Table');

%% (6)-C Preparing the data that we will use (24 hrs) (I corrected the delay):

% It is needed to run the first cell before running this one.
UTEP5_0100 = allTablesData{9};

initialDate = '20190101';
currentDate = initialDate;
finalDate   = '20200101';
isEmpty     = 0;
delay = 9; % delay = 1 means 10 minutes.

Table = cell2table(cell(0,5));
Table.Properties.VariableNames{'Var1'} = 'Time';
Table.Properties.VariableNames{'Var2'} = 'Forecast';
Table.Properties.VariableNames{'Var3'} = 'Real_UTE';
Table.Properties.VariableNames{'Var4'} = 'Real_ADME';
Table.Properties.VariableNames{'Var5'} = 'Date';

while not(strcmp(currentDate,finalDate))

    try
        currentDate         = datetime(currentDate,'InputFormat','yyyyMMdd');
        special_index       = find(UTEP5_0100.Date == currentDate);
        isEmpty             = isempty(special_index); % We check if the date exists in the data.
        forecast_UTEP5_0100 = UTEP5_0100(special_index,2).Forecast{1}(1:25); % Data from UTE.
        real_UTEP5_0100     = UTEP5_0100(special_index,3).Real{1}(1:25); % Data from UTE.
        currentDate         = datestr(currentDate,'yyyymmdd');
    catch error
        disp(error);
        try
            currentDate = datestr(currentDate,'yyyymmdd');
        end
        disp(['Some error in day ',currentDate]);
    end
    
    for i = 1:length(allWindData)
        if strcmp(allWindData{i}{1},currentDate)
            break;
        end
    end
    % We start in the point 7 because we want to start at 01:00 hrs.
    real_ADME = allWindData{i}{2}(7 + delay:end);
    real_ADME = [real_ADME;allWindData{i+1}{2}(1:7 + delay)];
    
    forecast_time = linspace(1,25,25);
    real_time     = linspace(1,25,145);
    
    forecast_UTEP5_0100_inter = interp1(forecast_time,forecast_UTEP5_0100,real_time,'linear'); 
    real_UTEP5_0100_inter     = interp1(forecast_time,real_UTEP5_0100,real_time,'linear'); 
    
    if isEmpty
        % If it is empty, we save all zeros.
        aux = {real_time,0*forecast_UTEP5_0100_inter,0*real_UTEP5_0100_inter,0*real_ADME,currentDate};
    else
        aux = {real_time,forecast_UTEP5_0100_inter,real_UTEP5_0100_inter,real_ADME,currentDate};
    end
    Table = [Table;aux];
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    
end

save('UTEP5_0100_and_Real_24h.mat','Table');

%% (7)-A We load the data from (6) to check and save all the plots:

load('MTLOG_0100_and_Real_24h.mat');

forecast  = Table.Forecast;
real_ute  = Table.Real_UTE;
real_adme = Table.Real_ADME;
time      = linspace(1,25,145);

figure(70);
currentDate = '20190101';
count = 1;

for i = 1:length(real_adme)
    
    set(0,'CurrentFigure',70); clf(70);
    P = plot(time,real_ute(i,:)); P.LineWidth = 1;
    hold on;
    P = plot(time,real_adme{i});  P.LineWidth = 1;
    P = plot(time,forecast(i,:)); P.LineWidth = 1;
    ylim([0 1400]); grid minor;
    xlabel('Hours (24 hrs starting at 01:00)'); ylabel('MW'); title(currentDate);
    xlim([1 25]);
    legend('Real UTE','Real ADME','Forecast');
    
    saveas(gcf,[pwd '/someResults/dataToUse_24/',num2str(count)],'epsc');
    pause(0.1);
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = count + 1;
    
end

%% (7)-B We load the data from (6)-B to check and save all the plots:

load('AWSTP_0100_and_Real_24h.mat');

forecast  = Table.Forecast;
real_ute  = Table.Real_UTE;
real_adme = Table.Real_ADME;
time      = linspace(1,25,145);

figure(70);
currentDate = '20190423';
count = 1;

for i = 1:length(real_adme)
    
    set(0,'CurrentFigure',70); clf(70);
    P = plot(time,real_ute(i,:)); P.LineWidth = 1;
    hold on;
    P = plot(time,real_adme{i});  P.LineWidth = 1;
    P = plot(time,forecast(i,:)); P.LineWidth = 1;
    ylim([0 1400]); grid minor;
    xlabel('Hours (24 hrs starting at 01:00)'); ylabel('MW'); title(currentDate);
    xlim([1 25]);
    legend('Real UTE','Real ADME','Forecast');
    
    saveas(gcf,[pwd '/someResults/dataToUse_24-B/',num2str(count)],'epsc');
    pause(0.1);
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = count + 1;
    
end

%% (7)-C We load the data from (6)-C to check and save all the plots:

load('UTEP5_0100_and_Real_24h.mat');

forecast  = Table.Forecast;
real_ute  = Table.Real_UTE;
real_adme = Table.Real_ADME;
time      = linspace(1,25,145);

figure(70);
currentDate = '20190101';
count = 1;

for i = 1:length(real_adme)
    
    set(0,'CurrentFigure',70); clf(70);
    P = plot(time,real_ute(i,:)); P.LineWidth = 1;
    hold on;
    P = plot(time,real_adme{i});  P.LineWidth = 1;
    P = plot(time,forecast(i,:)); P.LineWidth = 1;
    ylim([0 1400]); grid minor;
    xlabel('Hours (24 hrs starting at 01:00)'); ylabel('MW'); title(currentDate);
    xlim([1 25]);
    legend('Real UTE','Real ADME','Forecast');
    
    saveas(gcf,[pwd '/someResults/dataToUse_24-C/',num2str(count)],'epsc');
    pause(0.1);
    
    currentDate = datetime(currentDate,'InputFormat','yyyyMMdd');
    currentDate = currentDate + days(1);
    currentDate = datestr(currentDate,'yyyymmdd');
    count = count + 1;
    
end

%% (8)-A Statistical analysis UTE Vs. ADME real productions:

close all;
clear all;
clc;

load('MTLOG_0100_and_Real_24h.mat');

forecast      = Table.Forecast;
real_ute      = Table.Real_UTE;
real_adme     = Table.Real_ADME;
time          = linspace(1,25,145);
areZero       = [];
errorToRemove = [];
correctDates  = {};

for i = 1:length(real_adme)
    
    ute_i  = real_ute(i,:);
    adme_i = real_adme{i}';
    
    % In this analisys I am assuing MAX_WIND = 1400 MW.
    norm_wind         = 1474;
    relative_error(i) = sum(ute_i-adme_i) / (length(ute_i)*norm_wind);
    if relative_error(i) == 0 || relative_error(i) >= 0.007 || relative_error(i) <= -0.013
        errorToRemove(end+1) = i;
    end
    if relative_error(i) == 0
        areZero(end+1) = i;
    end

end

histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/all2019'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/all2019'],'epsc');
pause(0.1);

% We remove the values when all are zeros or error >= 0.025:
for i = length(errorToRemove):-1:1
    relative_error(errorToRemove(i)) = [];
    Table(errorToRemove(i),:)        = [];
end

figure;
histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/partially2019'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/partially2019'],'epsc');
pause(0.1);

disp(['In total, ',num2str(length(areZero)),' have not available data.']);
disp(['In total, ',num2str(length(errorToRemove)-length(areZero)),' have error >= 0.007 or error <= -0.013.']);
disp(['We work with ',num2str(length(relative_error)),' days from 2019.']);

save('MTLOG_0100_and_Real_24h_Corrected.mat','Table');

%% (8)-B Statistical analysis UTE Vs. ADME real productions:

close all;
clear all;
clc;

load('AWSTP_0100_and_Real_24h.mat');

forecast      = Table.Forecast;
real_ute      = Table.Real_UTE;
real_adme     = Table.Real_ADME;
time          = linspace(1,25,145);
areZero       = [];
errorToRemove = [];
correctDates  = {};

for i = 1:length(real_adme)
    
    ute_i  = real_ute(i,:);
    adme_i = real_adme{i}';
    
    % In this analisys I am assuing MAX_WIND = 1400 MW.
    norm_wind         = 1474;
    relative_error(i) = sum(ute_i-adme_i) / (length(ute_i)*norm_wind);
    if relative_error(i) == 0 || relative_error(i) >= 0.007 || relative_error(i) <= -0.013
        errorToRemove(end+1) = i;
    end
    if relative_error(i) == 0
        areZero(end+1) = i;
    end

end

histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/all2019-B'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/all2019-B'],'epsc');
pause(0.1);

% We remove the values when all are zeros or error >= 0.025:
for i = length(errorToRemove):-1:1
    relative_error(errorToRemove(i)) = [];
    Table(errorToRemove(i),:)        = [];
end

figure;
histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/partially2019-B'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/partially2019-B'],'epsc');
pause(0.1);

disp(['In total, ',num2str(length(areZero)),' have not available data.']);
disp(['In total, ',num2str(length(errorToRemove)-length(areZero)),' have error >= 0.007 or error <= -0.013.']);
disp(['We work with ',num2str(length(relative_error)),' days from 2019.']);

save('AWSTP_0100_and_Real_24h_Corrected.mat','Table');

%% (8)-C Statistical analysis UTE Vs. ADME real productions:

close all;
clear all;
clc;

load('UTEP5_0100_and_Real_24h.mat');

forecast      = Table.Forecast;
real_ute      = Table.Real_UTE;
real_adme     = Table.Real_ADME;
time          = linspace(1,25,145);
areZero       = [];
errorToRemove = [];
correctDates  = {};

for i = 1:length(real_adme)
    
    ute_i  = real_ute(i,:);
    adme_i = real_adme{i}';
    
    % In this analisys I am assuing MAX_WIND = 1400 MW.
    norm_wind         = 1474;
    relative_error(i) = sum(ute_i-adme_i) / (length(ute_i)*norm_wind);
    if relative_error(i) == 0 || relative_error(i) >= 0.007 || relative_error(i) <= -0.013
        errorToRemove(end+1) = i;
    end
    if relative_error(i) == 0
        areZero(end+1) = i;
    end

end

histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/all2019-C'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/all2019-C'],'epsc');
pause(0.1);

% We remove the values when all are zeros or error >= 0.025:
for i = length(errorToRemove):-1:1
    relative_error(errorToRemove(i)) = [];
    Table(errorToRemove(i),:)        = [];
end

figure;
histogram(relative_error,100);
grid minor;
title('Relative error between sources');
saveas(gcf,[pwd '/someResults/histograms/partially2019-C'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/partially2019-C'],'epsc');
pause(0.1);

disp(['In total, ',num2str(length(areZero)),' have not available data.']);
disp(['In total, ',num2str(length(errorToRemove)-length(areZero)),' have error >= 0.007 or error <= -0.013.']);
disp(['We work with ',num2str(length(relative_error)),' days from 2019.']);

save('UTEP5_0100_and_Real_24h_Corrected.mat','Table');

%% (9) We load the data from (8) to check and save all the plots:

close all;
clear all;
clc;

load('MTLOG_0100_and_Real_24h_Corrected.mat');

forecast  = Table.Forecast;
real_ute  = Table.Real_UTE;
real_adme = Table.Real_ADME;
%time      = linspace(1,25,145);
time      = linspace(0,1,145);
norm_wind = 1474;

figure(80);
count = 1;

for i = 1:length(real_adme)
    
    set(0,'CurrentFigure',80); clf(80);
    P = plot(time,real_ute(i,:)/norm_wind); P.LineWidth = 1;
    hold on;
    P = plot(time,real_adme{i}/norm_wind);  P.LineWidth = 1;
    P = plot(time,forecast(i,:)/norm_wind); P.LineWidth = 1;
    ylim([0 1]); grid minor;
    xlabel('Time'); ylabel('Power'); title(Table.Date(i));
    xlim([0 1]);
    legend('Real UTE','Real ADME','Forecast');
    
    saveas(gcf,[pwd '/someResults/dataToUse_24_corrected/',num2str(count)],'epsc');
    pause(0.1);
    
    count = count + 1;
    
end

%% (10)-A Final process of the correct data created in (8)-A:

close all;
clear all;
clc;

load('MTLOG_0100_and_Real_24h_Corrected.mat');

Table_Training = Table;
Table_Testing  = Table;
switching      = 1; % We use this variable to choose from which table to remove.

for i = height(Table):-1:1
    
    if switching == 1
        Table_Training(i,:) = [];
    elseif switching == -1
        Table_Testing(i,:) = [];
    end
    
    switching = - switching;
    
end

% Above, we created two tables. One with the data that will be used for
% training, and the other will be used for testing.

Table_Training_Complete = cell2table(cell(0,10));
Table_Training_Complete.Properties.VariableNames{'Var1'}  = 'Date';
Table_Training_Complete.Properties.VariableNames{'Var2'}  = 'Time';
Table_Training_Complete.Properties.VariableNames{'Var3'}  = 'Forecast';
Table_Training_Complete.Properties.VariableNames{'Var4'}  = 'Forecast_Dot';
Table_Training_Complete.Properties.VariableNames{'Var5'}  = 'Real_UTE';
Table_Training_Complete.Properties.VariableNames{'Var6'}  = 'Real_ADME';
Table_Training_Complete.Properties.VariableNames{'Var7'}  = 'Error';
Table_Training_Complete.Properties.VariableNames{'Var8'}  = 'Error_Transitions';
Table_Training_Complete.Properties.VariableNames{'Var9'}  = 'Error_Lamp';
Table_Training_Complete.Properties.VariableNames{'Var10'} = 'Error_Lamp_Transitions';

Table_Testing_Complete = Table_Training_Complete; % We copy the table.
Table_Complete         = Table_Training_Complete; % We copy the table.

Delta_T   = 1/144; % We normalize the time, then the transitions last 1/144.
norm_wind = 1474;

theta_0 = 2.2;
alpha   = 0.038;

for i = 1:height(Table)

    p     = Table.Forecast(i,:)/norm_wind;
    x     = Table.Real_ADME(i,:);
    x_ute = Table.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Complete = [Table_Complete;aux];
    
end

for i = 1:height(Table_Training)

    p     = Table_Training.Forecast(i,:)/norm_wind;
    x     = Table_Training.Real_ADME(i,:);
    x_ute = Table_Training.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Training.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Training_Complete = [Table_Training_Complete;aux];
    
end

for i = 1:height(Table_Testing)

    p     = Table_Testing.Forecast(i,:)/norm_wind;
    x     = Table_Testing.Real_ADME(i,:);
    x_ute = Table_Testing.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Testing.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Testing_Complete = [Table_Testing_Complete;aux];
    
end

save('MTLOG_0100_and_Real_24h_Training_Data.mat','Table_Training_Complete');
save('MTLOG_0100_and_Real_24h_Testing_Data.mat', 'Table_Testing_Complete');
save('MTLOG_0100_and_Real_24h_Complete_Data.mat', 'Table_Complete');

writetable(Table_Training_Complete,'Table_Training_Complete.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_Complete.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete.csv','Delimiter',',','QuoteStrings',true)

%% (10)-B Final process of the correct data created in (8)-B:

close all;
clear all;
clc;

load('AWSTP_0100_and_Real_24h_Corrected.mat');

Table_Training = Table;
Table_Testing  = Table;
switching      = 1; % We use this variable to choose from which table to remove.

for i = height(Table):-1:1
    
    if switching == 1
        Table_Training(i,:) = [];
    elseif switching == -1
        Table_Testing(i,:) = [];
    end
    
    switching = - switching;
    
end

% Above, we created two tables. One with the data that will be used for
% training, and the other will be used for testing.

Table_Training_Complete = cell2table(cell(0,10));
Table_Training_Complete.Properties.VariableNames{'Var1'}  = 'Date';
Table_Training_Complete.Properties.VariableNames{'Var2'}  = 'Time';
Table_Training_Complete.Properties.VariableNames{'Var3'}  = 'Forecast';
Table_Training_Complete.Properties.VariableNames{'Var4'}  = 'Forecast_Dot';
Table_Training_Complete.Properties.VariableNames{'Var5'}  = 'Real_UTE';
Table_Training_Complete.Properties.VariableNames{'Var6'}  = 'Real_ADME';
Table_Training_Complete.Properties.VariableNames{'Var7'}  = 'Error';
Table_Training_Complete.Properties.VariableNames{'Var8'}  = 'Error_Transitions';
Table_Training_Complete.Properties.VariableNames{'Var9'}  = 'Error_Lamp';
Table_Training_Complete.Properties.VariableNames{'Var10'} = 'Error_Lamp_Transitions';

Table_Testing_Complete = Table_Training_Complete; % We copy the table.
Table_Complete         = Table_Training_Complete; % We copy the table.

Delta_T   = 1/144; % We normalize the time, then the transitions last 1/144.
norm_wind = 1474;

theta_0 = 2.2;
alpha   = 0.038;

for i = 1:height(Table)

    p     = Table.Forecast(i,:)/norm_wind;
    x     = Table.Real_ADME(i,:);
    x_ute = Table.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Complete = [Table_Complete;aux];
    
end

for i = 1:height(Table_Training)

    p     = Table_Training.Forecast(i,:)/norm_wind;
    x     = Table_Training.Real_ADME(i,:);
    x_ute = Table_Training.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Training.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Training_Complete = [Table_Training_Complete;aux];
    
end

for i = 1:height(Table_Testing)

    p     = Table_Testing.Forecast(i,:)/norm_wind;
    x     = Table_Testing.Real_ADME(i,:);
    x_ute = Table_Testing.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Testing.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Testing_Complete = [Table_Testing_Complete;aux];
    
end

save('AWSTP_0100_and_Real_24h_Training_Data.mat','Table_Training_Complete');
save('AWSTP_0100_and_Real_24h_Testing_Data.mat', 'Table_Testing_Complete');
save('AWSTP_0100_and_Real_24h_Complete_Data.mat', 'Table_Complete');

writetable(Table_Training_Complete,'Table_Training_Complete-B.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_Complete-B.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete-B.csv','Delimiter',',','QuoteStrings',true)

%% (10)-C Final process of the correct data created in (8)-C:

close all;
clear all;
clc;

load('UTEP5_0100_and_Real_24h_Corrected.mat');

Table_Training = Table;
Table_Testing  = Table;
switching      = 1; % We use this variable to choose from which table to remove.

for i = height(Table):-1:1
    
    if switching == 1
        Table_Training(i,:) = [];
    elseif switching == -1
        Table_Testing(i,:) = [];
    end
    
    switching = - switching;
    
end

% Above, we created two tables. One with the data that will be used for
% training, and the other will be used for testing.

Table_Training_Complete = cell2table(cell(0,10));
Table_Training_Complete.Properties.VariableNames{'Var1'}  = 'Date';
Table_Training_Complete.Properties.VariableNames{'Var2'}  = 'Time';
Table_Training_Complete.Properties.VariableNames{'Var3'}  = 'Forecast';
Table_Training_Complete.Properties.VariableNames{'Var4'}  = 'Forecast_Dot';
Table_Training_Complete.Properties.VariableNames{'Var5'}  = 'Real_UTE';
Table_Training_Complete.Properties.VariableNames{'Var6'}  = 'Real_ADME';
Table_Training_Complete.Properties.VariableNames{'Var7'}  = 'Error';
Table_Training_Complete.Properties.VariableNames{'Var8'}  = 'Error_Transitions';
Table_Training_Complete.Properties.VariableNames{'Var9'}  = 'Error_Lamp';
Table_Training_Complete.Properties.VariableNames{'Var10'} = 'Error_Lamp_Transitions';

Table_Testing_Complete = Table_Training_Complete; % We copy the table.
Table_Complete         = Table_Training_Complete; % We copy the table.

Delta_T   = 1/144; % We normalize the time, then the transitions last 1/144.
norm_wind = 1474;

theta_0 = 2.2;
alpha   = 0.038;

for i = 1:height(Table)

    p     = Table.Forecast(i,:)/norm_wind;
    x     = Table.Real_ADME(i,:);
    x_ute = Table.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Complete = [Table_Complete;aux];
    
end

for i = 1:height(Table_Training)

    p     = Table_Training.Forecast(i,:)/norm_wind;
    x     = Table_Training.Real_ADME(i,:);
    x_ute = Table_Training.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Training.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Training_Complete = [Table_Training_Complete;aux];
    
end

for i = 1:height(Table_Testing)

    p     = Table_Testing.Forecast(i,:)/norm_wind;
    x     = Table_Testing.Real_ADME(i,:);
    x_ute = Table_Testing.Real_UTE(i,:)/norm_wind;
    x     = x{1}'/norm_wind;
    v     = x - p;
    lp    = -(sqrt(2/(alpha*theta_0)))*asin(sqrt(1-v-p)); % Lamperti Transform.
    for j = 1:length(x)-1
        p_dot(j)   = (p(j+1)-p(j)) / Delta_T;
        DeltaV(j)  = v(j+1) - v(j);
        lp_tran(j) = lp(j+1) - lp(j); % Lamperti Transform Transition.
    end
    t    = linspace(0,1,145);
    date = Table_Testing.Date(i);
    date = date{1};
    
    aux                     = {date,t,p,p_dot,x_ute,x,v,DeltaV,lp,lp_tran};
    Table_Testing_Complete = [Table_Testing_Complete;aux];
    
end

save('UTEP5_0100_and_Real_24h_Training_Data.mat','Table_Training_Complete');
save('UTEP5_0100_and_Real_24h_Testing_Data.mat', 'Table_Testing_Complete');
save('UTEP5_0100_and_Real_24h_Complete_Data.mat', 'Table_Complete');

writetable(Table_Training_Complete,'Table_Training_Complete-C.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_Complete-C.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete-C.csv','Delimiter',',','QuoteStrings',true)

%% (11) We load the data from (10) to check and save all the plots.

close all;
clear all;
clc;

allDaysPlots = 0;

load('MTLOG_0100_and_Real_24h_Training_Data.mat'); % Data from (10).
load('MTLOG_0100_and_Real_24h_Testing_Data.mat'); % Data from (10).
load('MTLOG_0100_and_Real_24h_Complete_Data.mat'); % Data from (10).

if allDaysPlots
    figure(90);
end

count = 1;
aux_conter = 1;

Forecast          = Table_Complete.Forecast;
Forecast_Dot      = Table_Complete.Forecast_Dot;
real_ADME         = Table_Complete.Real_ADME;
Error             = Table_Complete.Error;
Error_Transitions = Table_Complete.Error_Transitions;
Lamparti_Data     = Table_Complete.Error_Lamp;
Lamparti_Tran     = Table_Complete.Error_Lamp_Transitions;

dt                 = Table_Complete.Time(1,2);
New_Transform_Data = [];
New_Transform_Tran = [];
t_ticks            = [13:1/6:37]/24;

h_error = [];
m_error = [];
l_error = [];
h_tran  = [];
m_tran  = [];
l_tran  = [];
h_error_Lam = [];
m_error_Lam = [];
l_error_Lam = [];
h_tran_Lam  = [];
m_tran_Lam  = [];
l_tran_Lam  = [];

error = [];

time_1 = linspace(0,1,145);
time_2 = linspace(0,1-1/144,144);

for i = 1:height(Table_Complete)
    
    for j = 1:length(real_ADME(i,:))
                
        if j ~= length(real_ADME(i,:))
            New_Transform_Data(i,j) = (Lamparti_Data(i,j+1) - Lamparti_Data(i,j)) / sqrt(dt);
            if j ~= length(real_ADME(i,:)) - 1
                New_Transform_Tran(i,j) = (Lamparti_Data(i,j+2) - 2*Lamparti_Data(i,j+1)...
                    + Lamparti_Data(i,j)) / sqrt(dt);
            end
        end
        
        if real_ADME(i,j) < 0.3
            l_error(end+1)     = Error(i,j);
            l_error_Lam(end+1) = Lamparti_Data(i,j);
            if j ~= length(real_ADME(i,:))
                l_tran(end+1)     = Error_Transitions(i,j);
                l_tran_Lam(end+1) = Lamparti_Tran(i,j);
            end
        elseif real_ADME(i,j) >= 0.3 && real_ADME(i,j) < 0.6
            m_error(end+1)     = Error(i,j);
            m_error_Lam(end+1) = Lamparti_Data(i,j);
            if j ~= length(real_ADME(i,:))
                m_tran(end+1) = Error_Transitions(i,j);
                m_tran_Lam(end+1) = Lamparti_Tran(i,j);
            end
        else
            h_error(end+1)     = Error(i,j);
            h_error_Lam(end+1) = Lamparti_Data(i,j);
            if j ~= length(real_ADME(i,:))
                h_tran(end+1) = Error_Transitions(i,j);
                h_tran_Lam(end+1) = Lamparti_Tran(i,j);
            end
        end
        
    end
    
    allError   (i,:) = Table_Complete.Error(i,:);
    dailyError (i,:) = abs(Table_Complete.Error(i,:));
    error(i)         = sum(abs(Table_Complete.Error(i,:)))/145;
    
    if 1 == allDaysPlots % Here we plot and save the daily data for all the days.
    
        set(0,'CurrentFigure',90); clf(90);
        P = plot(t_ticks,Forecast(i,:)); P.LineWidth = 1;
        hold on;
        P = plot(t_ticks,real_ADME(i,:)); P.LineWidth = 1;
        xlabel('Time'); ylabel('Power'); 
        xticks([13:37]/24);
        datetick('x','HHPM','keepticks');
        xtickangle(90);
        date_format = datetime(Table_Complete.Date(i),'InputFormat','yyyyMMdd');
        date_format_next = date_format + days(1);
        title([datestr(date_format),' and ',datestr(date_format_next)]);
%         xlim([0 1]); 
        ylim([0 1]); 
        grid minor;
        legend('Forecast','Real Production');
        saveas(gcf,[pwd '/someResults/final/',num2str(count)],'epsc');
        saveas(gcf,[pwd '/someResults/forPaper/allDaysPlots/',num2str(aux_conter)],'epsc');
        aux_conter = aux_conter + 1;
        pause(0.1);

        set(0,'CurrentFigure',90); clf(90);
        P = plot(time_1,Error(i,:)); P.LineWidth = 1;
        xlabel('Time'); title(Table_Complete.Date(i));
        xlim([0 1]); ylim([-0.5 0.5]); grid minor;
        legend('Forecast Error');
        saveas(gcf,[pwd '/someResults/final/',num2str(count+1)],'epsc');
        pause(0.1);

        set(0,'CurrentFigure',90); clf(90);
        P = plot(time_2,Error_Transitions(i,:)); P.LineWidth = 1;
        xlabel('Time'); title(Table_Complete.Date(i));
        xlim([0 1]); ylim([-0.5 0.5]); grid minor;
        legend('Forecast Error Transition');
        saveas(gcf,[pwd '/someResults/final/',num2str(count+2)],'epsc');
        pause(0.1);

        set(0,'CurrentFigure',90); clf(90);
        P = plot(time_2,Forecast_Dot(i,:)); P.LineWidth = 1;
        xlabel('Time'); title(Table_Complete.Date(i));
        xlim([0 1]); ylim([-2 2]); grid minor;
        legend('Forecast Derivative');
        saveas(gcf,[pwd '/someResults/final/',num2str(count+3)],'epsc');
        pause(0.1);
    
    end
    
    count = count + 4;

end

for i = 1:145
    averagedDailyError(i) = mean(dailyError(:,i));
end

for i = 0:floor(height(Table_Complete) / 7) - 1
    weeklyMAE(i+1)  = mean(error( 1+i*7 : 7+i*7 ));
    weeklyTime(i+1) = i*7;
end

figure;
P = plot(error); P.LineWidth = 1;
hold on;
P = plot(weeklyTime,weeklyMAE,'*-'); P.LineWidth = 2;
xlim([1 length(error)]);
grid minor; title('Mean Absolute Error (Real Vs. Forecast)');
xlabel('Day');
legend('Daily MAE','Weekly MAE');
saveas(gcf,[pwd '/someResults/final/seasons'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/seasons'],'epsc');

figure;
P = plot(linspace(0,24,145),averagedDailyError); P.LineWidth = 1;
xlim([0 24]);
grid minor; title('Mean Absolute Error (Real Vs. Forecast)');
xlabel('Hour (from 00:00 to 24:00)');
legend('Houlry MAE');
saveas(gcf,[pwd '/someResults/final/hourlyEffect'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/hourlyEffect'],'epsc');

% FORECAST ERROR (NO TRANSITIONS):

figure; % LOW FORECAST ERROR:
histogram(l_error); grid minor; title('Low Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/LP'],'epsc');

figure; % MID FORECAST ERROR:
histogram(m_error); grid minor; title('Mid Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/MP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/MP'],'epsc');

figure; % HIGH FORECAST ERROR:
histogram(h_error); grid minor; title('High Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/HP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/HP'],'epsc');

figure; % ALL FORECAST ERROR:
histogram(Error); grid minor; title('All Power');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/AP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/AP'],'epsc');

% FORECAST ERROR AFTER LP:

figure; % LOW FORECAST ERROR AFTER LP:
histogram(l_error_Lam); grid minor; title('Low Power Range');
xlabel('Forecast Error (after LT)');
saveas(gcf,[pwd '/someResults/final/LP_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/LP_LP'],'epsc');

figure; % MID FORECAST ERROR AFTER LP:
histogram(m_error_Lam); grid minor; title('Mid Power Range');
xlabel('Forecast Error (after LT)');
saveas(gcf,[pwd '/someResults/final/MP_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/MP_LP'],'epsc');

figure; % HIGH FORECAST ERROR AFTER LP:
histogram(h_error_Lam); grid minor; title('High Power Range');
xlabel('Forecast Error (after LT)');
saveas(gcf,[pwd '/someResults/final/HP_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/HP_LP'],'epsc');

figure; % ALL FORECAST ERROR AFTER LP:
histogram(Lamparti_Data); grid minor; title('All Power');
xlabel('Forecast Error (after LT)');
saveas(gcf,[pwd '/someResults/final/AP_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/AP_LP'],'epsc');

% FORECAST ERROR TRANSITIONS:

figure; % LOW FORECAST TRANSITIONS:
histogram(l_tran); grid minor; title('Low Power Range');
xlabel('Forecast Error Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/LP_t'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/LP_t'],'epsc');

figure; % MID FORECAST TRANSITIONS:
histogram(m_tran); grid minor; title('Mid Power Range');
xlabel('Forecast Error Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/MP_t'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/MP_t'],'epsc');

figure; % HIGH FORECAST TRANSITIONS:
histogram(h_tran); grid minor; title('High Power Range');
xlabel('Forecast Error Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/HP_t'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/HP_t'],'epsc');

figure; % ALL FORECAST TRANSITIONS:
histogram(Error_Transitions); grid minor; title('All Power');
xlabel('Forecast Error Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/AP_t'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/AP_t'],'epsc');

% FORECAST ERROR TRANSITIONS AFTER LP:

figure; % LOW FORECAST TRANSITIONS AFTER LP:
histogram(l_tran_Lam); grid minor; title('Low Power Range');
xlabel('Forecast Error Transitions (after LT)');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/LP_t_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/LP_t_LP'],'epsc');

figure; % MID FORECAST TRANSITIONS AFTER LP:
histogram(m_tran_Lam); grid minor; title('Mid Power Range');
xlabel('Forecast Error Transitions (after LT)');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/MP_t_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/MP_t_LP'],'epsc');

figure; % HIGH FORECAST TRANSITIONS AFTER LP:
histogram(h_tran_Lam); grid minor; title('High Power Range');
xlabel('Forecast Error Transitions (after LT)');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/HP_t_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/HP_t_LP'],'epsc');

figure; % ALL FORECAST TRANSITIONS AFTER LP:
histogram(Lamparti_Tran);
grid minor; title('All Power');
xlabel('Forecast Error Transitions (after LT)');
% xlim([-0.05 0.05]);
% xlim([-0.4 0.4]);
saveas(gcf,[pwd '/someResults/final/AP_t_LP'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/AP_t_LP'],'epsc');

% TRANSITIONS COMPARISON:

figure; % LOW TRANSITIONS COMPARISON:
h1 = histogram(l_tran,200);
hold on; grid minor; title('Low Power');
h2 = histogram(l_tran_Lam,200);
% for i = -0.05:0.01:0.05
%     xline(i,'r');
% end
% for i = 0.01:0.01:0.05
%     yline(i,'r');
% end
h1.Normalization = 'probability';
h2.Normalization = 'probability';
xlabel('Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/LP_comp'],'epsc');

figure; % MID TRANSITIONS COMPARISON:
h1 = histogram(m_tran,200);
hold on; grid minor; title('Mid Power');
h2 = histogram(m_tran_Lam,200);
% for i = -0.05:0.01:0.05
%     xline(i,'r');
% end
% for i = 0.01:0.01:0.05
%     yline(i,'r');
% end
h1.Normalization = 'probability';
h2.Normalization = 'probability';
xlabel('Transitions');
% xlim([-0.05 0.05]);
saveas(gcf,[pwd '/someResults/final/MP_comp'],'epsc');

figure; % HIGH TRANSITIONS COMPARISON:
h1 = histogram(h_tran,200);
hold on; grid minor; title('High Power');
h2 = histogram(h_tran_Lam,200);
% for i = -0.05:0.01:0.05
%     xline(i,'r');
% end
% for i = 0.01:0.01:0.04
%     yline(i,'r');
% end
h1.Normalization = 'probability';
h2.Normalization = 'probability';
xlabel('Transitions');
% xlim([-0.05 0.05]);
% xlim([-0.3 0.3]);
saveas(gcf,[pwd '/someResults/final/HP_comp'],'epsc');

figure; % ALL TRANSITIONS COMPARISON:
h1 = histogram(Error_Transitions,200);
hold on; grid minor; title('All Power');
h2 = histogram(Lamparti_Tran,200);
% for i = -0.05:0.01:0.05
%     xline(i,'r');
% end
% for i = 0.01:0.01:0.07
%     yline(i,'r');
% end
h1.Normalization = 'pdf';
h2.Normalization = 'pdf';
xlabel('Transitions');
% xlim([-0.05 0.05]);
xlim([-0.3 0.3]);
saveas(gcf,[pwd '/someResults/final/AP_comp'],'epsc');

% >>> Gaussian Approximation:

% 1) Transitions histograms.
% 2) Only error histogram.
% 3) Only Lamperti histogram.

figure('Renderer', 'painters', 'Position', [10 10 1500 900]);
h1 = histogram(Error_Transitions,200);
hold on; grid minor; title('Error and Lamperti Transitions');
h2 = histogram(Lamparti_Tran,200);
h1.Normalization = 'pdf';
h2.Normalization = 'pdf';
xlabel('Value of Transition');
ylabel('Probability');
xlim([-0.5 0.5]);
std_of_1  = std(Error_Transitions(:));
mean_of_1 = mean(Error_Transitions(:));
std_of_2  = std(Lamparti_Tran(:));
mean_of_2 = mean(Lamparti_Tran(:));
std_of_3  = std(New_Transform_Tran(:));
mean_of_3 = mean(New_Transform_Tran(:));
x_lim  = [-0.5:0.001:0.5];
x_lim3 = [-10:0.01:10];
y1     = normpdf(x_lim,mean_of_1,std_of_1/1);
y2     = normpdf(x_lim,mean_of_2,std_of_2/1);
y3     = normpdf(x_lim3,mean_of_3,std_of_3/1);
P = plot(x_lim,y1,'b'); P.LineWidth = 2;
P = plot(x_lim,y2,'r'); P.LineWidth = 2;
legend('Error Transitions Histogram','Lamperti Transitions Histogram',...
    'Error Transitions Gaussian Approx.','Lamperti Transitions Gaussian Approx.');
set(gca,'FontSize',18);
saveas(gcf,[pwd '/someResults/final/Gauss_Approx'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx'],'epsc');


figure;
h1 = histogram(Error_Transitions,200);
hold on; grid minor; title('Error Transitions');
h1.Normalization = 'pdf';
xlabel('Value of Transition');
ylabel('Probability');
xlim([-0.1 0.1]);
P = plot(x_lim,y1,'b'); P.LineWidth = 2;
legend('Error Transitions Histogram','Error Transitions Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Err'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_Err'],'epsc');

figure;
h2 = histogram(Lamparti_Tran,200);
hold on; grid minor; title('Lamperti Transitions');
h2.Normalization = 'pdf';
h2.FaceColor = '#D95319';
xlabel('Value of Transition');
ylabel('Probability');
xlim([-0.5 0.5]);
P = plot(x_lim,y2,'r'); P.LineWidth = 2;
legend('Lamperti Transitions Histogram','Lamperti Transitions Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Lam'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_Lam'],'epsc');

figure;
h3 = histogram(New_Transform_Tran,200);
hold on; grid minor; title('New-Transform Transitions');
h3.Normalization = 'pdf';
h3.FaceColor = '#77AC30';
xlabel('Value of Transition');
ylabel('Probability');
xlim([-10 10]);
P = plot(x_lim3,y3,'g'); P.LineWidth = 2;
legend('New-Transform Transitions Histogram','New-Transform Transitions Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_NT'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_NT'],'epsc');

figure('Renderer', 'painters', 'Position', [10 10 1500 900]);
h1 = histogram(Error,200);
hold on; grid minor; title('Error and Lamperti Measurements');
h2 = histogram(Lamparti_Data,200);
h1.Normalization = 'pdf';
h2.Normalization = 'pdf';
xlabel('Value of Measurement');
ylabel('Probability');
std_of_1  = std(Error(:));
mean_of_1 = mean(Error(:));
std_of_2  = std(Lamparti_Data(:));
mean_of_2 = mean(Lamparti_Data(:));
std_of_3  = std(New_Transform_Data(:));
mean_of_3 = mean(New_Transform_Data(:));
% x_lim = [-4:0.001:3];
x_lim = [-7:0.001:1];
y1    = normpdf(x_lim,mean_of_1,std_of_1/1);
y2    = normpdf(x_lim,mean_of_2,std_of_2/1);
y3    = normpdf(x_lim3,mean_of_3,std_of_3/1);
P = plot(x_lim,y1,'b'); P.LineWidth = 2;
P = plot(x_lim,y2,'r'); P.LineWidth = 2;
xlim([min(x_lim) max(x_lim)]);
legend('Error Histogram','Lamperti Histogram',...
    'Error Gaussian Approx.','Lamperti Gaussian Approx.');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Measurements'],'epsc');

figure;
h1 = histogram(Error,200);
hold on; grid minor; title('Error Measurements');
h1.Normalization = 'pdf';
xlabel('Value of Measurement');
ylabel('Probability');
% xlim([-0.5 0.5]);
x_lim = [-0.5:0.001:0.5];
y1    = normpdf(x_lim,mean_of_1,std_of_1/1);
P = plot(x_lim,y1,'b'); P.LineWidth = 2;
legend('Error Histogram','Error Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Measurements_Error'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_Measurements_Error'],'epsc');

figure;
h2 = histogram(Lamparti_Data,200);
hold on; grid minor; title('Lamperti Measurements');
h2.Normalization = 'pdf';
h2.FaceColor = '#D95319';
xlabel('Value of Measurement');
ylabel('Probability');
% xlim([-4 3]);
x_lim = [-8:0.001:1];
y2 = normpdf(x_lim,mean_of_2,std_of_2/1);
P  = plot(x_lim,y2,'r'); P.LineWidth = 2;
xlim([min(x_lim) max(x_lim)]);
legend('Lamperti Histogram','Lamperti Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Measurements_Lamperti'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_Measurements_Lamperti'],'epsc');

figure;
h3 = histogram(New_Transform_Data,200);
hold on; grid minor; title('New-Transform Measurements');
h3.Normalization = 'pdf';
h3.FaceColor = '#77AC30';
xlabel('Value of Measurement');
ylabel('Probability');
P = plot(x_lim3,y3,'g'); P.LineWidth = 2;
xlim([min(x_lim3) max(x_lim3)]);
legend('New-Transform Histogram','New-Transform Gaussian Approx.','Location','southoutside');
saveas(gcf,[pwd '/someResults/final/Gauss_Approx_Measurements_NT'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/Gauss_Approx_Measurements_NT'],'epsc');

%% (12) We load the data from (6) to check the histograms with curtailing.

close all;
clear all;
clc;

load('MTLOG_0100_and_Real_24h_Training_Data.mat'); % Data from (10).
load('MTLOG_0100_and_Real_24h_Testing_Data.mat'); % Data from (10).
load('MTLOG_0100_and_Real_24h_Complete_Data.mat'); % Data from (10).

Forecast          = Table_Complete.Forecast;
Forecast_Dot      = Table_Complete.Forecast_Dot;
real_ADME         = Table_Complete.Real_ADME;
Error             = Table_Complete.Error;
Error_Transitions = Table_Complete.Error_Transitions;
Lamparti_Data     = Table_Complete.Error_Lamp;
Lamparti_Tran     = Table_Complete.Error_Lamp_Transitions;

load('MTLOG_0100_and_Real_24h.mat'); % Data from (6): Table.
Forecast_6  = Table.Forecast;
real_ADME_6 = Table.Real_ADME;
norm_wind = 1474;
h_error = [];
m_error = [];
l_error = [];
count = 1;
for i = 1:length(real_ADME_6)
    aux(i,:) = real_ADME_6{i};
    if aux(i,:) == 0 % We save the indices where all are zeros.
        toRemove(count) = i;
        count = count + 1;
    end
end
real_ADME_6 = aux;
for i = length(toRemove):-1:1
    real_ADME_6(toRemove(i),:) = [];
    Forecast_6(toRemove(i),:)  = [];
end
real_ADME_6 = real_ADME_6 / norm_wind;
Forecast_6  = Forecast_6  / norm_wind;
error       = real_ADME_6 - Forecast_6;

for i = 1:length(error(:,1))
    for j = 1:length(error(1,:))
        if real_ADME_6(i,j) < 0.3
            l_error(end+1) = error(i,j);
        elseif real_ADME_6(i,j) >= 0.3 && real_ADME_6(i,j) < 0.6
            m_error(end+1) = error(i,j);
        else
            h_error(end+1) = error(i,j);
        end
    end
end

figure; % LOW FORECAST ERROR:
histogram(l_error,20); grid minor;
% title('Low Power Range (data with curtailing)');
title('Low Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/LP_6'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/LP_6'],'epsc');

figure; % MID FORECAST ERROR:
histogram(m_error,20); grid minor;
% title('Mid Power Range (data with curtailing)');
title('Mid Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/MP_6'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/MP_6'],'epsc');

figure; % HIGH FORECAST ERROR:
histogram(h_error,20); grid minor;
% title('High Power Range (data with curtailing)');
title('High Power Range');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/HP_6'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/HP_6'],'epsc');

figure; % ALL FORECAST ERROR:
histogram(error,30); grid minor;
% title('All Power (data with curtailing)');
title('All Power');
xlabel('Forecast Error');
saveas(gcf,[pwd '/someResults/final/AP_6'],'epsc');
saveas(gcf,[pwd '/someResults/forPaper/AP_6'],'epsc');