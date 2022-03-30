import './Songs.css'
import { useState,useRef,useEffect } from 'react'
import Header  from "../header/Header"

function Songs(){

    return(
        <div className="Songs">
            <Header/>
            <div className="page">
                <div className="instructions"><h1>Choose a song you'd like to learn</h1></div>
                <div className="songs_container">
                    <div className="song_container">
                        <h4>Hatikva</h4>
                    </div>
                    <div className="song_container">
                        <h4>Yonatan Hakatan</h4>
                    </div>
                    <div className="song_container">
                        <h4>No woman no cry</h4>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Songs