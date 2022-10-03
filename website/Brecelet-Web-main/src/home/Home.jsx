import { useState,useRef,useEffect } from 'react'
import Header  from "../header/Header"
import NOTE_PIC  from "../pics/note.jpg"
import PLAY_FLAT  from "../pics/play-flat.png"
import {Link} from "react-router-dom";
import ROI from "../pics/roi.jpeg"
import STAV from "../pics/stav.jpg"
import ARDUINO from "../pics/arduino.jpeg"


function Home() {

    const [headerState,setHeader] = useState({hide:false,color: false})

    const secondRef = useRef(null);
    const prevScroll = useRef(window.scrollY || document.scrollTop)

    let curScroll = window.scrollY || document.scrollTop


    useEffect(() =>{
        prevScroll.current = curScroll
        window.addEventListener('scroll', checkScroll);


        return () => window.removeEventListener('scroll', checkScroll)
    }, [headerState])


    const checkScroll = function() {

        let changes = false;
        let down;
        let hide = headerState.hide;
        let color = headerState.color;

        curScroll = window.scrollY || document.scrollTop

        if (curScroll > prevScroll.current) {
            //scrolled down
            down = true;
        } else if (curScroll < prevScroll.current) {
            //scrolled up
            down = false;
        }

        prevScroll.current = curScroll

        if (down !== headerState.headerHide) {
            changes = true;
            hide = down;

        }

        const section = secondRef.current.getBoundingClientRect()
        if (section.top <= 50)
        {
            if( !headerState.color) {
                changes = true;
                color = true;
            }
        }
        else
        {
            if(headerState.color) {
                changes = true
                color = false
            }
        }

        if(changes){
            setHeader({hide,color})
        }
    };

    const {color,hide} = headerState

    return (
        <div className="Home">
            <Header headerColor={color} headerHide={hide}/>
            <div className="home_page">
                <div className="part first">
                    <div className="first_text">
                        <div className="first_title_container">
                            <h1 className="first_title">Hello everyone, Welcome to our site!</h1>
                        </div>
                        <h3>
                            Who we are?
                            A pair of students in the "Computer Science" department of the Tel Aviv-Yafo Academy.
                        </h3>
                    </div>
                    <div className="first_img_container">
                        <div className="man_container">
                             <img  src={STAV} alt="a pic of two lovely students" />
                        </div>
                        <div className="man_container">
                            <img src ={ROI}/>
                        </div>
                    </div>
                </div>

                <div className="part second" ref={secondRef}>
                    <div className="second_title_container">
                        <h1 className="second_title">the musical bracelet</h1>
                    </div>
                    <div className="second_info">
                        <div className="second_info_text">
                            <h2>
                                The musical bracelet is an Arduino-based device designed to make the world of musical creation accessible to those who could not before.
                                With the help of hand gestures the user can produce sounds, record them if he wishes, and upload them to the site.
                            </h2>
                        </div>
                        <div className="second_info_img_container">
                            <img src={ARDUINO} alt="a pic of a nice machinery / users using the bracelet" width="500" height="600"/>
                        </div>
                    </div>
                </div>

                <div className="part third">
                    <div className="third_info">
                        <div className="third_up">
                            building the musical bracelet was not enough,
                            as we see it, the power in music is that you can share it and make new connections and experiences
                            and above all use it to express yourself and let people to get to know you trough your music.
                            to accomplish this vision we've built this website, where you can
                            share your experiences with the bracelet with other people
                        </div>
                        <div className="third_middle">
                            <div className="circles">
                                <Link to="/posts" className="circle_container">

                                        <div className="circle">
                                            <img src={PLAY_FLAT} alt="a pic of posts" />
                                        </div>
                                    <h5> Post, Share, and hear others creations</h5>
                                </Link>
                                <Link to="/songs" className="circle_container">

                                        <div className="circle">
                                            <img src={NOTE_PIC} alt="a pic of songs" />
                                        </div>

                                    <h5> Learn to play some cool music with the music bracelet</h5>
                                </Link>
                            </div>
                        </div>
                        <div className="third_down">
                            Thanks for reading, enjoy.
                        </div>
                    </div>
                </div>

            </div>
        </div>
    )
}

export default Home
