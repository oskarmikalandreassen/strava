const button1 = document.getElementById('button1');
const button2 = document.getElementById('button2');
const plotImage = document.getElementById('plotImage');
const startDateInput = document.getElementById('startDate');
const endDateInput = document.getElementById('endDate');
const submitDatesButton = document.getElementById('submitDates');

let globalStartDate = '';
let globalEndDate = '';

document.addEventListener("DOMContentLoaded", function () {
    function updateDefaultPlotImage(base64String) {
        const plotImage = document.getElementById('plotImage');
        plotImage.src = `data:image/png;base64, ${base64String}`;
    }

    fetch('/kms')  
        .then(response => response.json())
        .then(data => {
            const plotData = data.plot;
            updateDefaultPlotImage(plotData);
        })
        .catch(error => console.error('Error:', error));
});

submitDatesButton.addEventListener('click', () => {
    submitDatesButton.classList.add('shadow-effect');
    setTimeout(() => {
        submitDatesButton.classList.remove('shadow-effect');
    }, 100);

    globalStartDate = startDateInput.value;
    globalEndDate = endDateInput.value;
    fetchData('/data');
});

function fetchData(url) {
    fetch(`${url}?startDate=${globalStartDate}&endDate=${globalEndDate}`)
        .then(response => response.json())
        .then(data => {
            plotImage.src = `data:image/png;base64, ${data.plot}`;
        })
        .catch(error => console.error('Error:', error));
}

kilometerButton.addEventListener('click', () => {
    kilometerButton.classList.add('shadow-effect');
    setTimeout(() => {
        kilometerButton.classList.remove('shadow-effect');
    }, 100);
    fetchData('/kms');
});

timeButton.addEventListener('click', () => {
    timeButton.classList.add('shadow-effect');
    setTimeout(() => {
        timeButton.classList.remove('shadow-effect');
    }, 100);
    fetchData('/time');
});
