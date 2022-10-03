import {SET_CURRNT_POST,SET_PLAYING} from "../../consts/consts";

const PostReducer = (state,action) =>{

    switch (action.type){
        case SET_CURRNT_POST:
            return {
                ...state,
                currentPost: action.data,
                playing: true
            }
        case SET_PLAYING:
            return{
                ...state,
                playing: action.data
            }
        default :
            return state
    }

}

export default PostReducer