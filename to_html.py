from bokeh.plotting import figure, output_file, show
import pandas as pd

excel_file = "meu_data.xlsx"

output_file("data.html")

excel_data = pd.read_excel(excel_file, sheetname=None, header=0, index_col=0)

x = excel_data['wait_time'].index.tolist()
y_wait = excel_data['wait_time']['Evidence vozidel'].tolist()
y_queue = excel_data['queue']['Evidence vozidel'].tolist()
y_booths = excel_data['active_booths']['Evidence vozidel'].tolist()

p = figure(
    title="Wait time for Evidence vozidel at MeU Cernosice", 
    x_axis_label="Time", x_axis_type="datetime",
    y_axis_label="mins/people/booths",
    width=1200)

#for col in excel_data['wait_time']:
#    y = excel_data['wait_time'][col]
#    p.line(x,y, legend=str(col), line_width=2)

p.line(x,y_wait, legend="Wait time (min)", line_width=2)
p.line(x,y_queue, legend="People in queue", line_width=2, line_color="red")
p.line(x,y_booths, legend="Active booths", line_width=2, line_color="green")

show(p)

print("Success")
