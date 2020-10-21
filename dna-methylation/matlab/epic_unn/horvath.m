clear all;

path = 'E:/YandexDisk/Work/pydnameth/unn_epic';

fn = sprintf('%s/betas_horvath_calculator_filtered_normallized.output.csv', path);
obs = readtable(fn);

status = obs.Sample_Group;
agediff = obs.AgeAccelerationDiff;
age = obs.Age;
age_dnam = obs.DNAmAge;

c_xs = [];
c_ys = [];

t_xs = [];
t_ys = [];

for id = 1 : size(age, 1)
    
    if status{id} == 'C'
        c_xs = vertcat(c_xs, age(id));
        c_ys = vertcat(c_ys, age_dnam(id));
    else
        t_xs = vertcat(t_xs, age(id));
        t_ys = vertcat(t_ys, age_dnam(id));
    end
    
end

fn = sprintf('%s/horvath/control.csv', path);
ctrl = readtable(fn);
c_xs_l = [0 100];
c_ys_l = c_xs_l * ctrl.coeffs(2) + ctrl.coeffs(1);

fn = sprintf('%s/horvath/treatment.csv', path);
ctrl = readtable(fn);
t_xs_l = [0 100];
t_ys_l = t_xs_l * ctrl.coeffs(2) + ctrl.coeffs(1);

fig = figure;
h = plot(c_xs, c_ys, 'o', 'MarkerSize', 10, 'Color', 'b');
h.Color(4) = 0.5;
legend(h, 'Control')
hold all;
h = plot(t_xs, t_ys, 'o', 'MarkerSize', 10, 'Color', 'r');
h.Color(4) = 0.5;
legend(h, 'Treatment')
set(gca, 'FontSize', 40);
xlabel('Age', 'Interpreter', 'latex');
set(gca, 'FontSize', 40);
ylabel('DNAmAge', 'Interpreter', 'latex');
h = plot([0 100], [0 100], 'k');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
h = plot(c_xs_l, c_ys_l, 'Color', 'b');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';
h = plot(t_xs_l, t_ys_l, 'Color', 'r');
h.Annotation.LegendInformation.IconDisplayStyle = 'off';

p = kruskalwallis(agediff, status, 'on');

a = get(get(gca,'children'),'children');   % Get the handles of all the objects
t = get(a,'tag');   % List the names of all the objects 
idx=strcmpi(t,'box');  % Find Box objects
boxes=a(idx);          % Get the children you need
set(a,'linewidth',2); % Set width

dim = [.15 .6 .3 .3];
str = sprintf('Kruskal-Wallis p-value: %0.2e', p);
annotation('textbox',dim,'String',str,'FitBoxToText','on');

