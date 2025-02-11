//Script for uploading resume
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
      const formData = new FormData();
      formData.append("file", file);
  
      fetch("/upload", {
        method: "POST",
        body: formData,
      })
        .then(response => response.json())
        .then(data => {
          alert(`File uploaded successfully: ${data.fileName}`);
        })
        .catch(error => {
          console.error("Error uploading file:", error);
          alert("Failed to upload file.");
        });
    }
  }
  ///////////////////////////////////////////
  
  //Script for slideshow
  let slideIndex = 1;
  showSlides(slideIndex);
  
  function plusSlides(n) {
    showSlides(slideIndex += n);
  }
  
  function currentSlide(n) {
    showSlides(slideIndex = n);
  }
  
  function showSlides(n) {
    let i;
    let slides = document.getElementsByClassName("mySlides");
    let dots = document.getElementsByClassName("dot");
    if (n > slides.length) {slideIndex = 1}    
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";  
    }
    for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";  
    dots[slideIndex-1].className += " active";
  }
  ///////////////////////////////////////////
  
  function toggleMenu() {
    const menu = document.querySelector(".nav-menu");
    menu.classList.toggle("open");
  }