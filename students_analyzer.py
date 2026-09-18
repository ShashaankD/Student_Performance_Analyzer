import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StudentPerformanceAnalyzer:

    def __init__(self, root):
        self.root = root

        self.root.title("Student Performance Analyzer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 650)

        # -----------------------------------------------------
        # Application variables
        # -----------------------------------------------------

        self.df = None
        self.analysis_df = None
        self.file_path = None

        self.subjects = []
        self.student_id_column = ""
        self.student_name_column = ""

        self.pass_mark = 40
        self.improvement_threshold = 50

        self.chart_figures = []

        # -----------------------------------------------------
        # Style
        # -----------------------------------------------------

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 20, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 10)
        )

        style.configure(
            "Big.TButton",
            font=("Arial", 11, "bold"),
            padding=10
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = ttk.Frame(
            self.root,
            padding=(15, 12)
        )

        header.pack(fill="x")

        ttk.Label(
            header,
            text="📊 Student Performance Analyzer",
            style="Title.TLabel"
        ).pack(anchor="w")

        ttk.Label(
            header,
            text="Upload → Configure → Analyze → Visualize → Understand",
            style="Subtitle.TLabel"
        ).pack(anchor="w", pady=(3, 0))

        # -----------------------------------------------------
        # Notebook
        # -----------------------------------------------------

        self.notebook = ttk.Notebook(
            self.root
        )

        self.notebook.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=(0, 12)
        )

        self.create_upload_tab()
        self.create_dataset_tab()
        self.create_configuration_tab()
        self.create_analysis_tab()
        self.create_charts_tab()

    # =========================================================
    # UPLOAD TAB
    # =========================================================

    def create_upload_tab(self):

        self.upload_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            self.upload_tab,
            text="📂 Upload"
        )

        container = ttk.Frame(
            self.upload_tab
        )

        container.pack(
            fill="both",
            expand=True
        )

        ttk.Label(
            container,
            text="Upload Student Dataset",
            font=("Arial", 18, "bold")
        ).pack(pady=(60, 10))

        ttk.Label(
            container,
            text=(
                "Supported file formats\n\n"
                "CSV  (.csv)\n"
                "Excel  (.xls / .xlsx)"
            ),
            justify="center",
            font=("Arial", 11)
        ).pack(pady=10)

        self.upload_button = ttk.Button(
            container,
            text="📂 SELECT CSV / EXCEL FILE",
            style="Big.TButton",
            command=self.upload_file
        )

        self.upload_button.pack(
            pady=20
        )

        self.file_status = ttk.Label(
            container,
            text="No dataset loaded.",
            font=("Arial", 11)
        )

        self.file_status.pack(
            pady=10
        )

        self.dataset_info = ttk.Label(
            container,
            text="",
            font=("Arial", 10)
        )

        self.dataset_info.pack(
            pady=5
        )

        ttk.Label(
            container,
            text=(
                "After uploading, go to Configuration "
                "to select the Student ID, Student Name "
                "and Subject columns."
            ),
            font=("Arial", 10, "italic"),
            justify="center"
        ).pack(
            pady=30
        )

    # =========================================================
    # DATASET TAB
    # =========================================================

    def create_dataset_tab(self):

        self.dataset_tab = ttk.Frame(
            self.notebook,
            padding=10
        )

        self.notebook.add(
            self.dataset_tab,
            text="📋 Dataset"
        )

        ttk.Label(
            self.dataset_tab,
            text="Dataset Preview",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        table_frame = ttk.Frame(
            self.dataset_tab
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.tree = ttk.Treeview(
            table_frame,
            show="headings"
        )

        vertical_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scrollbar = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scrollbar.set,
            xscrollcommand=horizontal_scrollbar.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scrollbar.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scrollbar.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.rowconfigure(
            0,
            weight=1
        )

        table_frame.columnconfigure(
            0,
            weight=1
        )

        ttk.Label(
            self.dataset_tab,
            text="Showing the first 100 rows.",
            font=("Arial", 9, "italic")
        ).pack(
            anchor="w",
            pady=(6, 0)
        )

    # =========================================================
    # CONFIGURATION TAB
    # =========================================================

    def create_configuration_tab(self):

        self.config_tab = ttk.Frame(
            self.notebook,
            padding=20
        )

        self.notebook.add(
            self.config_tab,
            text="⚙️ Configuration"
        )

        ttk.Label(
            self.config_tab,
            text="Dataset Configuration",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # -----------------------------------------------------
        # Student ID
        # -----------------------------------------------------

        ttk.Label(
            self.config_tab,
            text="Student ID Column:"
        ).pack(
            anchor="w"
        )

        self.student_id_combo = ttk.Combobox(
            self.config_tab,
            state="readonly"
        )

        self.student_id_combo.pack(
            fill="x",
            pady=(3, 12)
        )

        # -----------------------------------------------------
        # Student Name
        # -----------------------------------------------------

        ttk.Label(
            self.config_tab,
            text="Student Name Column:"
        ).pack(
            anchor="w"
        )

        self.student_name_combo = ttk.Combobox(
            self.config_tab,
            state="readonly"
        )

        self.student_name_combo.pack(
            fill="x",
            pady=(3, 12)
        )

        # -----------------------------------------------------
        # Subject columns
        # -----------------------------------------------------

        ttk.Label(
            self.config_tab,
            text="Select Subject Columns:"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            self.config_tab,
            text=(
                "Hold CTRL and click to select multiple "
                "subject columns."
            ),
            font=("Arial", 9, "italic")
        ).pack(
            anchor="w",
            pady=(2, 5)
        )

        subject_frame = ttk.Frame(
            self.config_tab
        )

        subject_frame.pack(
            fill="both",
            expand=True
        )

        self.subject_listbox = tk.Listbox(
            subject_frame,
            selectmode=tk.MULTIPLE,
            font=("Arial", 10),
            height=8
        )

        subject_scrollbar = ttk.Scrollbar(
            subject_frame,
            orient="vertical",
            command=self.subject_listbox.yview
        )

        self.subject_listbox.configure(
            yscrollcommand=subject_scrollbar.set
        )

        self.subject_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        subject_scrollbar.pack(
            side="right",
            fill="y"
        )

        # -----------------------------------------------------
        # Thresholds
        # -----------------------------------------------------

        threshold_frame = ttk.Frame(
            self.config_tab
        )

        threshold_frame.pack(
            fill="x",
            pady=15
        )

        ttk.Label(
            threshold_frame,
            text="Pass Mark:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(0, 8)
        )

        self.pass_entry = ttk.Entry(
            threshold_frame,
            width=10
        )

        self.pass_entry.insert(
            0,
            "40"
        )

        self.pass_entry.grid(
            row=0,
            column=1,
            padx=(0, 35)
        )

        ttk.Label(
            threshold_frame,
            text="Improvement Threshold:"
        ).grid(
            row=0,
            column=2,
            sticky="w",
            padx=(0, 8)
        )

        self.improvement_entry = ttk.Entry(
            threshold_frame,
            width=10
        )

        self.improvement_entry.insert(
            0,
            "50"
        )

        self.improvement_entry.grid(
            row=0,
            column=3
        )

        # -----------------------------------------------------
        # Analyze button
        # -----------------------------------------------------

        ttk.Button(
            self.config_tab,
            text="🚀 ANALYZE DATASET",
            style="Big.TButton",
            command=self.analyze_dataset
        ).pack(
            pady=10
        )

    # =========================================================
    # ANALYSIS TAB
    # =========================================================

    def create_analysis_tab(self):

        self.analysis_tab = ttk.Frame(
            self.notebook,
            padding=10
        )

        self.notebook.add(
            self.analysis_tab,
            text="📄 Analysis Report"
        )

        ttk.Label(
            self.analysis_tab,
            text="Student Performance Analysis Report",
            font=("Arial", 16, "bold")
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        self.result_text = ScrolledText(
            self.analysis_tab,
            wrap=tk.WORD,
            font=("Consolas", 11),
            padx=15,
            pady=15
        )

        self.result_text.pack(
            fill="both",
            expand=True
        )

        self.result_text.insert(
            tk.END,
            "Upload a dataset and configure the columns.\n\n"
            "Then click 'ANALYZE DATASET' to generate "
            "the complete report."
        )

        self.result_text.config(
            state=tk.DISABLED
        )

    # =========================================================
    # CHARTS TAB
    # =========================================================

    def create_charts_tab(self):

        self.charts_tab = ttk.Frame(
            self.notebook,
            padding=10
        )

        self.notebook.add(
            self.charts_tab,
            text="📈 Charts"
        )

        self.chart_notebook = ttk.Notebook(
            self.charts_tab
        )

        self.chart_notebook.pack(
            fill="both",
            expand=True
        )

        self.subject_chart_tab = ttk.Frame(
            self.chart_notebook
        )

        self.top5_chart_tab = ttk.Frame(
            self.chart_notebook
        )

        self.passfail_chart_tab = ttk.Frame(
            self.chart_notebook
        )

        self.chart_notebook.add(
            self.subject_chart_tab,
            text="Subject Performance"
        )

        self.chart_notebook.add(
            self.top5_chart_tab,
            text="Top 5 Students"
        )

        self.chart_notebook.add(
            self.passfail_chart_tab,
            text="Pass / Fail"
        )

        ttk.Label(
            self.subject_chart_tab,
            text="Analyze a dataset to display charts.",
            font=("Arial", 11)
        ).pack(
            pady=30
        )

    # =========================================================
    # UPLOAD FILE
    # =========================================================

    def upload_file(self):

        file_path = filedialog.askopenfilename(
            title="Select Student Dataset",
            filetypes=[
                (
                    "Supported Files",
                    "*.csv *.xls *.xlsx"
                ),
                (
                    "CSV Files",
                    "*.csv"
                ),
                (
                    "Excel Files",
                    "*.xls *.xlsx"
                ),
                (
                    "All Files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        try:

            extension = os.path.splitext(
                file_path
            )[1].lower()

            if extension == ".csv":

                dataframe = pd.read_csv(
                    file_path
                )

            elif extension in [".xls", ".xlsx"]:

                dataframe = pd.read_excel(
                    file_path
                )

            else:

                messagebox.showerror(
                    "Unsupported File",
                    "Please select a CSV, XLS, or XLSX file."
                )

                return

            if dataframe.empty:

                messagebox.showerror(
                    "Empty Dataset",
                    "The selected file contains no data."
                )

                return

            # Store dataset
            self.df = dataframe
            self.file_path = file_path

            # Update status
            self.file_status.config(
                text=(
                    "Loaded: "
                    + os.path.basename(file_path)
                )
            )

            self.dataset_info.config(
                text=(
                    f"Rows: {len(dataframe)}    |    "
                    f"Columns: {len(dataframe.columns)}"
                )
            )

            # Display data
            self.populate_dataset_table()

            # Populate configuration
            self.populate_column_selection()

            # Go to configuration
            self.notebook.select(
                self.config_tab
            )

            messagebox.showinfo(
                "Dataset Loaded",
                "Dataset loaded successfully!\n\n"
                "Now select the Student ID, Student Name "
                "and Subject columns."
            )

        except Exception as error:

            messagebox.showerror(
                "File Loading Error",
                "The dataset could not be loaded.\n\n"
                + str(error)
            )

    # =========================================================
    # POPULATE DATASET TABLE
    # =========================================================

    def populate_dataset_table(self):

        # Clear existing table
        for item in self.tree.get_children():

            self.tree.delete(
                item
            )

        # Set columns
        columns = list(
            self.df.columns
        )

        self.tree["columns"] = columns

        for column in columns:

            self.tree.heading(
                column,
                text=str(column)
            )

            self.tree.column(
                column,
                width=140,
                minwidth=80
            )

        # Insert first 100 rows
        preview = self.df.head(100)

        for _, row in preview.iterrows():

            values = []

            for value in row:

                if pd.isna(value):

                    values.append("")

                else:

                    values.append(
                        str(value)
                    )

            self.tree.insert(
                "",
                tk.END,
                values=values
            )

    # =========================================================
    # POPULATE COLUMN SELECTION
    # =========================================================

    def populate_column_selection(self):

        columns = [
            str(column)
            for column in self.df.columns
        ]

        # Student ID
        self.student_id_combo["values"] = columns
        self.student_id_combo.set("")

        # Student Name
        self.student_name_combo["values"] = columns
        self.student_name_combo.set("")

        # Subjects
        self.subject_listbox.delete(
            0,
            tk.END
        )

        for column in columns:

            self.subject_listbox.insert(
                tk.END,
                column
            )

    # =========================================================
    # CLEAN DATA
    # =========================================================

    def clean_data(self):

        dataframe = self.df.copy()

        # Clean column names
        dataframe.columns = [
            str(column).strip()
            for column in dataframe.columns
        ]

        # Remove completely empty rows
        dataframe.dropna(
            how="all",
            inplace=True
        )

        # Remove duplicate rows
        dataframe.drop_duplicates(
            inplace=True
        )

        return dataframe

    # =========================================================
    # ANALYZE DATASET
    # =========================================================

    def analyze_dataset(self):

        # -----------------------------------------------------
        # Check dataset
        # -----------------------------------------------------

        if self.df is None:

            messagebox.showwarning(
                "No Dataset",
                "Please upload a dataset first."
            )

            self.notebook.select(
                self.upload_tab
            )

            return

        # -----------------------------------------------------
        # Get selections
        # -----------------------------------------------------

        student_id = (
            self.student_id_combo.get()
        )

        student_name = (
            self.student_name_combo.get()
        )

        selected_indices = (
            self.subject_listbox.curselection()
        )

        subjects = [
            self.subject_listbox.get(index)
            for index in selected_indices
        ]

        # -----------------------------------------------------
        # Validate Student ID
        # -----------------------------------------------------

        if not student_id:

            messagebox.showwarning(
                "Student ID Missing",
                "Please select the Student ID column."
            )

            return

        # -----------------------------------------------------
        # Validate Student Name
        # -----------------------------------------------------

        if not student_name:

            messagebox.showwarning(
                "Student Name Missing",
                "Please select the Student Name column."
            )

            return

        # -----------------------------------------------------
        # Validate Subjects
        # -----------------------------------------------------

        if not subjects:

            messagebox.showwarning(
                "No Subjects Selected",
                "Please select at least one subject column."
            )

            return

        # -----------------------------------------------------
        # Read thresholds
        # -----------------------------------------------------

        try:

            pass_mark = float(
                self.pass_entry.get()
            )

            improvement_threshold = float(
                self.improvement_entry.get()
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Threshold",
                "Pass Mark and Improvement Threshold "
                "must be numbers."
            )

            return

        if pass_mark < 0 or pass_mark > 100:

            messagebox.showerror(
                "Invalid Pass Mark",
                "Pass Mark must be between 0 and 100."
            )

            return

        if (
            improvement_threshold < 0
            or improvement_threshold > 100
        ):

            messagebox.showerror(
                "Invalid Improvement Threshold",
                "Improvement Threshold must be "
                "between 0 and 100."
            )

            return

        # -----------------------------------------------------
        # Clean data
        # -----------------------------------------------------

        dataframe = self.clean_data()

        # -----------------------------------------------------
        # Check columns
        # -----------------------------------------------------

        required_columns = [
            student_id,
            student_name
        ] + subjects

        missing_columns = [
            column
            for column in required_columns
            if column not in dataframe.columns
        ]

        if missing_columns:

            messagebox.showerror(
                "Missing Columns",
                "These selected columns were not found:\n\n"
                + "\n".join(missing_columns)
            )

            return

        # -----------------------------------------------------
        # Convert subject columns to numbers
        # -----------------------------------------------------

        conversion_information = []

        for subject in subjects:

            before_conversion = (
                dataframe[subject].notna().sum()
            )

            dataframe[subject] = pd.to_numeric(
                dataframe[subject],
                errors="coerce"
            )

            after_conversion = (
                dataframe[subject].notna().sum()
            )

            conversion_information.append(
                f"{subject}: "
                f"{after_conversion} numeric values "
                f"out of {before_conversion}"
            )

        # -----------------------------------------------------
        # Check whether marks exist
        # -----------------------------------------------------

        total_valid_marks = (
            dataframe[subjects]
            .notna()
            .sum()
            .sum()
        )

        if total_valid_marks == 0:

            messagebox.showerror(
                "No Valid Marks",
                "None of the selected subject columns "
                "contain numeric marks.\n\n"
                "Please check your subject selections."
            )

            return

        # -----------------------------------------------------
        # Remove rows with no subject marks
        # -----------------------------------------------------

        dataframe.dropna(
            subset=subjects,
            how="all",
            inplace=True
        )

        if dataframe.empty:

            messagebox.showerror(
                "No Student Records",
                "No usable student records remain "
                "after cleaning."
            )

            return

        # -----------------------------------------------------
        # Fill missing marks with subject average
        # -----------------------------------------------------

        missing_information = []

        for subject in subjects:

            missing_count = (
                dataframe[subject].isna().sum()
            )

            if missing_count > 0:

                subject_mean = (
                    dataframe[subject].mean()
                )

                if pd.isna(subject_mean):

                    messagebox.showerror(
                        "Invalid Subject",
                        f"Subject '{subject}' does not "
                        "contain usable numeric marks."
                    )

                    return

                dataframe[subject] = (
                    dataframe[subject]
                    .fillna(subject_mean)
                )

                missing_information.append(
                    f"{subject}: {missing_count} missing "
                    f"value(s) filled with subject average"
                )

        # -----------------------------------------------------
        # Remove invalid marks
        # -----------------------------------------------------

        invalid_rows = pd.Series(
            False,
            index=dataframe.index
        )

        for subject in subjects:

            invalid_rows = (
                invalid_rows
                | (dataframe[subject] < 0)
                | (dataframe[subject] > 100)
            )

        invalid_count = int(
            invalid_rows.sum()
        )

        if invalid_count > 0:

            dataframe = dataframe.loc[
                ~invalid_rows
            ].copy()

        # -----------------------------------------------------
        # Final student count check
        # -----------------------------------------------------

        total_students = len(
            dataframe
        )

        if total_students == 0:

            messagebox.showerror(
                "No Valid Students",
                "All student records were removed "
                "because their marks were outside "
                "the valid range of 0 to 100."
            )

            return

        # -----------------------------------------------------
        # Calculate Total
        # -----------------------------------------------------

        dataframe["Total"] = (
            dataframe[subjects]
            .sum(axis=1)
        )

        # -----------------------------------------------------
        # Calculate Average
        # -----------------------------------------------------

        dataframe["Average"] = (
            dataframe[subjects]
            .mean(axis=1)
        )

        # -----------------------------------------------------
        # Pass / Fail
        # -----------------------------------------------------

        dataframe["Result"] = (
            dataframe[subjects] >= pass_mark
        ).all(axis=1)

        # -----------------------------------------------------
        # Overall statistics
        # -----------------------------------------------------

        overall_average = (
            dataframe["Average"].mean()
        )

        highest_mark = (
            dataframe[subjects].max().max()
        )

        lowest_mark = (
            dataframe[subjects].min().min()
        )

        # -----------------------------------------------------
        # Subject averages
        # -----------------------------------------------------

        subject_averages = (
            dataframe[subjects]
            .mean()
            .sort_values(
                ascending=False
            )
        )

        # -----------------------------------------------------
        # Pass / Fail counts
        # -----------------------------------------------------

        pass_count = int(
            dataframe["Result"].sum()
        )

        fail_count = int(
            total_students - pass_count
        )

        # -----------------------------------------------------
        # SAFETY CHECK
        # -----------------------------------------------------

        if total_students <= 0:

            messagebox.showerror(
                "Analysis Error",
                "There are no students available "
                "for analysis."
            )

            return

        # -----------------------------------------------------
        # Percentages
        # -----------------------------------------------------

        pass_percentage = (
            pass_count / total_students
        ) * 100

        fail_percentage = (
            fail_count / total_students
        ) * 100

        # -----------------------------------------------------
        # Top 5
        # -----------------------------------------------------

        top5 = (
            dataframe
            .sort_values(
                by="Average",
                ascending=False
            )
            .head(5)
        )

        # -----------------------------------------------------
        # Improvement students
        # -----------------------------------------------------

        improvement_students = (
            dataframe[
                dataframe["Average"]
                < improvement_threshold
            ]
            .sort_values(
                by="Average"
            )
        )

        # -----------------------------------------------------
        # Store analysis information
        # -----------------------------------------------------

        self.analysis_df = dataframe
        self.subjects = subjects
        self.student_id_column = student_id
        self.student_name_column = student_name
        self.pass_mark = pass_mark
        self.improvement_threshold = (
            improvement_threshold
        )

        # -----------------------------------------------------
        # Generate report
        # -----------------------------------------------------

        report = self.generate_report(
            dataframe,
            subjects,
            student_id,
            student_name,
            overall_average,
            highest_mark,
            lowest_mark,
            subject_averages,
            pass_count,
            fail_count,
            pass_percentage,
            fail_percentage,
            top5,
            improvement_students,
            invalid_count,
            conversion_information,
            missing_information
        )

        # -----------------------------------------------------
        # Display report
        # -----------------------------------------------------

        self.result_text.config(
            state=tk.NORMAL
        )

        self.result_text.delete(
            "1.0",
            tk.END
        )

        self.result_text.insert(
            tk.END,
            report
        )

        self.result_text.config(
            state=tk.DISABLED
        )

        # -----------------------------------------------------
        # Create charts
        # -----------------------------------------------------

        self.create_charts(
            dataframe,
            subjects,
            top5,
            pass_count,
            fail_count
        )

        # -----------------------------------------------------
        # Show report
        # -----------------------------------------------------

        self.notebook.select(
            self.analysis_tab
        )

        messagebox.showinfo(
            "Analysis Complete",
            "Analysis completed successfully!\n\n"
            f"Students analyzed: {total_students}\n"
            f"Subjects analyzed: {len(subjects)}"
        )

    # =========================================================
    # GENERATE REPORT
    # =========================================================

    def generate_report(
        self,
        dataframe,
        subjects,
        student_id,
        student_name,
        overall_average,
        highest_mark,
        lowest_mark,
        subject_averages,
        pass_count,
        fail_count,
        pass_percentage,
        fail_percentage,
        top5,
        improvement_students,
        invalid_count,
        conversion_information,
        missing_information
    ):

        report = ""

        report += "=" * 78 + "\n"
        report += (
            "           STUDENT PERFORMANCE ANALYSIS REPORT\n"
        )
        report += "=" * 78 + "\n\n"

        # -----------------------------------------------------
        # Dataset information
        # -----------------------------------------------------

        report += "1. DATASET INFORMATION\n"
        report += "-" * 78 + "\n"

        report += (
            f"File                : "
            f"{os.path.basename(self.file_path)}\n"
        )

        report += (
            f"Students Analyzed   : "
            f"{len(dataframe)}\n"
        )

        report += (
            f"Subjects Analyzed   : "
            f"{len(subjects)}\n"
        )

        report += (
            f"Student ID Column   : "
            f"{student_id}\n"
        )

        report += (
            f"Student Name Column : "
            f"{student_name}\n"
        )

        report += (
            f"Pass Mark           : "
            f"{self.pass_mark}\n"
        )

        report += (
            f"Improvement Limit   : "
            f"{self.improvement_threshold}\n"
        )

        report += (
            f"Subjects            : "
            f"{', '.join(subjects)}\n\n"
        )

        # -----------------------------------------------------
        # Data cleaning
        # -----------------------------------------------------

        report += "2. DATA CLEANING\n"
        report += "-" * 78 + "\n"

        report += (
            "The dataset was cleaned before analysis.\n\n"
        )

        report += (
            f"Invalid mark rows removed: "
            f"{invalid_count}\n"
        )

        if missing_information:

            report += (
                "\nMissing values handled:\n"
            )

            for item in missing_information:

                report += (
                    f"• {item}\n"
                )

        else:

            report += (
                "Missing subject values: None requiring "
                "replacement.\n"
            )

        report += (
            "\nNumeric conversion:\n"
        )

        for item in conversion_information:

            report += (
                f"• {item}\n"
            )

        report += "\n"

        # -----------------------------------------------------
        # Overall performance
        # -----------------------------------------------------

        report += "3. OVERALL PERFORMANCE\n"
        report += "-" * 78 + "\n"

        report += (
            f"Overall Average : "
            f"{overall_average:.2f}\n"
        )

        report += (
            f"Highest Mark    : "
            f"{highest_mark:.2f}\n"
        )

        report += (
            f"Lowest Mark     : "
            f"{lowest_mark:.2f}\n\n"
        )

        # -----------------------------------------------------
        # Subject performance
        # -----------------------------------------------------

        report += "4. SUBJECT-WISE PERFORMANCE\n"
        report += "-" * 78 + "\n"

        for subject, average in subject_averages.items():

            report += (
                f"{subject:<30}"
                f" Average: {average:.2f}\n"
            )

        report += "\n"

        # -----------------------------------------------------
        # Pass fail
        # -----------------------------------------------------

        report += "5. PASS / FAIL ANALYSIS\n"
        report += "-" * 78 + "\n"

        report += (
            f"Passed Students : "
            f"{pass_count}\n"
        )

        report += (
            f"Failed Students : "
            f"{fail_count}\n"
        )

        report += (
            f"Pass Percentage : "
            f"{pass_percentage:.2f}%\n"
        )

        report += (
            f"Fail Percentage : "
            f"{fail_percentage:.2f}%\n\n"
        )

        # -----------------------------------------------------
        # Top 5
        # -----------------------------------------------------

        report += "6. TOP 5 STUDENTS\n"
        report += "-" * 78 + "\n"

        for rank, (_, row) in enumerate(
            top5.iterrows(),
            start=1
        ):

            report += (
                f"{rank}. "
                f"{row[student_name]} "
                f"({row[student_id]})"
                f"  →  Average: "
                f"{row['Average']:.2f}\n"
            )

        report += "\n"

        # -----------------------------------------------------
        # Improvement
        # -----------------------------------------------------

        report += "7. STUDENTS NEEDING IMPROVEMENT\n"
        report += "-" * 78 + "\n"

        if improvement_students.empty:

            report += (
                "No students are below the "
                f"{self.improvement_threshold} "
                "average threshold.\n"
            )

        else:

            for _, row in (
                improvement_students.iterrows()
            ):

                report += (
                    f"• {row[student_name]} "
                    f"({row[student_id]})"
                    f"  →  Average: "
                    f"{row['Average']:.2f}\n"
                )

        report += "\n"

        # -----------------------------------------------------
        # Insights
        # -----------------------------------------------------

        report += "8. AUTOMATIC INSIGHTS\n"
        report += "-" * 78 + "\n"

        best_subject = (
            subject_averages.idxmax()
        )

        lowest_subject = (
            subject_averages.idxmin()
        )

        top_student = (
            top5.iloc[0]
        )

        report += (
            f"• The overall average mark is "
            f"{overall_average:.2f}.\n"
        )

        report += (
            f"• {best_subject} has the highest "
            f"subject average of "
            f"{subject_averages[best_subject]:.2f}.\n"
        )

        report += (
            f"• {lowest_subject} has the lowest "
            f"subject average of "
            f"{subject_averages[lowest_subject]:.2f}.\n"
        )

        report += (
            f"• {pass_percentage:.2f}% of students "
            f"passed all selected subjects.\n"
        )

        report += (
            f"• {fail_percentage:.2f}% of students "
            f"failed at least one selected subject.\n"
        )

        report += (
            f"• The highest average in this dataset "
            f"belongs to {top_student[student_name]} "
            f"with an average of "
            f"{top_student['Average']:.2f}.\n"
        )

        report += (
            f"• {len(improvement_students)} student(s) "
            f"are below the improvement threshold "
            f"of {self.improvement_threshold}.\n"
        )

        report += "\n"

        # -----------------------------------------------------
        # Final summary
        # -----------------------------------------------------

        report += "9. FINAL SUMMARY\n"
        report += "-" * 78 + "\n"

        report += (
            "The Student Performance Analyzer "
            "processes student data by cleaning the "
            "dataset, calculating statistical measures, "
            "comparing subject performance, identifying "
            "top-performing students, detecting students "
            "who may need additional support, and "
            "presenting the findings through charts "
            "and automatic insights.\n"
        )

        report += "\n"
        report += "=" * 78 + "\n"
        report += "                    END OF REPORT\n"
        report += "=" * 78 + "\n"

        return report

    # =========================================================
    # CREATE CHARTS
    # =========================================================

    def create_charts(
        self,
        dataframe,
        subjects,
        top5,
        pass_count,
        fail_count
    ):

        # -----------------------------------------------------
        # Clear old chart widgets
        # -----------------------------------------------------

        for widget in (
            self.subject_chart_tab.winfo_children()
        ):

            widget.destroy()

        for widget in (
            self.top5_chart_tab.winfo_children()
        ):

            widget.destroy()

        for widget in (
            self.passfail_chart_tab.winfo_children()
        ):

            widget.destroy()

        # -----------------------------------------------------
        # Close old figures
        # -----------------------------------------------------

        for figure in self.chart_figures:

            plt.close(
                figure
            )

        self.chart_figures = []

        # =====================================================
        # SUBJECT PERFORMANCE CHART
        # =====================================================

        subject_average = (
            dataframe[subjects]
            .mean()
        )

        figure1, axis1 = plt.subplots(
            figsize=(8, 5)
        )

        subject_average.plot(
            kind="bar",
            ax=axis1
        )

        axis1.set_title(
            "Average Marks by Subject"
        )

        axis1.set_xlabel(
            "Subjects"
        )

        axis1.set_ylabel(
            "Average Marks"
        )

        axis1.set_ylim(
            0,
            100
        )

        axis1.tick_params(
            axis="x",
            rotation=30
        )

        figure1.tight_layout()

        canvas1 = FigureCanvasTkAgg(
            figure1,
            master=self.subject_chart_tab
        )

        canvas1.draw()

        canvas1.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.chart_figures.append(
            figure1
        )

        # =====================================================
        # TOP 5 CHART
        # =====================================================

        figure2, axis2 = plt.subplots(
            figsize=(8, 5)
        )

        names = [
            str(name)
            for name in top5[
                self.student_name_column
            ]
        ]

        averages = (
            top5["Average"]
        )

        axis2.bar(
            names,
            averages
        )

        axis2.set_title(
            "Top 5 Students by Average"
        )

        axis2.set_xlabel(
            "Students"
        )

        axis2.set_ylabel(
            "Average Marks"
        )

        axis2.set_ylim(
            0,
            100
        )

        axis2.tick_params(
            axis="x",
            rotation=30
        )

        figure2.tight_layout()

        canvas2 = FigureCanvasTkAgg(
            figure2,
            master=self.top5_chart_tab
        )

        canvas2.draw()

        canvas2.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.chart_figures.append(
            figure2
        )

        # =====================================================
        # PASS / FAIL CHART
        # =====================================================

        figure3, axis3 = plt.subplots(
            figsize=(7, 5)
        )

        axis3.pie(
            [pass_count, fail_count],
            labels=[
                "Passed",
                "Failed"
            ],
            autopct="%1.1f%%",
            startangle=90
        )

        axis3.set_title(
            "Pass / Fail Distribution"
        )

        figure3.tight_layout()

        canvas3 = FigureCanvasTkAgg(
            figure3,
            master=self.passfail_chart_tab
        )

        canvas3.draw()

        canvas3.get_tk_widget().pack(
            fill="both",
            expand=True
        )

        self.chart_figures.append(
            figure3
        )

        # -----------------------------------------------------
        # Save PNG charts
        # -----------------------------------------------------

        self.save_charts(
            subject_average,
            top5,
            pass_count,
            fail_count
        )

    # =========================================================
    # SAVE CHARTS
    # =========================================================

    def save_charts(
        self,
        subject_average,
        top5,
        pass_count,
        fail_count
    ):

        try:

            os.makedirs(
                "charts",
                exist_ok=True
            )

            # -------------------------------------------------
            # Subject performance
            # -------------------------------------------------

            figure, axis = plt.subplots(
                figsize=(8, 5)
            )

            subject_average.plot(
                kind="bar",
                ax=axis
            )

            axis.set_title(
                "Average Marks by Subject"
            )

            axis.set_xlabel(
                "Subjects"
            )

            axis.set_ylabel(
                "Average Marks"
            )

            axis.set_ylim(
                0,
                100
            )

            figure.tight_layout()

            figure.savefig(
                "charts/subject_performance.png",
                dpi=150
            )

            plt.close(
                figure
            )

            # -------------------------------------------------
            # Top 5
            # -------------------------------------------------

            figure, axis = plt.subplots(
                figsize=(8, 5)
            )

            names = [
                str(name)
                for name in top5[
                    self.student_name_column
                ]
            ]

            averages = (
                top5["Average"]
            )

            axis.bar(
                names,
                averages
            )

            axis.set_title(
                "Top 5 Students"
            )

            axis.set_xlabel(
                "Students"
            )

            axis.set_ylabel(
                "Average Marks"
            )

            axis.set_ylim(
                0,
                100
            )

            axis.tick_params(
                axis="x",
                rotation=30
            )

            figure.tight_layout()

            figure.savefig(
                "charts/top_5_students.png",
                dpi=150
            )

            plt.close(
                figure
            )

            # -------------------------------------------------
            # Pass / Fail
            # -------------------------------------------------

            figure, axis = plt.subplots(
                figsize=(7, 5)
            )

            axis.pie(
                [pass_count, fail_count],
                labels=[
                    "Passed",
                    "Failed"
                ],
                autopct="%1.1f%%",
                startangle=90
            )

            axis.set_title(
                "Pass / Fail Distribution"
            )

            figure.tight_layout()

            figure.savefig(
                "charts/pass_fail.png",
                dpi=150
            )

            plt.close(
                figure
            )

        except Exception as error:

            print(
                "Chart saving error:",
                error
            )


# =============================================================
# PROGRAM START
# =============================================================

if __name__ == "__main__":

    root = tk.Tk()

    application = (
        StudentPerformanceAnalyzer(root)
    )

    root.mainloop()