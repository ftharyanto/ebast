# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to Semantic Versioning (though we are not using explicit version numbers currently).

## 2025-05-11 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-05-11&until=2025-05-11))

### Enhanced
- Improved suggestion dropdowns in kelompok_form and errorstation_form to display all options when the input is focused, even if empty.
- Updated CSS for better visibility and usability of suggestion dropdowns.
- Updated base.html to use Bootstrap 5.3.6 for improved styling and functionality.
- Cleaned up unnecessary script imports in kelompok_form.html.

## 2025-05-10 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-05-10&until=2025-05-10))

### Enhanced
- Improved suggestion dropdown functionality in kelompok_form and errorstation_form:
  - Updated CSS to style suggestion dropdowns for better visibility and usability.
  - Modified JavaScript in kelompok_form.js to show all suggestions when the input is focused, even if empty.
  - Adjusted errorstation_form.js to display all stations when the input is empty, improving user experience.
- Updated base.html to use the latest Bootstrap version for improved styling and functionality.
- Cleaned up unnecessary script imports in kelompok_form.html.

## 2025-05-09 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-05-09&until=2025-05-09))

### Added
- Add ErrorStation model, views, forms, and templates; update base template and settings

### Changed
- Update CHANGELOG.md to include full changelog that links to the commit

## 2025-05-08 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-05-08&until=2025-05-08))

### Fixed
- BAST: Fix notes not shown in exported Excel and PDF

## 2025-05-06 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-05-06&until=2025-05-06))

### Changed
- Update ID fields in models to be unique across all applications to prevent duplicate ID
- Update the character limit of the ID on all apps
- Update the id format for all apps, create a script to update the existing id
### Fixed
- Fix repeating word on export excel function of QC and QCFM apps
- Fix the automatic CS input in BAST form
### Removed
- Delete .cursor folder
### Merged
- Merge pull request #12 from ftharyanto/11-fix-the-id-sorting-issue-by-changing-the-id-format

## 2025-04-28 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-28&until=2025-04-28))

### Fixed
- BAST: Fix the default_row_height
- BAST: Fix row height difference in 6th row on export excel and pdf

## 2025-04-25 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-25&until=2025-04-25))

### Fixed
- BAST: 1. Fix BAST template by removing the default value in excel file. 2. Fix the numbering of member data.

## 2025-04-21 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-21&until=2025-04-21))

### Added
- Add "Blank" column to show the count_blanks in cs_list.html and truncate the operator name shown in the table if it's longer than it should
### Fixed
- Fix: calculation of selisih is not included in the event csv form and enhance the accordion part in BAST app

## 2025-04-20 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-20&until=2025-04-20))

### Added
- Text_formatter: add tutorial on how to use it
### Changed
- Update table column widths in cs_list and operator_list templates for better layout
### Fixed
- Fix drag-handle is not working

## 2025-04-19 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-19&until=2025-04-19))

### Changed
- Text formatter: change new line addition from 2 to 1
- Text formatter: change new line addition from 2 to 1

## 2025-04-18 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-18&until=2025-04-18))

### Changed
- Enhance the UI: Navbar, form container
- Refactor table column alignment and styles in kelompok form for consistency
- Refactor table layouts and styles across multiple templates; add base CSS for consistent styling

## 2025-04-17 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-17&until=2025-04-17))

### Added
- Add staticfiles_urlpatterns to urlpatterns in development settings
### Changed
- Enhance the table stylings for all the apps
- Change /github.com/
- Refactor kelompok form: move the styling and js to separate files
- Enhance kelompok form with drag-and-drop functionality and improved styling
### Fixed
- Fix navbar, add /github.comitignore
### Removed
- Remove top margin from page header in kelompok form styles. Add collectstatic to the update_ebast.sh
- Untrack static root directory
- Untrack static root directory

## 2025-04-04 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-04-04&until=2025-04-04))

### Fixed
- Fix datetime automatic input for 'M' case in BAST record form

## 2025-03-28 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-28&until=2025-03-28))

### Added
- Add NIP input handling and save functionality in QC Record Form
- Add member attendance count to BAST sheet generation

## 2025-03-22 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-22&until=2025-03-22))

### Added
- Add data source link to QC FM Record Form
### Changed
- Update QC App link to QC Waveform and add data source reference in QC Record Form

## 2025-03-21 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-21&until=2025-03-21))

### Added
- Add instruction for users to fill in their NIP on the homepage
### Changed
- Update Pagi shift time to '08:00 - 14:00 WIB'
### Fixed
- Fix filter functionality in operator list

## 2025-03-20 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-20&until=2025-03-20))

### Changed
- Automatically expand fetched data section on data retrieval in bastrecord_form.html
- Update homepage description for clarity on services offered
- Update homepage layout and enhance accordion functionality in forms for better user experience
### Fixed
- Fix column name formatting in clean_fm_data function to ensure consistent display of 'CLVD (%)'

## 2025-03-19 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-19&until=2025-03-19))

###Changed
- Refactor text formatting in text_formatter.html to improve newline handling, align first line center, and justify paragraphs
- Enhance text formatting in text_formatter.html to add new line after the second line and apply justify and center alignment to paragraphs

## 2025-03-18 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-18&until=2025-03-18))

### Changed
- Update update_ebast.sh to use makemigrations and migrate commands instead of dmigrate
- Enhance table styling in bastrecord_list.html and add update script for applying update of this project
- Update .gitignore to include Django migrations, Python cache files, media, and SQLite database
- Refactor the export excel and pdf functions on all apps
### Fixed
- Fix the navbar issue
### Removed
- Remove tracked media and db.sqlite3 files
- Remove tracked migrations and pycache folders
- Remove event Indonesia and Luar Negeri fields from export functions in views.py
- Remove unused event fields from QcFmRecord model and clean up related forms. Fix the navbar issue

## 2025-03-16 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-16&until=2025-03-16))

### Changed
- Refactor operator fetching in kelompok_form.html to return operators and improve member ID handling
- Update expiration dates in BastRecordModel and fix member data handling in bastrecord_form.html
- Adjust row height and text alignment for MMI values in Excel and PDF exports
- Enhance member data handling in bastrecord_form.html and update context in views.py
- Update export functions to include location in date and adjust column titles for clarity
- Refactor Focmec app to QcFm, updating models, forms, views, and URLs; remove obsolete files
### Fixed
- Fix event export to PDF by adjusting row indexing and header inclusion
### Removed
- Remove code column from kelompok list view
### Merged
- Merge branch 'focmec' Add QC Focal Mechanism

## 2025-03-13 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-13&until=2025-03-13))

### Added
- Add "orang" to BAST.xlsx
- Initialize Focmec app with models, forms, views, and templates for QC focal mechanism records
- Add total event count to Excel and PDF exports
### Removed
- Remove 'pulsa_samsung' field from BastRecordModel and update related forms and exports

## 2025-03-10 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-10&until=2025-03-10))

### Added
- Add NIP field to Excel and PDF exports in record views
- Add 'waktu_cs' field to BastRecordModel and update related forms and exports
- Add JSON parsing for member data in Excel export and limit member display to 9 entries
### Changed
- Make waktu_pelaksanaan to be selected automatically based on selected date input
- Rename 'waktu_pelaksaan' to 'waktu_pelaksanaan' in BastRecordModel and update related templates and exports
- Handle NaN values in selisihPGR calculation to prevent display errors
- Handle NaN values in selisihPGN display to prevent NaN content in bastrecord_form.html
- Omit cells with tooltips from CSV export and trigger conversion on table updates
### Fixed
- Fix typo in 'waktu_pelaksaan' field name to 'waktu_pelaksanaan' in BastRecordModel
- Fix cell alignment in Excel export by updating the column index for alignment settings
- Fix CSV export function by adding headers and improve cell alignment in Excel export

## 2025-03-08 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-08&until=2025-03-08))

### Changed
- Update .gitignore to exclude all __pycache__ directories and enhance HTML tooltips for MMI and Dis. PGN fields
### Removed
- Remove duplicate info icons in MMI and Dis. PGN tooltip sections in bastrecord_form.html

## 2025-03-06 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-06&until=2025-03-06))

### Merged
- Merge BAST to main

## 2025-03-02 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-03-02&until=2025-03-02))

### Added
- Add environment.yml for project dependencies

## 2025-02-26 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-26&until=2025-02-26))

### Fixed
- Fix cs_id is not updated when updating the record

## 2025-02-18 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-18&until=2025-02-18))

### Changed
- Change PDF export command in export_to_pdf function to use Calc format

## 2025-02-16 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-16&until=2025-02-16))

### Changed
- Refactor clean_sensor function to improve data validation by using a new list for cleaned sensor data instead of modifying the existing list
### Fixed
- Fix date formatting in CS export functions to handle night shift date

## 2025-02-15 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-15&until=2025-02-15))

### Changed
- Change PDF export command in CS export function to use Calc format
### Fixed
- Fix range in Excel export functions to iterate through rows 7 to 249

## 2025-02-13 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-13&until=2025-02-13))

### Added
- Add pagination and filtering to CS list table for improved usability
### Changed
- Update last update display in CS form to use bold formatting for better visibility
- Alter 'jam_pelaksanaan' field in QC record to use a default TimeField with UTC timezone
- Enhance table layouts in CS and QC record lists for improved readability and usability
- Change datetime input in QC form to use 24h format

## 2025-02-10 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-10&until=2025-02-10))

### Added
- Add kelompok column in QC List, adjust table for QC list and CS list
- Add option for group 6 in KELOMPOK selections
### Changed
- Improve CSV upload instructions and enhance form layout for better clarity
- Improve CSV upload guide and enhance operator form layout
- Enhance CS list table styling by adding striped rows for better readability

## 2025-02-09 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-09&until=2025-02-09))

### Fixed
- Fix error on get_hari_indonesia function

## 2025-02-03 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-02-03&until=2025-02-03))

### Fixed
- Fix the default date input and time input

## 2025-01-28 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-28&until=2025-01-28))

### Changed
- Make the table to be smaller in QC form and emove obsolete migration files for qcrecord model and clean up migration history

## 2025-01-27 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-27&until=2025-01-27))

### Added
- Add Text Formatter link to homepage and implement toast notification for copy action
- Add text_formatter app with initial configuration and views; update settings and URLs
- Add last update timestamp to gaps and blanks fetch functionality; update UI to display last update
- Add functionality to fetch gaps and blanks from checklist.txt; update URLs and templates accordingly

## 2025-01-26 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-26&until=2025-01-26))

### Added
- Add 'No' column to data tables and update fetch_data to include row numbers; modify jam_pelaksanaan and kelompok fields in migration
- Add shift field and update kelompok choices in QcRecord model; modify form and JavaScript for shift handling

## 2025-01-25 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-25&until=2025-01-25))

### Changed
- Enhance export functions to include national and international event
### Merged
- Merge branch 'main' of https://github.com/ftharyanto/ebast_new
### Reverted
- Revert "Add db.sqlite3 to .gitignore to prevent tracking of the database file"
### Added
- Add db.sqlite3 back

## 2025-01-24 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-24&until=2025-01-24))

### Changed
- Add db.sqlite3 to .gitignore to prevent tracking of the database file
### Fixed
- Fix slmon image accidentally removed after saving
### Removed
- Delete db.sqlite3

## 2025-01-20 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-20&until=2025-01-20))

### Changed
- Back to hide CS and QC input instead of making it readonly to fix the bug of None value when submitting the form

## 2025-01-19 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-19&until=2025-01-19))

### Added
- Add 'table-sm' class to fetched data tables in qcrecord_form.html for improved styling
### Changed
- Update CS and QC form templates to make ID fields readonly and adjust JavaScript for dynamic ID generation
- Move readme file

## 2025-01-17 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-17&until=2025-01-17))

### Added
- Add deployment instructions and configuration files for Nginx and Gunicorn
### Fixed
- Fix SLMon image handling in CsUpdateView and correct comments in export functions

## 2025-01-14 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-14&until=2025-01-14))

### Added
- Add functionality to clear SLMon image in CsUpdateView and update cs_form.html
- Add date field to QcRecord model and update qcrecord_form.html for date input handling
- Add date field to CsRecordModel and update cs_form.html for date input handling

## 2025-01-12 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-12&until=2025-01-12))

### Changed
- Update qcrecord_form.html for improved layout and functionality
- Update settings.py and requirements.txt; add ADMIN_MEDIA_PREFIX and specify whitenoise version
### Added
- Add whitenoise to requirements.txt

## 2025-01-10 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-10&until=2025-01-10))

### Added
- Add Docker support with Dockerfile and docker-compose.yml; update requirements.txt and add .dockerignore; add whitenoise to improve static serving

## 2025-01-09 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-09&until=2025-01-09))

### Added
- Add local_settings.py to .gitignore and move SECRET_KEY to settings.py
- Create django.yml
### Changed
- Update github action file
- Update requirements.txt to simplify package dependencies
- Move SECRET_KEY to local_settings.py for improved security and maintainability
### Fixed
- Fix file path casing in export functions and add .gitignore for project dependencies

## 2025-01-05 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-05&until=2025-01-05))

### Changed
- Refactor delete functionality in CsDeleteView; change to a post method for improved handling and update cs_list.html for better button styling and tooltip support
- Enhance form functionality in cs_form.html; add automatic jam pelaksanaan update based on selected shift and improve gap, spike, and blank handling in cs_export_excel function
- Refactor gap, spike, and blank handling in CsRecordModel; replace split method for improved readability and consistency Enhance HTML for image upload; update styling and text for better user experience Update STATIC_ROOT in settings; ensure proper static file handling in deployment

## 2025-01-04 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-04&until=2025-01-04))

### Changed
- Refactor media settings in Django; update MEDIA_URL and MEDIA_ROOT, and adjust URL patterns for static file serving in development

## 2025-01-03 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2025-01-03&until=2025-01-03))

### Changed
- Enhance UI for Ceklis Seiscomp and QC record lists; update button styles and add icons for better usability
### Fixed
- Fix date formatting in export functions for QC records; adjust index for correct date extraction

## 2024-12-29 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-29&until=2024-12-29))

### Added
- Add PDF export functionality to CsRecordModel; include image handling and date formatting
### Changed
- Enhance image handling in CsRecordModel and improve Excel export functionality; add date range formatting and handle missing image cases

## 2024-12-28 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-28&until=2024-12-28))

### Added
- Add image upload functionality to CsRecordModel; update forms and views for SLMon image handling
- Add Ceklis Seiscomp functionality with models, views, and templates; update admin and URLs
### Changed
- Refactor media settings and update image handling in CsRecordModel; add image export functionality to Excel
- Update qc_id field length in QcRecord model and modify qc_id generation format in form

## 2024-12-27 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-27&until=2024-12-27))

### Added
- Add kel_sebelum field to QcRecord model and update form and templates
### Fixed
- Fix cancel button on delete confirmation

## 2024-12-26 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-26&until=2024-12-26))

### Added
- Add cl_seiscomp app with initial models, views, and templates
- Add disabled qc_id field to QcRecordForm for improved data integrity
### Changed
- Refactor station list table for improved sorting and filtering functionality

## 2024-12-25 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-25&until=2024-12-25))

### Added
- Add pagination and filtering functionality to Operator and QC record tables
- Add sorting functionality to Operator list table
- Add filtering functionality to Operator list table
- Add Operator management views, forms, and templates; update URLs and navigation
- Add Operator link to navigation bar in base template
- Add conditional navigation bar for home namespace with Operator link
### Changed
- Enhance QC data fetching and update templates for improved user experience

## 2024-12-24 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-24&until=2024-12-24))

### Added
- Add Operator model and register in admin; update QcRecord references
- Initialize core app with models, views, and templates; update settings and URLs
### Changed
- Add Admin link to navigation bar and update Operator model import path

## 2024-12-23 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-23&until=2024-12-23))

### Added
- Add homepage view and template; update settings and URLs for new structure
- Add PDF export functionality and update templates with Font Awesome icons
### Changed
- Update date and time labels in QC record form to specify UTC
- Refactor navigation bar in base template for improved structure and responsiveness
- Implement delete confirmation modal and direct delete functionality for QC records
- Sort QC records in reverse order by qc_id in the template
- Update PDF export formatting and change content disposition to inline
### Removed
- Remove old URL configuration and add homepage template
- Remove temporary PDF files after export and clean up unused PDF templates

## 2024-12-21 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-21&until=2024-12-21))

### Changed
- Change the output file to qc_id
- Make the date, name and NIP to be dynamic based on the rows added
### Fixed
- Fix exporting all data in a database to excel file

## 2024-12-20 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-20&until=2024-12-20))

### Added
- Add export_to_excel function
### Changed
- Add stylings to the table
- Insert data to table
- Set the NIP's value to be filled automatically based on the Operator model

## 2024-12-18 ([Full Changelog](https://github.com/ftharyanto/ebast/commits/main?since=2024-12-18&until=2024-12-18))

### Fixed
- Fix forms not submitted correctly
