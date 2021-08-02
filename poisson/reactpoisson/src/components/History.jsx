import React, {useEffect, useState} from 'react'
import axios from "axios";

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
  }, [])

  return (
    <div className='poisson'>
      <h2>History</h2>
      {data.map(his => {
        return JSON.stringify(his)
      })}
    </div>
  )
}

export default History