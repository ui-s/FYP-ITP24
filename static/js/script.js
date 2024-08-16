document.addEventListener('DOMContentLoaded', function() {
    const ageGroups = document.querySelectorAll('.age-group');
    const genderGroups = document.querySelectorAll('.gender-group');
    const submitButton = document.getElementById('submit-selection');

    let selectedAge = null;
    let selectedGender = null;

    function selectItem(items, selectedItem) {
        items.forEach(item => item.classList.remove('selected'));
        selectedItem.classList.add('selected');
    }

    ageGroups.forEach(group => {
        group.addEventListener('click', function() {
            selectItem(ageGroups, this);
            selectedAge = this.dataset.age;
        });
    });

    genderGroups.forEach(group => {
        group.addEventListener('click', function() {
            selectItem(genderGroups, this);
            selectedGender = this.dataset.gender;
        });
    });

    submitButton.addEventListener('click', function() {
        if (selectedAge && selectedGender) {
            const form = document.createElement('form');
            form.method = 'post';
            form.action = '/';

            const ageInput = document.createElement('input');
            ageInput.type = 'hidden';
            ageInput.name = 'age_group';
            ageInput.value = selectedAge;
            form.appendChild(ageInput);

            const genderInput = document.createElement('input');
            genderInput.type = 'hidden';
            genderInput.name = 'gender';
            genderInput.value = selectedGender;
            form.appendChild(genderInput);

            document.body.appendChild(form);
            form.submit();
        } else {
            alert('Please select both an age group and a gender.');
        }
    });
});