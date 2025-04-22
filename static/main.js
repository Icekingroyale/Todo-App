document.addEventListener('DOMContentLoaded', () => {
    // Task filtering (Search by task content)
    const taskSearch = document.getElementById('taskSearch');
    taskSearch.addEventListener('input', function () {
        let filter = taskSearch.value.toLowerCase();
        const taskRows = document.querySelectorAll('table tr');  // Select all task rows
        taskRows.forEach(row => {
            const taskContent = row.querySelector('td')?.textContent.toLowerCase();
            if (taskContent && taskContent.includes(filter)) {
                row.style.display = '';  // Show matching tasks
            } else {
                row.style.display = 'none';  // Hide non-matching tasks
            }
        });
    });
});
