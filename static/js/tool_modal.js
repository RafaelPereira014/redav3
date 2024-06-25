// Get the modal
var modal = document.getElementById("toolModal");

// Get the button that opens the modal
var readmoreButtons = document.getElementsByClassName("readmore");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

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
        modal.style.display = "block";
    });
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
    modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
