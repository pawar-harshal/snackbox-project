  let lastScrollY = window.scrollY;

  window.addEventListener("scroll", () => {
    const navbar = document.querySelector(".navbar");

    if (window.scrollY > lastScrollY) {
      // Scrolling down – hide navbar
      navbar.classList.add("hidden");
    } else {
      // Scrolling up – show navbar
      navbar.classList.remove("hidden");
    }

    lastScrollY = window.scrollY;
  });