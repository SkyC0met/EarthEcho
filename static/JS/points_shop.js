//SKY JS
$(document).ready(function () {
  var foodCarousel = $(".food-carousel");
  var fashionCarousel = $(".fashion-carousel");
  foodCarousel.owlCarousel({
    loop: true,
    margin: 10,
    nav: false, // Disable default nav
    dots: false, // Disable pagination dots
    responsive: {
      0: {
        items: 1,
      },
      320: {
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

  fashionCarousel.owlCarousel({
    loop: true,
    margin: 10,
    nav: false, // Disable default nav
    dots: false, // Disable pagination dots
    responsive: {
      0: {
        items: 1,
      },
      320: {
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
  $(".left-btn-food").click(function(){
    foodCarousel.trigger('prev.owl.carousel');
  });

  $(".right-btn-food").click(function(){
    foodCarousel.trigger('next.owl.carousel');
  });

  $(".left-btn-fashion").click(function(){
    fashionCarousel.trigger('prev.owl.carousel');
  });

  $(".right-btn-fashion").click(function(){
    fashionCarousel.trigger('next.owl.carousel');
  });
});
