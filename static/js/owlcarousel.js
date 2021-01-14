$('.owl-carousel').owlCarousel({
            loop:true,
            margin:20,
            nav: true,
            lazyLoad: true,
            dots: false,
            autoplay:true,
            autoplayTimeout:2000,
            autoplayHoverPause:true,
            responsive:{
                0:{
                    items:1,
                    
                    
                },
                600:{
                    items:2,
                },
                1000:{
                    items:3, 
                },
                1200:{
                    items:4,
                }
            }
        });