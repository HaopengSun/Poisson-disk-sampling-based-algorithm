import React, {useEffect, useState} from 'react'
import axios from "axios";
import deleteData from "../helper/deleteData"

const History = function(){

  const [data, setData] = useState([])

  useEffect(() => {
    axios.get('/api/algorithms/')
    .then(function (response) {
      setData(response.data);
    })
    .catch(function (error) {
      console.log(error);
    })
  }, [data])

  return (
    <div className='poisson'>
      <h2>History</h2>
      {data.map((his, idx) => {
        return (
        <div key={idx}>
          <h6>{JSON.stringify(his)}</h6>
          <div>
            <button className="btn btn-light" >edit</button>
            <button className="btn btn-light" onClick={() => deleteData(his.id)}>delete</button>
          </div>
        </div>
        )
      })}
    </div>
  )
}

export default History