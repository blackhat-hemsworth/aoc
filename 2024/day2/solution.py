class Report:
    report_tuple: tuple
    is_ordered: bool
    dist_list = list
    list_max_dist = int
    list_min_dist = int
    alt_list = list
    is_safe: bool

    def __init__(self, input_list: list):
        self.report_tuple = tuple(input_list)
        self.is_ordered = input_list == sorted(input_list) or input_list == list(reversed(sorted(input_list)))
        self.dist_list = [abs(input_list[i] - input_list[i + 1]) for i in range(len(input_list) - 1)]
        self.list_max_dist = max(self.dist_list)
        self.list_min_dist = min(self.dist_list)
        self.is_safe = self.is_ordered and 1 <= self.list_min_dist and self.list_max_dist <= 3

        self.alt_list = []
        for index in range(len(input_list)):
            self.alt_list.append([val for idx, val in enumerate(input_list) if idx != index])


report_list = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        report_list.append(Report([int(num.strip()) for num in line.split(" ")]))

print(sum([report.is_safe for report in report_list]))

unsafe_reports = [report for report in report_list if not report.is_safe]

damp_results = []
for report in unsafe_reports:
    damp_results.append(sum([Report(alt).is_safe for alt in report.alt_list]) > 0 )

print(sum(damp_results) + sum([report.is_safe for report in report_list]))
