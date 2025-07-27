import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from scipy.stats import linregress
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime as dt
import matplotlib.dates as mdates
from PIL import Image, ImageTk
import warnings

# Suppress RunTimeWarning from division by zero or log of zero in models
warnings.filterwarnings("ignore", category=RuntimeWarning)

class EarthquakeDecayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Earthquake Decay Analysis")
        self.root.geometry("350x300")

        # Data storage
        self.datnum = None
        self.logo_image = None
        try:
            # Load logo for plots
            self.logo_image = Image.open('bmkg-icon.jpg')
        except FileNotFoundError:
            print("Warning: 'bmkg-icon.jpg' not found. Logo will not be displayed.")


        # --- Main Frame ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- UI Controls ---
        # Input Data Button
        self.btn_input = ttk.Button(main_frame, text="Load Event Data (.txt)", command=self.load_data)
        self.btn_input.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5)

        # Interval Entry
        ttk.Label(main_frame, text="Time Interval:").grid(row=1, column=0, sticky="w", padx=5)
        self.e_intv = ttk.Entry(main_frame, width=10)
        self.e_intv.grid(row=1, column=1, sticky="w")
        self.e_intv.insert(0, "1") # Default value

        # Interval Unit Dropdown
        ttk.Label(main_frame, text="Interval Unit:").grid(row=2, column=0, sticky="w", padx=5)
        self.p_intv_var = tk.StringVar(value="Days")
        self.p_intv = ttk.Combobox(main_frame, textvariable=self.p_intv_var, values=["Hours", "Days"], width=8, state='readonly')
        self.p_intv.grid(row=2, column=1, sticky="w")

        # Model Checkboxes
        models_frame = ttk.LabelFrame(main_frame, text="Select Models")
        models_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.cb_omori_var = tk.BooleanVar(value=True)
        self.cb_mogi1_var = tk.BooleanVar()
        self.cb_mogi2_var = tk.BooleanVar()
        self.cb_utsu_var = tk.BooleanVar()

        ttk.Checkbutton(models_frame, text="Omori", variable=self.cb_omori_var).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(models_frame, text="Mogi I", variable=self.cb_mogi1_var).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(models_frame, text="Mogi II", variable=self.cb_mogi2_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(models_frame, text="Utsu", variable=self.cb_utsu_var).grid(row=1, column=1, sticky="w")

        # Action Buttons
        self.btn_process = ttk.Button(main_frame, text="Process and Plot", command=self.process_data)
        self.btn_process.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
        
        self.btn_histogram = ttk.Button(main_frame, text="Show Data Histogram", command=self.show_data_histogram)
        self.btn_histogram.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)

    def load_data(self):
        """Callback for loading earthquake data from a text file."""
        file_path = filedialog.askopenfilename(
            title="Select Data File",
            filetypes=[("Text files", "*.txt"), ("Data files", "*.dat"), ("All files", "*.*")]
        )
        if not file_path:
            return

        try:
            # Read date and time columns as strings
            raw_data = np.loadtxt(file_path, dtype=str, comments='#')
            if raw_data.ndim == 1: # Handle case of a single line file
                raw_data = raw_data.reshape(1, -1)
            
            dates_str = [f"{d} {t}" for d, t in raw_data]
            
            # Convert to matplotlib datenums
            datetimes = [dt.datetime.strptime(ds, '%Y-%m-%d %H:%M:%S') for ds in dates_str]
            self.datnum = mdates.date2num(datetimes)
            self.datnum.sort()
            
            messagebox.showinfo("Success", f"Successfully loaded {len(self.datnum)} events.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file.\nEnsure format is 'YYYY-MM-DD HH:MM:SS'.\n\nDetails: {e}")
            self.datnum = None

    def process_data(self):
        """Callback for the 'Process' button. It calculates frequencies and runs selected models."""
        if self.datnum is None:
            messagebox.showwarning("No Data", "Please load event data first.")
            return

        try:
            periode = float(self.e_intv.get())
            if periode <= 0: raise ValueError("Interval must be positive.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the time interval.")
            return

        # Set period conversion factor (days is the base unit for mdates)
        unit = self.p_intv_var.get()
        if unit == "Hours":
            jam2hari = 1 / 24
            period_in_days = periode / 24
        else: # Days
            jam2hari = 1
            period_in_days = periode
            
        # Create time bins for the histogram
        start_time, end_time = self.datnum[0], self.datnum[-1]
        bins = np.arange(start_time, end_time + period_in_days, period_in_days)
        
        # Calculate frequency (number of events in each bin)
        frekuensi, rentang_edges = np.histogram(self.datnum, bins=bins)
        rentang_centers = (rentang_edges[:-1] + rentang_edges[1:]) / 2 # Use bin centers for plotting

        # Time count axis for regression (1, 2, 3, ... intervals)
        rentang_count = np.arange(1, len(frekuensi) + 1) * periode

        model_map = {
            "omori": (self.cb_omori_var.get(), self.run_omori, "Omori"),
            "mogi1": (self.cb_mogi1_var.get(), self.run_mogi1, "Mogi I"),
            "mogi2": (self.cb_mogi2_var.get(), self.run_mogi2, "Mogi II"),
            "utsu": (self.cb_utsu_var.get(), self.run_utsu, "Utsu"),
        }

        any_model_run = False
        for key, (is_selected, model_func, model_name) in model_map.items():
            if is_selected:
                try:
                    any_model_run = True
                    model_func(rentang_count, frekuensi, rentang_centers, jam2hari, periode)
                except Exception as e:
                    messagebox.showerror("Model Error", f"Could not generate {model_name} model.\nTrend may be too fluctuating or data is insufficient.\n\nDetails: {e}")
        
        if not any_model_run:
            messagebox.showinfo("No Models Selected", "Please select at least one model to process.")

    def _regression(self, x, y):
        """Wrapper for scipy's linear regression."""
        # Filter out invalid values for log or division
        valid_indices = np.where((np.isfinite(x)) & (np.isfinite(y)))[0]
        if len(valid_indices) < 2:
            raise ValueError("Not enough valid data points for regression.")
            
        x_clean, y_clean = x[valid_indices], y[valid_indices]
        slope, intercept, r_value, _, _ = linregress(x_clean, y_clean)
        return r_value, slope, intercept
    
    def plot_graph(self, rentang, frekuensi, tt_graph, nt, t1_days, r, title_str):
        """Generic plotting function for all models."""
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot observed data and model
        ax.plot(rentang, frekuensi, 'r*', label='Observation')
        ax.plot(tt_graph, nt, 'b-', linewidth=2, label='Model')

        # Formatting
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))
        ax.set_xlim(tt_graph[0], tt_graph[-1])
        ax.set_ylim(0, max(frekuensi) * 1.1)
        ax.set_xlabel('Time', fontweight='bold')
        ax.set_ylabel('Number of Earthquakes', fontweight='bold')
        ax.set_title(title_str, fontsize=14.5)
        ax.legend(loc='best', fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.6)
        
        # Add results text box
        end_date_num = mdates.num2date(rentang[0] + t1_days)
        text_content = (f"T = {t1_days:.0f} Days ({end_date_num.strftime('%d %B %Y')})\n"
                        f"R = {r:.4f}")
        ax.text(0.95, 0.95, text_content, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', horizontalalignment='right',
                bbox=dict(boxstyle='round,pad=0.5', fc='red', alpha=0.2))

        # Add logo
        if self.logo_image:
            logo_ax = fig.add_axes([0.8, 0.8, 0.1, 0.1], anchor='NE', zorder=1)
            logo_ax.imshow(self.logo_image)
            logo_ax.axis('off')

        fig.autofmt_xdate()
        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.show()

    def run_omori(self, rentang_count, frekuensi, rentang_plot, jam2hari, periode):
        y = 1 / frekuensi
        x = rentang_count
        r, B, A = self._regression(x, y)
        a = 1 / B
        b = A * a
        t1 = (a - b) # in units of periode
        tt = np.linspace(rentang_count[0], t1, 500)
        nt = a / (tt + b)
        
        t1_days = t1 * periode * jam2hari
        tt_graph = np.linspace(rentang_plot[0], rentang_plot[0] + t1_days, len(tt))
        self.plot_graph(rentang_plot, frekuensi, tt_graph, nt, t1_days, r, "Earthquake Decay Forecast - OMORI Model")

    def run_mogi1(self, rentang_count, frekuensi, rentang_plot, jam2hari, periode):
        y = np.log10(frekuensi)
        x = np.log10(rentang_count)
        r, B, A = self._regression(x, y)
        a = 10**A
        b = -B
        t1 = 10**(np.log10(a) / b) # in units of periode
        tt = np.linspace(rentang_count[0], t1, 500)
        nt = a * tt**(-b)

        t1_days = t1 * periode * jam2hari
        tt_graph = np.linspace(rentang_plot[0], rentang_plot[0] + t1_days, len(tt))
        self.plot_graph(rentang_plot, frekuensi, tt_graph, nt, t1_days, r, "Earthquake Decay Forecast - MOGI I Model")
        
    def run_mogi2(self, rentang_count, frekuensi, rentang_plot, jam2hari, periode):
        y = np.log(frekuensi)
        x = rentang_count
        r, B, A = self._regression(x, y)
        a = np.exp(A)
        b = -B
        t1 = np.log(a) / b # in units of periode
        tt = np.linspace(rentang_count[0], t1, 500)
        nt = a * np.exp(-b * tt)

        t1_days = t1 * periode * jam2hari
        tt_graph = np.linspace(rentang_plot[0], rentang_plot[0] + t1_days, len(tt))
        self.plot_graph(rentang_plot, frekuensi, tt_graph, nt, t1_days, r, "Earthquake Decay Forecast - MOGI II Model")
        
    def run_utsu(self, rentang_count, frekuensi, rentang_plot, jam2hari, periode):
        c = 0.01 # small constant from original code
        y = np.log10(frekuensi)
        x = np.log10(rentang_count + c)
        r, B, A = self._regression(x, y)
        a = 10**A
        b = -B
        t1 = 10**(np.log10(a) / b) - c # in units of periode
        tt = np.linspace(rentang_count[0], t1, 500)
        nt = a * (tt + c)**(-b)
        
        t1_days = t1 * periode * jam2hari
        tt_graph = np.linspace(rentang_plot[0], rentang_plot[0] + t1_days, len(tt))
        self.plot_graph(rentang_plot, frekuensi, tt_graph, nt, t1_days, r, "Earthquake Decay Forecast - UTSU Model")

    def show_data_histogram(self):
        """Plots a histogram of the raw event data over time."""
        if self.datnum is None:
            messagebox.showwarning("No Data", "Please load event data first.")
            return

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.hist(self.datnum, bins=50) # Using 50 bins for a general overview
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b-%Y'))
        fig.autofmt_xdate()
        
        ax.set_title('Actual Earthquake Decay Data')
        ax.set_xlabel('Date')
        ax.set_ylabel('Number of Earthquakes')
        ax.set_xlim(self.datnum.min(), self.datnum.max())
        ax.grid(True, linestyle='--', alpha=0.6)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = EarthquakeDecayApp(root)
    # Set app icon if available
    try:
        icon = ImageTk.PhotoImage(file='bmkg-icon.jpg')
        root.iconphoto(True, icon)
    except:
        pass # Silently fail if icon not found or Pillow not installed properly
    root.mainloop()
