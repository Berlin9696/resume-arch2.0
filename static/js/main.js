var slideIndex = 0;
showSlides();

function showSlides() {
    var slides = document.getElementsByClassName("mySlides");
    // Hide all slides
    for (var i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slideIndex++;
    // Reset slideIndex if it exceeds number of slides
    if (slideIndex > slides.length) {
        slideIndex = 1;
    }
    // Display the current slide and add a fade effect (if desired)
    slides[slideIndex - 1].style.display = "block";
    // Repeat every 3 seconds (3000 milliseconds)
    setTimeout(showSlides, 3000);
}

  
  function toggleMenu() {
    const menu = document.querySelector(".nav-menu");
    menu.classList.toggle("open");
  }