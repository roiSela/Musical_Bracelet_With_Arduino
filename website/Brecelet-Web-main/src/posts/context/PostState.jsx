import React, {useReducer} from "react"
import PostContext from "./PostContext";

import PostReducer from "./PostReducer";
import {SET_CURRNT_POST, SET_PLAYING} from "../../consts/consts";

const PostState = (props) => {
    const initialState ={
        currentPost: 0,
        playing: false
    }

    const [state,dispatch] = useReducer(PostReducer, initialState)

    const setCurrentPost = (index) => dispatch({type:SET_CURRNT_POST,data: index})
    const setPlaying = (bool) => dispatch({type:SET_PLAYING, data:bool})

    return (
        <PostContext.Provider
        value={{
            currentPost: state.currentPost,
            playing: state.playing,
            setCurrentPost,
            setPlaying
        }}>
            {props.children}
        </PostContext.Provider>
)
}

export default PostState

