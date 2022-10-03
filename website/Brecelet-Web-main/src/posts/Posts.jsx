import Header from "../header/Header"
import Post from "./Post/Post"

import "./Posts.css"

import { useState,useEffect } from 'react'
import axios from "axios";
import PostState from "./context/PostState";


function Posts() {

    const MUSIC_URL = (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') ? "http://localhost:3001/music" : "https://musical-bracelet-server.herokuapp.com/music"
    const [musicFiles,setMusicFiles] = useState(null)
    const [err, setErr] = useState("loading...")

    useEffect(()=>{
        const getMusic = async () =>{
            try {
                const res = await axios.get(MUSIC_URL)
                console.log(res)
                setMusicFiles(res.data.files)
                setErr(null)
            }catch (err){
                setErr(err.message)
            }
        }
        getMusic()
    }, [])


    return (
        <div className="Posts">
            <Header/>
            <div className="posts_container">
                <PostState>
                    {err ? <div className="err">{err}</div> :
                        musicFiles.map((musicFile,i)=>{
                            console.log(MUSIC_URL)
                            return(<Post file={musicFile} url={MUSIC_URL} index={i}/>)
                        })}
                </PostState>
            </div>
        </div>
    )
}

export default Posts