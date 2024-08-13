function toggleDropdown() {
    document.getElementById("myDropdown").classList.toggle("show");
    document.getElementById("myInput").focus();
}

function filterFunction() {
    var input, filter, div, a, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    div = document.getElementById("myDropdown");
    a = div.getElementsByTagName("a");
    for (i = 0; i < a.length; i++) {
        if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
        } else {
            a[i].style.display = "none";
        }
    }
}

document.querySelectorAll('#myDropdown a').forEach(function(item) {
    item.addEventListener('click', function(event) {
        event.preventDefault();
        var value = this.getAttribute('data-value');
        document.getElementById('Location').value = value;  // Update the visible Location input
        document.getElementById('selected_location_display').innerText = 'Selected Location: ' + value;  // Display the selected location
        document.getElementById('myDropdown').classList.remove('show');  // Hide the dropdown
    });
});

function toggleMap() {
    var mapContainer = document.getElementById("mapContainer");
    var viewMapBtn = document.getElementById("viewMapBtn");

    if (mapContainer.style.display === "none") {
        mapContainer.style.display = "block";
        viewMapBtn.style.display = "none";
    } else {
        mapContainer.style.display = "none";
        viewMapBtn.style.display = "inline-block";
    }
}

// document.addEventListener('DOMContentLoaded', function() {
//     // Attach click event listener to all contact buttons
//     document.querySelectorAll('a[data-toggle="modal"]').forEach(function(button) {
//         button.addEventListener('click', function() {
//             // Get data attributes from the clicked button
//             var name = this.getAttribute('data-name');
//             var email = this.getAttribute('data-email');
//             var phone = this.getAttribute('data-phone');

//             // Populate the modal with the fetched data
//             document.getElementById('modalName').textContent = name;
//             document.getElementById('modalEmail').textContent = email;
//             document.getElementById('modalPhone').textContent = phone;
//         });
//     });
// });
