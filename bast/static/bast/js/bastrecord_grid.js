// Grid API: Access to Grid API methods
let gridApi;

// Function to perform global search
function onFilterTextBoxChanged() {
    const searchValue = document.getElementById('globalSearch').value.toLowerCase();
    
    gridApi.setGridOption('quickFilterText', searchValue);
}

// Function to clear the search
function clearSearch() {
    document.getElementById('globalSearch').value = '';
    gridApi.setGridOption('quickFilterText', '');
}

// Function to get selected rows
function getSelectedRows() {
    const selectedNodes = gridApi.getSelectedNodes();
    return selectedNodes.map(node => node.data);
}

// Function to log selected rows
function logSelectedRows() {
    const selectedRows = getSelectedRows();
    console.log('Selected Rows:', selectedRows);
    return selectedRows;
}

// Grid Options: Contains all of the grid configurations
const gridOptions = {
    theme: 'quartz',
    themeParams: {
        browserColorScheme: 'light',
        headerFontSize: 14
    },
    // Enable horizontal scrolling
    suppressHorizontalScroll: false,
    // Set a minimum width for columns to prevent them from becoming too narrow
    defaultColDef: {
        flex: 1,
        minWidth: 150,  // Minimum column width
        filter: true,
        sortable: true,
        resizable: true,
    },
    // Data to be displayed
    rowData: [], // Will be loaded via AJAX
    // Columns to be displayed (Should match BastRecordModel fields)
    columnDefs: [
        {
            headerName: '',
            field: 'selected',
            width: 50,
            resizable: false,
            filter: false,  // Disable filtering for the selection column
            suppressSizeToFit: true,
            checkboxSelection: true,
            headerCheckboxSelection: true,
            headerCheckboxSelectionFilteredOnly: true,
            pinned: 'center'
        },
        { 
            field: "id", 
            headerName: "ID", 
            filter: "agNumberColumnFilter",
            width: 80,  // Fixed width
            flex: 0,    // Prevent column from growing
            resizable: true  // Allow manual resizing if needed
        },
        { field: "bast_id", headerName: "BAST ID", filter: "agTextColumnFilter" },
        { field: "date", headerName: "Tanggal", filter: "agDateColumnFilter" },
        { field: "shift", headerName: "Shift", filter: "agTextColumnFilter" },
        { field: "kelompok", headerName: "Kelompok", filter: "agTextColumnFilter" },
        { field: "kel_berikut", headerName: "Kel. Berikut", filter: "agTextColumnFilter" },
        { field: "events", headerName: "Events", filter: "agTextColumnFilter" },
        { field: "count_gaps", headerName: "Gaps", filter: "agNumberColumnFilter" },
        { field: "count_spikes", headerName: "Spikes", filter: "agNumberColumnFilter" },
        { field: "count_blanks", headerName: "Blanks", filter: "agNumberColumnFilter" },
        { field: "waktu_cs", headerName: "Waktu CS", filter: "agTextColumnFilter" },
        { field: "pulsa_poco", headerName: "Pulsa POCO", filter: "agNumberColumnFilter" },
        { field: "poco_exp", headerName: "POCO Exp", filter: "agDateColumnFilter" },
        { field: "samsung_exp", headerName: "Samsung Exp", filter: "agDateColumnFilter" },
        { 
            field: "spv_name",  
            headerName: "SPV", 
            filter: "agTextColumnFilter",
            sortable: true,
            valueGetter: params => params.data.spv_name || ''
        },
        { field: "notes", headerName: "Notes", filter: "agTextColumnFilter" }
    ],

    rowSelection: 'multiple',
    suppressRowClickSelection: true,
    onRowSelected: (event) => {
        // This will be called whenever row selection changes
        // logSelectedRows();
    },
    enableCellTextSelection: true,
    enableCellChangeFlash: true,
};

// Create Grid
document.addEventListener('DOMContentLoaded', () => {
    const gridDiv = document.querySelector("#myGrid");
    // Ensure the grid container has proper layout for scrolling
    gridDiv.style.width = '100%';
    gridDiv.style.height = '100%';
    gridDiv.style.display = 'flex';
    gridDiv.style.flexDirection = 'column';
    
    gridApi = agGrid.createGrid(gridDiv, gridOptions);

    // Fetch BAST records from Django API and set as rowData
    fetch('/bast/api/bastrecord_list/')
        .then(response => response.json())
        .then(data => {
            gridApi.setGridOption('rowData', data);
        })
        .catch(error => {
            console.error('Failed to load BAST records:', error);
        });

    // Add event listeners for search
    document.getElementById('globalSearch').addEventListener('input', onFilterTextBoxChanged);
    document.getElementById('clearSearch').addEventListener('click', clearSearch);

    // Add event listener for CSV export
    document.getElementById('exportCsvBtn').addEventListener('click', () => {
        try {
            console.log('Starting CSV export...');
            
            // Get all column fields
            const columnFields = gridApi.getColumnDefs()
                .map(col => col.field)
                .filter(Boolean);
                
            console.log('Column fields:', columnFields);
            
            // Basic export with minimal options
            const params = {
                fileName: `bast_records_${new Date().toISOString().slice(0, 10)}.csv`,
                skipColumnHeaders: false,
                skipColumnGroupHeaders: true,
                onlySelected: false,
                allColumns: false
            };
            
            console.log('Exporting with params:', params);
            
            // Export the data
            gridApi.exportDataAsCsv(params);
            console.log('CSV export initiated');
        } catch (error) {
            console.error('Error during CSV export:', error);
            alert('Failed to export CSV. Please check console for details.');
        }
    });

    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Focus search with Ctrl+F or Cmd+F
        if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
            e.preventDefault();
            const searchInput = document.getElementById('globalSearch');
            searchInput.focus();
            searchInput.select();
        }
        // Clear search with Escape
        else if (e.key === 'Escape') {
            const searchInput = document.getElementById('globalSearch');
            if (document.activeElement === searchInput && searchInput.value) {
                e.preventDefault();
                clearSearch();
            }
        }
    });
});