close all;
clear all;
clc;

% 23/04/2020. We want to create three datasets with exactly the same dates.
% Each dataset will be from a different provider. We do this to use
% correctly the BIC and AIC.

load('AWSTP_0100_and_Real_24h_Complete_Data.mat');
Table_Complete_AWSTP = Table_Complete;

load('MTLOG_0100_and_Real_24h_Complete_Data.mat');
Table_Complete_MTLOG = Table_Complete;

load('UTEP5_0100_and_Real_24h_Complete_Data.mat');
Table_Complete_UTEP5 = Table_Complete;

clear Table_Complete;
Final_date  = '20191231';
Actual_date = Final_date;

Dates_AWSTP = Table_Complete_AWSTP.Date;
Dates_MTLOG = Table_Complete_MTLOG.Date;
Dates_UTEP5 = Table_Complete_UTEP5.Date;

while not(strcmp(Actual_date,'20181231'))
    
    disp(Actual_date);
    
    Is_in_all = any(strcmp(Dates_AWSTP,Actual_date)) + ...
        any(strcmp(Dates_MTLOG,Actual_date)) + any(strcmp(Dates_UTEP5,Actual_date));

    if Is_in_all ~= 3
        for i = height(Table_Complete_AWSTP):-1:1
            if strcmp(Table_Complete_AWSTP.Date{i},Actual_date)
                Table_Complete_AWSTP(i,:) = [];
            end
        end
        for i = height(Table_Complete_MTLOG):-1:1
            if strcmp(Table_Complete_MTLOG.Date{i},Actual_date)
                Table_Complete_MTLOG(i,:) = [];
            end
        end
        for i = height(Table_Complete_UTEP5):-1:1
            if strcmp(Table_Complete_UTEP5.Date{i},Actual_date)
                Table_Complete_UTEP5(i,:) = [];
            end
        end
    end
    
    Actual_date_timeFormat = datetime(Actual_date,'InputFormat','yyyyMMdd');
    Actual_date_timeFormat = Actual_date_timeFormat - days(1);
    Actual_date            = datestr(Actual_date_timeFormat,'yyyymmdd');
    
end

% Now, we create the training and testing tables:

Table_Training_AWSTP = Table_Complete_AWSTP;
Table_Testing_AWSTP  = Table_Complete_AWSTP;
Table_Training_MTLOG = Table_Complete_MTLOG;
Table_Testing_MTLOG  = Table_Complete_MTLOG;
Table_Training_UTEP5 = Table_Complete_UTEP5;
Table_Testing_UTEP5  = Table_Complete_UTEP5;
switching            = 1;

for i = height(Table_Complete_AWSTP):-1:1
    if switching == 1
        Table_Training_AWSTP(i,:) = [];
        Table_Training_MTLOG(i,:) = [];
        Table_Training_UTEP5(i,:) = [];
    elseif switching == -1
        Table_Testing_AWSTP(i,:) = [];
        Table_Testing_MTLOG(i,:) = [];
        Table_Testing_UTEP5(i,:) = [];
    end
    switching = - switching;
end

Table_Complete          = Table_Complete_AWSTP;
Table_Training_Complete = Table_Training_AWSTP;
Table_Testing_Complete  = Table_Testing_AWSTP;
save('Table_Complete_AWSTP.mat','Table_Complete');
save('Table_Training_AWSTP.mat','Table_Training_Complete');
save('Table_Testing_AWSTP.mat', 'Table_Testing_Complete');
writetable(Table_Training_Complete,'Table_Training_AWSTP.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_AWSTP.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete_AWSTP.csv','Delimiter',',','QuoteStrings',true)

Table_Complete          = Table_Complete_MTLOG;
Table_Training_Complete = Table_Training_MTLOG;
Table_Testing_Complete  = Table_Testing_MTLOG;
save('Table_Complete_MTLOG.mat','Table_Complete');
save('Table_Training_MTLOG.mat','Table_Training_Complete');
save('Table_Testing_MTLOG.mat', 'Table_Testing_Complete');
writetable(Table_Training_Complete,'Table_Training_MTLOG.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_MTLOG.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete_MTLOG.csv','Delimiter',',','QuoteStrings',true)

Table_Complete          = Table_Complete_UTEP5;
Table_Training_Complete = Table_Training_UTEP5;
Table_Testing_Complete  = Table_Testing_UTEP5;
save('Table_Complete_UTEP5.mat','Table_Complete');
save('Table_Training_UTEP5.mat','Table_Training_Complete');
save('Table_Testing_UTEP5.mat', 'Table_Testing_Complete');
writetable(Table_Training_Complete,'Table_Training_UTEP5.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Testing_Complete,'Table_Testing_UTEP5.csv','Delimiter',',','QuoteStrings',true)
writetable(Table_Complete,'Table_Complete_UTEP5.csv','Delimiter',',','QuoteStrings',true)