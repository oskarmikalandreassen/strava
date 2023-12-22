const button1 = document.getElementById('button1');
const button2 = document.getElementById('button2');
const plotImage = document.getElementById('plotImage');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const submitDatesButton = document.getElementById('submitDates');

let globalStartDate = '';
let globalEndDate = '';

submitDatesButton.addEventListener('click', () => {
    globalStartDate = startDateInput.value;
    globalEndDate = endDateInput.value;    
});

function fetchData(url) {
    fetch(`${url}?startDate=${globalStartDate}&endDate=${globalEndDate}`)
        .then(response => response.json())
        .then(data => {
            plotImage.src = `data:image/png;base64, ${data.plot}`;
        })
        .catch(error => console.error('Error:', error));
}

button1.addEventListener('click', () => {
    fetchData('/kms');
});

button2.addEventListener('click', () => {
    fetchData('/time');
});
