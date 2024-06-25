// Get the modal for "Ler mais"
var appModal = document.getElementById("appModal");

// Get the read more buttons
var readmoreButtons = document.getElementsByClassName("readmore");

// Get the close button inside the modal
var closeButton = document.querySelector("#appModal .close");

// Iterate over read more buttons and add click event listeners
for (var i = 0; i < readmoreButtons.length; i++) {
    readmoreButtons[i].addEventListener("click", function(event) {
        var parentRectangle = event.target.closest(".rectangle");
        var modalTitle = parentRectangle.querySelector("h2").innerText;
        var shortDescription = parentRectangle.querySelector(".short-description").innerText;
        var fullDescription = parentRectangle.querySelector(".full-description").innerText;
        
        document.getElementById("modalTitle").innerText = modalTitle;
        document.getElementById("modalDescription").innerText = fullDescription;

        // Display the modal
        appModal.style.display = "block";
    });
}

// When the user clicks on the close button (x), close the modal
closeButton.onclick = function() {
    appModal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == appModal) {
        appModal.style.display = "none";
    }
}

// Modal for "Abrir endereço" functionality (already implemented)
var openPathModal = document.getElementById("openPathModal");
var openPathButtons = document.getElementsByClassName("open-path");
var compreendiButton = document.querySelector("#openPathModal .compreendi");
var closeButton = document.querySelector("#openPathModal .close-modal");

for (var i = 0; i < openPathButtons.length; i++) {
    openPathButtons[i].addEventListener("click", function(event) {
        openPathModal.style.display = "block";
    });
}

closeButton.onclick = function() {
    openPathModal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == openPathModal) {
        openPathModal.style.display = "none";
    }
}

// Handle "Compreendi" button click (for redirection, replace "#" with your desired URL)
compreendiButton.onclick = function() {
    window.location.href = "#"; // Replace "#" with your desired URL
}
