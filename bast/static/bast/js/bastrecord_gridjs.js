// Sample data - replace this with your actual data from the server
const sampleData = [
    { make: "Tesla", model: "Model Y", price: 64950, electric: true },
    { make: "Ford", model: "F-Series", price: 33850, electric: false },
    { make: "Toyota", model: "Corolla", price: 29600, electric: false },
    { make: "Mercedes", model: "EQA", price: 48890, electric: true },
    { make: "Fiat", model: "500", price: 15774, electric: false },
    { make: "Nissan", model: "Juke", price: 20675, electric: false }
];

// Initialize the grid
let grid;

// Function to initialize the grid
function initGrid() {
    grid = new gridjs.Grid({
        columns: [
            {
                id: 'selected',
                name: gridjs.html('<input type="checkbox" id="selectAll" class="form-check-input">'),
                width: '50px',
                formatter: (_, row) => 
                    gridjs.html(`<input type="checkbox" class="row-checkbox form-check-input" data-id="${row.cells[1].data}">`),
                sort: false
            },
            { 
                id: 'make',
                name: 'Make',
                sort: true,
                formatter: (cell) => gridjs.html(`<span class="text-primary fw-medium">${cell}</span>`)
            },
            { 
                id: 'model',
                name: 'Model',
                sort: true 
            },
            { 
                id: 'price',
                name: 'Price',
                sort: true,
                formatter: (cell) => `$${cell.toLocaleString()}`
            },
            { 
                id: 'electric',
                name: 'Electric',
                sort: true,
                formatter: (cell) => cell ? 'Yes' : 'No'
            },
        ],
        data: sampleData,
        search: true,
        pagination: {
            limit: 10,
            summary: true
        },
        sort: true,
        language: {
            search: {
                placeholder: 'Search in all columns...'
            },
            pagination: {
                previous: '<',
                next: '>',
                showing: 'Showing',
                results: () => 'Records'
            }
        },
        style: {
            table: {
                'white-space': 'nowrap'
            },
            th: {
                'background-color': 'rgba(0, 0, 0, 0.1)',
                'padding': '0.75rem 1rem',
                'text-align': 'left'
            },
            td: {
                'padding': '0.5rem 1rem',
                'vertical-align': 'middle'
            },
            '.gridjs-tbody': {
                'font-size': '0.9em'
            }
        }
    }).render(document.getElementById('gridjs-wrapper'));

    // Add event listeners
    setupEventListeners();
}

// Function to set up event listeners
function setupEventListeners() {
    // Select all checkbox
    document.addEventListener('click', (e) => {
        if (e.target && e.target.id === 'selectAll') {
            const checkboxes = document.querySelectorAll('.row-checkbox');
            checkboxes.forEach(checkbox => {
                checkbox.checked = e.target.checked;
            });
            updateSelectedCount();
        }
    });

    // Individual row checkbox
    document.addEventListener('change', (e) => {
        if (e.target && e.target.classList.contains('row-checkbox')) {
            updateSelectedCount();
        }
    });

    // Get selected rows button
    document.getElementById('getSelectedBtn').addEventListener('click', () => {
        const selectedRows = getSelectedRows();
        console.log('Selected Rows:', selectedRows);
        if (selectedRows.length === 0) {
            alert('No rows selected');
        } else {
            // You can process the selected rows here
            alert(`Selected ${selectedRows.length} row(s)`);
        }
    });

    // Clear selection button
    document.getElementById('clearSelectionBtn').addEventListener('click', () => {
        const checkboxes = document.querySelectorAll('.row-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.checked = false;
        });
        document.getElementById('selectAll').checked = false;
        updateSelectedCount();
    });

    // Global search
    const globalSearch = document.getElementById('globalSearch');
    let searchTimeout;
    
    globalSearch.addEventListener('input', () => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            grid.search(globalSearch.value);
        }, 300);
    });

    // Clear search button
    document.getElementById('clearSearch').addEventListener('click', () => {
        globalSearch.value = '';
        grid.search('');
    });
}

// Function to get selected rows
function getSelectedRows() {
    const selectedRows = [];
    const checkboxes = document.querySelectorAll('.row-checkbox:checked');
    
    checkboxes.forEach(checkbox => {
        const row = checkbox.closest('tr');
        if (row) {
            const rowData = {};
            const cells = row.querySelectorAll('td');
            
            // Skip the first cell (checkbox) and last cell (actions)
            for (let i = 1; i < cells.length - 1; i++) {
                const columnId = grid.config.columns[i].id;
                rowData[columnId] = cells[i].textContent.trim();
            }
            
            selectedRows.push(rowData);
        }
    });
    
    return selectedRows;
}

// Function to update the selected count
function updateSelectedCount() {
    const selectedCount = document.querySelectorAll('.row-checkbox:checked').length;
    const totalCount = document.querySelectorAll('.row-checkbox').length;
    const selectAllCheckbox = document.getElementById('selectAll');
    
    if (selectAllCheckbox) {
        selectAllCheckbox.checked = selectedCount === totalCount && totalCount > 0;
        selectAllCheckbox.indeterminate = selectedCount > 0 && selectedCount < totalCount;
    }
}

// Initialize the grid when the DOM is fully loaded
document.addEventListener('DOMContentLoaded', initGrid);
