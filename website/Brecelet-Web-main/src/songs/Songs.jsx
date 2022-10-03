import './Songs.css'
import { useState,useRef,useEffect } from 'react'
import Header  from "../header/Header"

import YONATAN from "../pics/yonatan.jpeg"

function Songs(){

    const [pic,setPic] = useState(null)

    return(
        <div className="Songs">
            <Header/>
            {pic ?
                <div className="image_page"  onClick={() => setPic(null)}>
                    <div className="image_container">
                        <img src={pic} alt={"pic"} />
                    </div>
                </div>
                :
                <div className="page">
                    <div className="instructions"><h1>Choose a song you'd like to learn</h1></div>
                    <div className="songs_container">
                        <div className="song_container">
                            <h4>Hatikva</h4>
                        </div>
                        <div className="song_container" onClick={() => setPic(YONATAN)}>
                            <h4>Yonatan Hakatan</h4>
                        </div>
                        <div className="song_container">
                            <h4>No woman no cry</h4>
                        </div>
                    </div>
                </div>
            }
        </div>
    )
}

export default Songs