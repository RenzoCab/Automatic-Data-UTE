% Supplementary Material for the Wind-Power Paper.
% Author: Renzo Caballero
% KAUST: King Abdullah University of Science and Technology
% email: Renzo.CaballeroRosas@kaust.edu.sa CaballeroRenzo@hotmail.com
% Website: https://orcid.org/0000-0003-3220-0923.
% July 2020; Last revision: 19/07/2020.

close all;
clear all;
clc;

allDaysPlots = 1;

data_sets = {'A','B','C'};
angle      = 45;

for i = 1:3

    data_set = data_sets{i};

    if strcmp(data_set,'A')

        load('Table_Complete_MTLOG.mat');
        load('Table_Training_MTLOG.mat');
        load('Table_Testing_MTLOG.mat');

    elseif strcmp(data_set,'B')

        load('Table_Complete_AWSTP.mat');
        load('Table_Training_AWSTP.mat');
        load('Table_Testing_AWSTP.mat');

    elseif strcmp(data_set,'C')

        load('Table_Complete_UTEP5.mat');
        load('Table_Training_UTEP5.mat');
        load('Table_Testing_UTEP5.mat');

    end

    if allDaysPlots
        figure(90);
    end

    count = 1;

    Forecast          = Table_Complete.Forecast;
    Forecast_Dot      = Table_Complete.Forecast_Dot;
    real_ADME         = Table_Complete.Real_ADME;
    Error             = Table_Complete.Error;
    Error_Transitions = Table_Complete.Error_Transitions;

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

        allError   (i,:) = Table_Complete.Error(i,:);
        dailyError (i,:) = abs(Table_Complete.Error(i,:));
        error(i)         = sum(abs(Table_Complete.Error(i,:)))/145;

        if 1 == allDaysPlots % Here we plot and save the daily data for all the days.

            set(0,'CurrentFigure',90); clf(90);
            P = plot(t_ticks,Forecast(i,:),'k'); P.LineWidth = 2;
            hold on;
            P = plot(t_ticks,real_ADME(i,:),'b'); P.LineWidth = 2;
    %         xlabel('Time');
    %         ylabel('Power'); 
            xticks([13:2:37]/24);
            datetick('x','HHPM','keepticks');
            xtickangle(angle);
            date_format = datetime(Table_Complete.Date(i),'InputFormat','yyyyMMdd');
            date_format_next = date_format + days(1);
            title([datestr(date_format),' and ',datestr(date_format_next)]);
            ylim([0 1]); 
            grid minor;
            legend(['Forecast Provider ',data_set],'Real Production');
            saveas(gcf,[pwd '/supplementary_material/data_plots/prov_',data_set,'/plots/',num2str(count)],'epsc');
            pause(0.1);

            set(0,'CurrentFigure',90); clf(90);
            P = plot(t_ticks,Error(i,:)); P.LineWidth = 1;
            ylim([-0.5 0.5]);
    %         xlabel('Time');
    %         ylabel('Power'); 
            xticks([13:2:37]/24);
            datetick('x','HHPM','keepticks');
            xtickangle(angle);
            title([datestr(date_format),' and ',datestr(date_format_next)]);
            legend(['Forecast Error Provider ',data_set]); grid minor;
            saveas(gcf,[pwd '/supplementary_material/data_plots/prov_',data_set,'/error/',num2str(count)],'epsc');
            pause(0.1);

            set(0,'CurrentFigure',90); clf(90);
            P = plot(t_ticks(1:end-1),Error_Transitions(i,:)); P.LineWidth = 1;
            ylim([-0.5 0.5]);
    %         xlabel('Time');
    %         ylabel('Power'); 
            xticks([13:2:37]/24);
            datetick('x','HHPM','keepticks');
            xtickangle(angle);
            title([datestr(date_format),' and ',datestr(date_format_next)]);
            legend(['Forecast Error Transition Provider ',data_set]); grid minor;
            saveas(gcf,[pwd '/supplementary_material/data_plots/prov_',data_set,'/transition/',num2str(count)],'epsc');
            pause(0.1);

            set(0,'CurrentFigure',90); clf(90);
            P = plot(t_ticks(1:end-1),Forecast_Dot(i,:)); P.LineWidth = 1;
            ylim([-2 2]);
    %         xlabel('Time');
    %         ylabel('Power'); 
            xticks([13:2:37]/24);
            datetick('x','HHPM','keepticks');
            xtickangle(angle);
            title([datestr(date_format),' and ',datestr(date_format_next)]);
            legend(['Forecast Derivative Provider ',data_set]); grid minor;
            saveas(gcf,[pwd '/supplementary_material/data_plots/prov_',data_set,'/derivative/',num2str(count)],'epsc');
            pause(0.1);

        end

        count = count + 1;

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
    title('Mean Absolute Error (Real Vs. Forecast)');
    xlabel('Day');
    grid minor;
    legend(['Daily MAE  Provider ',data_set],['Weekly MAE  Provider ',data_set]);
    saveas(gcf,[pwd '/supplementary_material/mean_errors/prov_',data_set,'/MAE'],'epsc');

    figure;
    P = plot(t_ticks,averagedDailyError); P.LineWidth = 1;
    xlim([0 24]);
    grid minor; title('Mean Absolute Error (Real Vs. Forecast)');
    xticks([13:37]/24);
    datetick('x','HHPM','keepticks');
    xtickangle(angle);
    legend(['Houlry MAE Provider ',data_set]);
    saveas(gcf,[pwd '/supplementary_material/mean_errors/prov_',data_set,'/H_MAE'],'epsc');

    figure('Renderer', 'painters', 'Position', [10 10 1200 600]);
    plot(Forecast,Error,'.','Color',[0,0.7,0.9]); grid minor;
    title(['Error over Forecast Provider ',data_set]);
    xlabel('Forecast value'); ylabel('Error value');
    saveas(gcf,[pwd '/supplementary_material/scatter/prov_',data_set,'/scatter'],'epsc');

end

copyfile('supplementary_material', '../../../Probabilistic Wind Power Forecasting/LaTeX_Code/Paper/Supplementary Material/plots');