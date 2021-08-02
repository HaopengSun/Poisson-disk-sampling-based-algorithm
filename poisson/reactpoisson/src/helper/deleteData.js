import axios from "axios";

const poseParameter =function(id){
  axios.delete(`http://localhost:8000/api/algorithms/${id}/`)
}

export default poseParameter