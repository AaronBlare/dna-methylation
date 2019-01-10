function plot_clock_metrics(config, metric)

fn = sprintf('%s/%s/%s.xlsx', ...
    config.up, ...
    get_result_path(config), ...
    config.file_name);

[num,txt,raw] = xlsread(fn);

keys = raw(1, :);
metric_id = find(string(keys)==string(metric));

names = raw(2:end, 1);
counts = cell2mat(raw(2:end, 3));
metrics = cell2mat(raw(2:end, metric_id));

hold all;
h = plot(counts, metrics, 'o-', 'LineWidth', 3);
legend(h, sprintf('gender: %s', config.gender));
set(h, 'Color', config.color)
set(gca, 'FontSize', 30);
xlabel('count', 'Interpreter', 'latex');
set(gca, 'FontSize', 30);
ylabel(sprintf('%s', metric), 'Interpreter', 'none');
box on;

end

