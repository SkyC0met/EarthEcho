$(document).ready(function () {
  var owl = $(".owl-carousel");
  owl.owlCarousel({
    loop: true,
    margin: 10,
    nav: false, // Disable default nav
    dots: false, // Disable pagination dots
    responsive: {
      0: {
        items: 2,
      },
      576: {
        items: 3,
      },
      768: {
        items: 4,
      },
      992: {
        items: 5,
      },
    },
  });

  // Custom Navigation Events
  $(".left-btn").click(function () {
    owl.trigger("prev.owl.carousel");
  });

  $(".right-btn").click(function () {
    owl.trigger("next.owl.carousel");
  });
});
