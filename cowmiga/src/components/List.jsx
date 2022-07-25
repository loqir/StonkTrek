import React, { useState } from 'react'
import { collection, getDocs, query, orderBy, limit } from 'firebase/firestore'
import { db } from '../lib/init-firebase'
import { useEffect } from 'react'


export default function List() {

    const [movies, setMovies] = useState([])

    useEffect(() => {
        getMovies()
    }, [])

    useEffect(() => {
        console.log(movies)
    }, [movies])

    function getMovies() {
        const listRef = collection(db, 'searches')
        getDocs(listRef).then(response => {
            console.log(response.docs)
            const movs = response.docs.map(doc => ({
                data: doc.data(),
                id: doc.id,
            }))
            setMovies(movs)
        })
            .catch(error => console.log(error.message))
    }

    return (
        <div>
            <button onClick={() => getMovies()}>Refresh</button>
            <ul>
                {console.log(movies)}
            {movies.map(movie => <li key = {movie.data.count}>{movie.data.name} <bold> count: </bold>{movie.data.count}</li> )}
            </ul>

        </div>
    )
}
