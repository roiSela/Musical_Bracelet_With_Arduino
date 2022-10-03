import { RiPlayMiniFill } from "react-icons/ri";
import {RiPauseMiniFill} from "react-icons/ri";
import { useState,useEffect,useRef,useContext } from 'react'


import './Post.css'
import PostContext from "../context/PostContext";



function calcTime(sec) {
    const MINUTE = 60

    let minute = 0

    minute = ~~(sec / MINUTE)
    sec = sec - (minute*MINUTE)

    sec = ~~sec
    const MM = minute < 10 ? "0" + minute : minute
    const SS = sec < 10 ? "0" + sec : sec
    return MM + ":" + SS

}

function Post({file,url,index}) {
    const {
        currentPost,
        playing,
        setCurrentPost,
        setPlaying,
    } = useContext(PostContext)

    const [duration,setDuration] = useState(0)
    const [time,setTime] = useState(0)
    const [range,setRange ] = useState(0)
    const audio = useRef('audio_tag')

    let inputChange = false



    useEffect(()=>{

        audio.current.currentTime = time
    },[])

    const togglePlay = (on) =>{
        if(on) {
            setCurrentPost(index)
            audio.current.play()
        }
        else{
            setPlaying(false)
            audio.current.pause()

        }
    }

    const handleRange = (e) => {
        inputChange = true
        const range = e.target.value
        const currentTime = duration * range / 100

        audio.current.currentTime = currentTime
        setRange(range)
        setTime(currentTime)

        inputChange = false
    }

    if (currentPost !== index && playing ) {
            audio.current.pause()
    }

    const handleTimeUpdate = (e) => {
        if (!inputChange) {
            setTime(e.target.currentTime)
            setRange(e.target.currentTime / duration * 100)
        }
    }

    const handlePlay =(e)=>{
        duration === 0 ? setDuration((e.target.duration)) : null
        duration === 0 ? e.target.currentTime = time : null
    }

    const handleEnd = (e) => {
        setRange(0)
        setPlaying(false)
    }


    return(
        <div className={"post " + ((index !== 0 )? "border-top" : "")}  key={file._id} >
            <audio
            ref={audio}
            onTimeUpdate={handleTimeUpdate}
            onCanPlay={handlePlay}
            onEnded={handleEnd}
            type="audio/mpeg"
            preload="metadata"
            src={url+'/'+file.filename}>
            </audio>
            <div className="play-container">
                {currentPost === index && playing ? <RiPauseMiniFill size={25} onClick={() => togglePlay(false)} /> : <RiPlayMiniFill size={25} onClick={() => togglePlay(true)} />}
            </div>
            <div className="slider-container">
                <div className="purple-line" style={{width:range +'%'}}/>
                <input
                    className="slider"
                    type="range"
                    name="progresBar"
                    id="prgbar"
                    value={range}
                    onChange={handleRange}
                />
            </div>
            <div className="time">{calcTime(time)}/{calcTime(duration)}</div>
        </div>
    )
}






export default Post