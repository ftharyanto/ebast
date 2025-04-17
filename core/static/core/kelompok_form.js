// JavaScript for the kelompok form page
const oprInput = document.getElementById('oprInput');
const suggestionsBox = document.getElementById('suggestions');
const oprTableBody = document.getElementById('oprTableBody');
let oprCount = 0;
let operators = [];

async function fetchOperators() {
    try {
        const response = await fetch('/core/api/get_operator_list/');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        operators = data.operators;
        return operators;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

window.addEventListener('load', () => {
    fetchOperators().then((operators) => {
        const memberIds = document.getElementById('{{ form.member.id_for_label }}').value.split(',');
        memberIds.forEach(memberId => {
            const operator = operators.find(opr => opr.pk == memberId);
            if (operator) {
                addOprToTable(operator.name);
            }
        });
    });
});

oprInput.addEventListener('input', () => {
    const query = oprInput.value.toLowerCase();
    suggestionsBox.innerHTML = '';
    if (query) {
        const matchedOpr = operators.filter(operator => operator.name.toLowerCase().includes(query));
        if (matchedOpr.length) {
            matchedOpr.forEach(operator => {
                const item = document.createElement('div');
                item.className = 'suggestion-item';
                item.textContent = operator.name;
                item.addEventListener('click', () => {
                    addOprToTable(operator.name);
                    oprInput.value = '';
                    suggestionsBox.classList.add('d-none');
                });
                suggestionsBox.appendChild(item);
            });
            suggestionsBox.classList.remove('d-none');
        } else {
            suggestionsBox.classList.add('d-none');
        }
    } else {
        suggestionsBox.classList.add('d-none');
    }
});

oprInput.addEventListener('blur', () => {
    setTimeout(() => suggestionsBox.classList.add('d-none'), 200);
});

function addOprToTable(operator) {
    oprCount++;
    const operatorData = operators.find(opr => opr.name === operator);

    const row = document.createElement('tr');
    row.setAttribute('draggable', 'true');
    row.innerHTML = `
    <td class="drag-handle">☰</td>
    <td>${oprCount}</td>
    <td>${operatorData.pk}</td>
    <td>${operatorData.name}</td>
    <td>
      <button class="btn btn-danger btn-sm delete"><i class="fas fa-trash"></i></button>
    </td>
  `;

    row.querySelector('.delete').addEventListener('click', () => {
        row.remove();
        updateRowNumbers();
        updateMemberInput();
    });

    oprTableBody.appendChild(row);
    updateMemberInput();
}

function updateRowNumbers() {
    const rows = oprTableBody.querySelectorAll('tr');
    oprCount = 0;
    rows.forEach((row) => {
        oprCount++;
        row.children[1].textContent = oprCount;
    });
}

function updateMemberInput() {
    const rows = oprTableBody.querySelectorAll('tr');
    const ids = Array.from(rows).map(row => row.children[2].textContent);
    document.getElementById('{{ form.member.id_for_label }}').value = ids.join(',');
}

oprTableBody.addEventListener('dragstart', (event) => {
    if (event.target.tagName === 'TR') {
        event.target.classList.add('dragging');
    }
});

oprTableBody.addEventListener('dragend', (event) => {
    if (event.target.tagName === 'TR') {
        event.target.classList.remove('dragging');
    }
});

oprTableBody.addEventListener('dragover', (event) => {
    event.preventDefault();
    const draggingRow = oprTableBody.querySelector('.dragging');
    const afterElement = getDragAfterElement(oprTableBody, event.clientY);

    oprTableBody.querySelectorAll('tr').forEach(row => row.classList.remove('drag-over'));

    if (afterElement == null) {
        oprTableBody.appendChild(draggingRow);
    } else {
        oprTableBody.insertBefore(draggingRow, afterElement);
        afterElement.classList.add('drag-over');
    }
});

oprTableBody.addEventListener('dragleave', () => {
    oprTableBody.querySelectorAll('tr').forEach(row => row.classList.remove('drag-over'));
});

oprTableBody.addEventListener('drop', () => {
    oprTableBody.querySelectorAll('tr').forEach(row => row.classList.remove('drag-over'));
    updateRowNumbers();
    updateMemberInput();
});

function getDragAfterElement(container, y) {
    const draggableElements = [...container.querySelectorAll('tr:not(.dragging)')];

    return draggableElements.reduce((closest, child) => {
        const box = child.getBoundingClientRect();
        const offset = y - box.top - box.height / 2;
        if (offset < 0 && offset > closest.offset) {
            return { offset: offset, element: child };
        } else {
            return closest;
        }
    }, { offset: Number.NEGATIVE_INFINITY }).element;
}