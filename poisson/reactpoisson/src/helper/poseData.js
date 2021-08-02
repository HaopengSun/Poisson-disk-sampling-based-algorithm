import axios from "axios";
// import { useEffect } from "react";

const poseParameter =function(parameter){
  axios.post('http://localhost:8000/api/algorithms/', parameter)
}

export default poseParameter