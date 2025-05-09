# Django Management Command: find_duplicates_all

This command finds and optionally deletes duplicate records in all user-defined models of your Django project, using the first user-input field (e.g., qc_id, qcfm_id, cs_id, bast_id, name, etc.).

## Features
- Scans all models in all apps (except Django built-in apps and StationListModel in cl_seiscomp).
- Uses the first user-input field (CharField, IntegerField, or TextField, skipping PK and date/time fields) for duplicate detection.
- Interactive prompt to delete duplicates (keeps one record, deletes the rest).
- Prints deleted primary keys for transparency.

## Usage

```bash
python manage.py find_duplicates_all
```

- The command will print duplicate values and their primary keys for each model.
- For each set of duplicates, you will be prompted:
  
  `Delete duplicates for [app_label.ModelName] field 'field'? (y/N):`

  - Type `y` and press Enter to delete all but one of each duplicate value.
  - Type `n` or just press Enter to skip deletion.

## What is considered a duplicate?
- Two or more records with the same value in the selected field (e.g., two records with the same `qc_id`).
- The script always keeps the record with the lowest primary key (pk) and deletes the rest.

## Exclusions
- Does **not** check models in Django built-in apps: `admin`, `auth`, `contenttypes`, `sessions`.
- Does **not** check `StationListModel` in the `cl_seiscomp` app.

## Safety
- The script is interactive by default. No records are deleted unless you confirm.
- Always review the output before confirming deletion.

## Customization
- To change which models/fields are checked, edit the logic in `find_duplicates_all.py`.
- For non-interactive or dry-run modes, further customization is possible.

---

**Author:** Your Team
**Location:** `qc/management/commands/find_duplicates_all.py` 