%R56
Rname = 'R56';
Re0 = 40.20;
Rref = 39.4;
fsave = '200416\200416_';
f3p4 = readtable('200416\200416_glass_R56_power_dep_f3p4.txt');
f15 =  readtable('200416\200416_glass_R56_power_dep_f15.txt');
f30 = readtable('200416\200416_glass_R56_power_dep_f30.txt');
f50 = readtable('200416\200416_glass_R56_power_dep_f50.txt');

freqs = [3.4, 15, 30, 50];

f3p4.I1w = f3p4.X1 / Re0;
f15.I1w = f15.X1 / Re0;
f30.I1w = f30.X1 / Re0;
f50.I1w = f50.X1 / Re0;

f3p4.X3_pure = f3p4.X3 - f3p4.X3_ref;
f15.X3_pure = f15.X3 - f15.X3_ref;
f30.X3_pure = f30.X3 - f30.X3_ref;
f50.X3_pure = f50.X3 - f50.X3_ref;

f3p4.Y3_pure = f3p4.Y3 - f3p4.Y3_ref;
f15.Y3_pure = f15.Y3 - f15.Y3_ref;
f30.Y3_pure = f30.Y3 - f30.Y3_ref;
f50.Y3_pure = f50.Y3 - f50.Y3_ref;

f = table(f3p4,f15,f30,f50);
%f1 = figure;
plot(f{:,1}.V_input(1:end-2),f{:,1}.X3(1:end-2))
hold on
scatter(f{:,1}.V_input(1:end-2),f{:,1}.X3(1:end-2))
for i = 2:width(f)
    plot(f{:,i}.V_input(1:end-2),f{:,i}.X3(1:end-2))
    scatter(f{:,i}.V_input(1:end-2),f{:,i}.X3(1:end-2))
end
xlabel('V_{input}(V)')
ylabel('X3(V)')
title([Rname, ' V_{input} vs. V_{3w}'])
%saveas(f1, [fsave, Rname, '_V_input_vs_X3.jpg'])
%after1.4V, breakdown?V3w up up
%not linear?

%f2 = figure;
plot(f{:,1}.V_input(1:end-2),f{:,1}.X3_ref(1:end-2))
hold on
scatter(f{:,1}.V_input(1:end-2),f{:,1}.X3_ref(1:end-2))
for i = 2:width(f)
    plot(f{:,i}.V_input(1:end-2),f{:,i}.X3_ref(1:end-2))
    scatter(f{:,i}.V_input(1:end-2),f{:,i}.X3_ref(1:end-2))
end
xlabel('V_{input}(V)')
ylabel('X3_ref(V)')
title([Rname, ' V_{input} vs. Vref_{3w}'])
%saveas(f2, [fsave, Rname, '_V_input_vs_X3_ref.jpg'])

%f3 = figure;
plot(f{:,1}.V_input(1:end-2),f{:,1}.X3_pure(1:end-2))
hold on
scatter(f{:,1}.V_input(1:end-2),f{:,1}.X3_pure(1:end-2))
for i = 2:width(f)
    plot(f{:,i}.V_input(1:end-2),f{:,i}.X3_pure(1:end-2))
    scatter(f{:,i}.V_input(1:end-2),f{:,i}.X3_pure(1:end-2))
end
xlabel('V_{input}(V)')
ylabel('X3_pure(V)')
title([Rname, ' V_{input} vs. V_{3wpure}'])
%saveas(f3, [fsave, Rname, '_V_input_vs_X3_pure.jpg'])

%f4 = figure;
plot(f{:,1}.V_input(1:end-2),f{:,1}.X1(1:end-2))
hold on
scatter(f{:,1}.V_input(1:end-2),f{:,1}.X1(1:end-2))
for i = 2:width(f)
    plot(f{:,i}.V_input(1:end-2),f{:,i}.X1(1:end-2))
    scatter(f{:,i}.V_input(1:end-2),f{:,i}.X1(1:end-2))
end
xlabel('V_{input}(V)')
ylabel('X1(V)')
title([Rname, ' V_{input} vs. V_{1w}'])
%saveas(f4, [fsave, Rname, '_V_input_vs_X1.jpg'])

f5 = figure;
hold on
h(1) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3_pure(1:end-2), 'DisplayName', sprintf('f = %0.1fHz',freqs(1)));
%h(9) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3_pure(1:end-2));
h(2) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3_pure(1:end-2));
%h(10) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3_pure(1:end-2));
for i = 2:width(f)
    h(i * 2 - 1) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3_pure(1:end-2), 'DisplayName', sprintf('f = %dHz',freqs(i)));
    h(i * 2) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3_pure(1:end-2));
    %h(i * 2 + 7) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3_pure(1:end-2));
    %h(i * 2 + 8) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3_pure(1:end-2));
end
hold off
legend(h([1,3,5,7]))
xlabel('I_{1w}^3(A)')
ylabel('V3w_{pure}(V)')
title([Rname, ' I_{1w}^3 vs. V_{3wpure}'])
%saveas(f5, [fsave, Rname, '_I_1w_vs_X3_pure.jpg'])

f6 = figure;
hold on
h(1) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3(1:end-2), 'DisplayName', sprintf('f = %0.1fHz',freqs(1)));
h(2) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3(1:end-2));
h(3) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3(1:end-2));
h(4) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3(1:end-2));
for i = 2:width(f)
    h(i * 4 - 3) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3(1:end-2), 'DisplayName', sprintf('f = %dHz',freqs(i)));
    h(i * 4 - 2) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3(1:end-2));
    h(i * 4 - 1) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3(1:end-2));
    h(i * 4) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3(1:end-2));
end
hold off
legend(h([1,5,9,13]))
xlabel('I_{1w}^3(A)')
ylabel('V3w(V)')
title([Rname, ' I_{1w}^3 vs. V_{3w}'])
text(2e-8,-12e-6, 'X3')
text(2e-8,0, 'Y3')
%saveas(f6, [fsave, Rname, '_I_1w_vs_X3.jpg'])

f7 = figure;
hold on
h(1) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3_ref(1:end-2), 'DisplayName', sprintf('f = %0.1fHz',freqs(1)));
h(2) = plot(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3_ref(1:end-2));
h(3) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.X3_ref(1:end-2));
h(4) = scatter(f{:,1}.I1w(1:end-2).^3,f{:,1}.Y3_ref(1:end-2));
for i = 2:width(f)
    h(i * 4 - 3) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3_ref(1:end-2), 'DisplayName', sprintf('f = %dHz',freqs(i)));
    h(i * 4 - 2) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.X3_ref(1:end-2));
    h(i * 4 - 1) = plot(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3_ref(1:end-2));
    h(i * 4) = scatter(f{:,i}.I1w(1:end-2).^3,f{:,i}.Y3_ref(1:end-2));
end
hold off
legend(h([1,5,9,13]))
xlabel('I_{1w}^3(A)')
ylabel('V3w_ref(V)')
title([Rname, ' I_{1w}^3 vs. V_{3wref}'])
text(2e-8,10e-6, 'X3')
text(2e-8,0, 'Y3')
%saveas(f7, [fsave, Rname, '_I_1w_vs_X3_ref.jpg'])