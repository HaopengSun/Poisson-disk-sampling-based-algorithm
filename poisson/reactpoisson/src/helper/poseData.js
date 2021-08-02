import axios from "axios";

const poseParameter =function(parameter){
  axios.post('http://localhost:8000/api/algorithms/', parameter)
}

export default poseParameter