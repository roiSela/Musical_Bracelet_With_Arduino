$(document).ready(function() {

    let doc = document.documentElement;
    let w = window;

    let prevScroll = w.scrollY || doc.scrollTop;
    let curScroll;
    let direction = 0;
    let prevDirection = 0;

    let header = $("#header");

    let headerTop = header.position().top;
    let headerBottom = headerTop + header.outerHeight();


    let checkScroll = function() {

        /*
        ** Find the direction of scroll
        ** 0 - initial, 1 - up, 2 - down
        */

        curScroll = w.scrollY || doc.scrollTop;
        if (curScroll > prevScroll) {
            //scrolled up
            direction = 2;
        }
        else if (curScroll < prevScroll) {
            //scrolled down
            direction = 1;
        }

        if (direction !== prevDirection) {
            toggleHeader(direction, curScroll);
        }

        prevScroll = curScroll;



            let section = $(".second")
            let sectionTop = section.position().top - $(window).scrollTop();
            let sectionBottom = section.position().top - $(window).scrollTop() + section.height();
            console.log("sectionTop: "+sectionTop+",sectionBottom:  "+sectionBottom+", headerTop: "+ headerTop+ ", headerBottom: "+headerBottom);
            if (sectionTop <=50W) {
                header.css("background-color", "#1D1B26");
            } else {
                header.css("background-color", "#6A5495");
            }


    };

    var toggleHeader = function(direction, curScroll) {
        if (direction === 2 && curScroll > 52) {

            //replace 52 with the height of your header in px

            header.addClass('hide');
            prevDirection = direction;
        }
        else if (direction === 1) {
            header.removeClass('hide');
            prevDirection = direction;
        }
    };






    window.addEventListener('scroll', checkScroll);



});

