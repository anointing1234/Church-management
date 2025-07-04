// static/admin/js/juniorchurch_toggle.js

document.addEventListener('DOMContentLoaded', function () {
    const churchTypeSelect = document.querySelector('#id_church_type');
    const childrenFields = document.querySelectorAll('.children-field');
    const teensFields = document.querySelectorAll('.teens-field');

    function toggleFields() {
        const selected = churchTypeSelect.value;
        childrenFields.forEach(field => {
            const row = field.closest('.form-row') || field.closest('div');
            row.style.display = (selected === 'children') ? '' : 'none';
        });
        teensFields.forEach(field => {
            const row = field.closest('.form-row') || field.closest('div');
            row.style.display = (selected === 'teens') ? '' : 'none';
        });
    }

    if (churchTypeSelect) {
        churchTypeSelect.addEventListener('change', toggleFields);
        toggleFields(); // Initial state
    }
});
