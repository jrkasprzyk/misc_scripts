% Snow-17 accumulation and ablation model. This version of Snow-17 is
% intended for use at a point location. The time steps for precipitation
% and temperature must be equal for this code.
%
%RELEASE NOTES
%   Written by Mark Raleigh (mraleig1@uw.edu) based on Anderson (2006).
%   Version 1.0 Released on January 27, 2010
%   Version 1.1 Released by Mark Raleigh, Feb 2013 - issues fixed with RvS
%       and rain-on-snow melt, and new option for Rain vs. Snow added
%   Version 1.2 Released by Mark Raleigh, June 2013 - issue fixed where
%       W_q retains non-zero value once the snowpack has melted (I set W_q
%       to 0 when W_i is 0)
%
%SYNTAX
%   [TIME, modelSWE, outflow] = snow17(T,P,yr_i, month_i, day_i, hr_i ,elevation, dtt, dtp, S, RvS);
%   [TIME, modelSWE, outflow] = snow17(T,P,yr_i, month_i, day_i, hr_i ,elevation, dtt, dtp, S, RvS, UADJ, MBASE, MFMAX, MFMIN, TIPM, NMF, PLWHC);
%
%INPUTS
%   1) T - Lx1 array of air temperature data (deg C)
%   2) P - Lx1 array of incremental precipitation data (mm/timestep)
%   3) yr_i = 1x1 value of starting year (i.e. 2003)
%   4) month_i = 1x1 value of starting month (i.e. 10)
%   5) day_i = 1x1 value of starting day (i.e. 1)
%   6) hr_i = 1x1 value of starting hour (0-23)
%   7) elevation = 1x1 value of station elevation (m MSL)
%   8) dtt = 1x1 value of time step for temperature (should be the same as precipitation time step, dtp)
%   9) dtp = 1x1 value of time step for temperature (should be the same as temperature time step, dtt)
%   10) S = 1x1 value of SCF
%   11) RvS = control of how rain and snow are divided.
%         Enter 0 if you want a single temperature (PXTEMP) that divides rain and snow
%         Enter 1 if you want a linear transition between 2 temperatures (PXTEMP1 and PXTEMP2)
%         Enter 2 if you want no adjustments made to the precipitation data.  All precipitation is considered snowfall.
%         Enter 3 if you want to use an S-shaped transition [Kienzle 2008]
%   12) (optional) params = seven sets of 1x1 values of model parameters
%       Note: The default model calibration will be used if (UADJ, MBASE,
%       MFMAX, MFMIN, TIPM, NMF, PLWHC) are not used as input
%
%OUTPUTS
%   1) TIME = Lx7 matrix of time values (see timebuilder.m for column designation)
%   2) modelSWE = Lx1 array of modelSWE (mm)
%   3) outflow = Lx1 array of outflow from the snowpack (snowmelt, or rain
%   percolating through the snowpack).  Note: Outflow is zero during times
%   when it is raining on bare ground (no snowpack exists).

function [TIME, modelSWE, outflow] = snow17(T,P,yr_i, month_i, day_i, hr_i, elevation, dtt, dtp, S, RvS, varargin)

%% Snow-17 Default Parameters

SCF = S;                %gauge under-catch snow correction factor


if nargin ==11
    UADJ = 0.04;            %average wind function during rain on snow (mm/mb) - 0.04 value for the American River Basin from Shamir & Georgakakos 2007
    MBASE = 1;              %base temperature above which melt typically occurs (deg C) - ****must be greater than 0 deg C****- value of 1 for the American River Basin from Shamir & Georgakakos 2007
    MFMAX = 1.05;           %maximum melt factor during non-rain periods (mm/deg C 6 hr) - in western facing slope assumed to occur on June 21 - value of 1.05 for the American River Basin from Shamir & Georgakakos 2007
    MFMIN = 0.60;           %minimum melt factor during non-rain periods (mm/deg C 6 hr) - in western facing slope assumed to occur on December 21 - value of 0.60 for the American River Basin from Shamir & Georgakakos 2007
    TIPM = 0.1;             %model parameter (>0.0 and <1.0) - Anderson Manual recommends 0.1 to 0.2 for deep snowpack areas
    NMF = 0.15;             %maximum negative melt factor (mm/deg C 6 hr) - value of 0.15 for the American River Basin from Shamir & Georgakakos 2007
    PLWHC = 0.04;           %percent liquid water holding capacity of the snow pack - max is 0.4 - value of 0.04 for the American River Basin from Shamir & Georgakakos 2007
elseif nargin == 18
    if size(varargin,2) ~= 7
        error('params input must be seven separate 1x1 variables')
    end
    varargin=cell2mat(varargin);
    UADJ = varargin(1);
    MBASE = varargin(2);
    MFMAX = varargin(3);
    MFMIN = varargin(4);
    TIPM = varargin(5);
    NMF = varargin(6);
    PLWHC  = varargin(7);
else
    error('Invalid input')
end

PXTEMP = 1;             %Temperature of rainfall


%% Checks

if size(T,1) ~= size(P,1)
    error('Error - temperature and precip arrays must be the same size')
end

if nanmax(nanmax(isnan(T)))==1 || nanmax(nanmax(isnan(P)))==1
    error('NaN values detected in T or P data.  This is not allowed')
end

if isnan(S)==1
    error('snow correction factor (S or SCF) cannot be NaN')
end

if RvS==2
    disp('snow17.m, Note: All precip is considered snowfall, so no rain-on-snow melt will be calculated')
end

%% Initialization

ATI = 0;                % Antecedent Temperature Index, deg C
W_q = 0;                % Liquid water held by the snow (mm)
W_i=0;                  % W_i = accumulated water equivalent of the ice portion of the snow cover (mm)
Deficit = 0;            % Heat Deficit, also known as NEGHS, Negative Heat Storage

L = size(T,1);                 % number of time steps
modelSWE = zeros(L,1);
outflow = zeros(L,1);

TIME = time_builder(yr_i, month_i, day_i, hr_i, dtt, L);

stefan = 6.12 * (10^(-10));                                                     % Stefan-Boltzman constant (mm/K/hr)

elevation = elevation/100;                                                      % Elevation for P_atm equation needs to be in hundreds of meters
P_atm = 33.86 * (29.9 - (0.335 * elevation) + (0.00022 * (elevation^2.4)));     % atmospheric pressure (mb) where elevation is in HUNDREDS of meters (this is incorrectly stated in the manual)



TIPM_dtt = 1.0 - ((1.0 - TIPM)^(dtt/6));


% Divide Rain and Snow at all time steps
if RvS ==0 || RvS==1 || RvS==2
    [Rfall, Sfall] = RvsS(T,P,RvS);
elseif RvS==3
    [Rfall, Sfall] = RvsS2(TIME,T,P);
else
    error('Invalid rain vs snow option')
end

% calculate fraction of rain and snow at each time step
fracrain = Rfall./P;
fracsnow = Sfall./P;

% set fracrain and fracsnow to 0 at any timesteps with 0 precip
fracrain(P==0) = 0;
fracsnow(P==0) = 0;



%% Model Execution

for i = 1:L
    DAYN = TIME(i,6);     % the current julian date
    Mf =  meltfunction(TIME(i,1), DAYN, dtt, MFMAX, MFMIN);
    
    T_air_meanC = T(i);                 % air temperature at this time step (deg C)
    precip = P(i);                      % precipitation at this time step (mm)
    
    
    %% Snow Accumulation
    
    Pn = precip*fracsnow(i)*SCF;           % water equivalent of new snowfall (mm)
    W_i = W_i + Pn;                       % W_i = accumulated water equivalent of the ice portion of the snow cover (mm)
    E=0;
    RAIN = fracrain(i)*precip;         % amount of precip (mm) that is rain during this time step
    
    
    %% Temperature and Heat Deficit from new Snow
    
    if T_air_meanC < 0
        T_snow_new = T_air_meanC;
        delta_HD_snow = - (T_snow_new*Pn)/(80/0.5);      % delta_HD_snow = change in the heat deficit due to snowfall (mm)
        T_rain = PXTEMP;
    else
        T_snow_new = 0;
        delta_HD_snow = 0;
        T_rain = T_air_meanC;
    end
    
    %% Antecedent temperature Index
    
    if (Pn > (1.5*dtp))
        ATI = T_snow_new;
    else
        ATI = ATI + TIPM_dtt * (T_air_meanC - ATI);       %Antecedent temperature index
    end
    
    if (ATI > 0)
        ATI = 0;
    end
    
    %% Heat Exchange when no Surface Melt
    
    
    delta_HD_T = NMF * (dtp/6) * ((Mf)./MFMAX) * (ATI - T_snow_new);            % delta_HD_T = change in heat deficit due to a temperature gradient (mm)
    
    
    %% Rain-on-Snow Melt
    
    if RvS==2
        % do not compute rain-on-snow melt if all precip is considered snowfall
        M_RoS = 0;
    else
        
        e_sat = 2.7489 * (10^8) * exp((-4278.63/(T_air_meanC+242.792)));                % saturated vapor pressure at T_air_meanC (mb)
        
        if RAIN > (0.25 * dtp)         %1.5 mm/ 6 hrs
            %Melt (mm) during rain-on-snow periods is:
            clear M_RoS1 M_RoS2 M_RoS3
            M_RoS1 = max(stefan * dtp * (((T_air_meanC+273)^4)-(273^4)), 0);
            M_RoS2 = max((0.0125 * RAIN * T_rain),0);
            M_RoS3 = max((8.5 * UADJ * (dtp/6) * (((0.9*e_sat) - 6.11) + (0.00057*P_atm*T_air_meanC))),0);
            M_RoS = M_RoS1 + M_RoS2 + M_RoS3;
        else
            M_RoS = 0;
        end
    end
    
    
    %% Non-Rain Melt
    
    if RAIN <= (0.25 * dtp) && (T_air_meanC > MBASE)
        %Melt during non-rain periods is:
        M_NR = (Mf * (T_air_meanC - MBASE) * (dtp/dtt)) + (0.0125 * RAIN * T_rain);
    else
        M_NR = 0;
    end
    
    
    %% Ripeness of the snow cover
    
    Melt = M_RoS + M_NR;
    
    if Melt<=0
        Melt=0;
    end
    
    if Melt<W_i
        W_i = W_i-Melt;
    else
        Melt=W_i+W_q;
        W_i=0;
    end
    
    Qw = Melt + RAIN;                                           % Qw = liquid water available melted/rained at the snow surface (mm)
    W_qx = PLWHC * W_i;                                         % W_qx = liquid water capacity (mm)
    Deficit = Deficit + delta_HD_snow + delta_HD_T;             % Deficit = heat deficit (mm)
    
    if Deficit<0                    % limits of heat deficit
        Deficit=0;
    elseif Deficit>(0.33*W_i)
        Deficit=0.33*W_i;
    end
    
    % In SNOW-17 the snow cover is ripe when both (Deficit=0) & (W_q = W_qx)
    if W_i>0
        if (Qw + W_q) > ((Deficit*(1+PLWHC)) + W_qx)        % THEN the snow is RIPE
            E = Qw + W_q - W_qx - (Deficit*(1+PLWHC));      % Excess liquid water (mm)
            W_q = W_qx;                                     % fills liquid water capacity
            W_i = W_i + Deficit;                            % W_i increases because water refreezes as heat deficit is decreased
            Deficit = 0;
        elseif (Qw >= Deficit) %& ((Qw + W_q) <= ((Deficit*(1+PLWHC)) + W_qx))            % THEN the snow is NOT yet ripe, but ice is being melted
            E = 0;
            W_q = W_q + Qw - Deficit;
            W_i = W_i + Deficit;               % W_i increases because water refreezes as heat deficit is decreased
            Deficit = 0;
        elseif (Qw < Deficit) %elseif ((Qw + W_q) < Deficit)                                      % THEN the snow is NOT yet ripe
            E = 0;
            W_i = W_i + Qw;                   % W_i increases because water refreezes as heat deficit is decreased
            Deficit = Deficit - Qw;
        end
        
        SWE = W_i + W_q;   % + E;
    else
        %%% then no snow exists!
        E = Qw;
        SWE = 0;
        W_q = 0;
    end
    
    if Deficit == 0
        ATI = 0;
    end
    
    
    %% End of model execution
    
    modelSWE(i,1) = SWE;                           % total SWE (mm) at this time step
    outflow(i,1) = E;
    

    
end


end

%% Seasonal variation calcs - indexed for Non-Rain melt

function meltf = meltfunction(yearrun, jday, dtt, MFMAX, MFMIN)

leap = isleap(yearrun);

if leap == 1                         % then this is a leap year
    days=366;
    N_Mar21=jday-81;                      % day of year since March 21 (leap)
else                                          % not a leap year
    days=365;
    N_Mar21=jday-80;                      % day of year since March 21 (non-leap)
end

Sv = (0.5*sin((N_Mar21 * 2 * pi)/days)) + 0.5;                              % seasonal variation
Av = 1.0;                                                                   % latitude parameter, Av=1.0 when lat < 54 deg N
meltf = (dtt/6) * ((Sv * Av * (MFMAX - MFMIN)) + MFMIN);                       %non-rain melt factor, seasonally varying

end