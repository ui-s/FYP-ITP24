function selectGoal(goalId) {
    // Remove 'selected' class from all goal boxes
    document.querySelectorAll('.goal-box').forEach(box => {
        box.classList.remove('selected');
    });
    
    // Add 'selected' class to the clicked goal box
    document.getElementById(goalId).parentElement.classList.add('selected');
    
    // Check the radio button
    document.getElementById(goalId).checked = true;
}