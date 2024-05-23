<template>
  <div class="container">
    <MovieDetail :movie="currentMovie" :meetId="meetId"/>
    <div class="navigation-buttons">
      <button @click="goToList" class="btn btn-nav">목록가기</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import MovieDetail from '@/components/MovieDetail.vue'
import { useMovieStore } from '@/stores/movie'

const router = useRouter()
const route = useRoute()
const store = useMovieStore()

const meetId = ref(null)
const movieId = ref(null)
const movies = ref([])
const currentMovie = ref(null)

const goToList = () => {
  router.push({ name: 'detail', params: { id: meetId.value } })
}

const getMovies = async function () {
  await store.getGroupDetail(meetId.value)
  await store.getMoviesByKeywords(store.groupDetail.keywords)
  movies.value = store.filteredMovies
  setCurrentMovie()
}

const setCurrentMovie = () => {
  currentMovie.value = movies.value.find(movie => movie.id === parseInt(movieId.value))
}

const goToPreviousMovie = () => {
  const currentIndex = movies.value.findIndex(movie => movie.id === parseInt(movieId.value))
  if (currentIndex > 0) {
    const previousMovieId = movies.value[currentIndex - 1].id
    router.push({ name: 'movie', params: { meetId: meetId.value, movieId: previousMovieId } })
  }
}

const goToNextMovie = () => {
  const currentIndex = movies.value.findIndex(movie => movie.id === parseInt(movieId.value))
  if (currentIndex < movies.value.length - 1) {
    const nextMovieId = movies.value[currentIndex + 1].id
    router.push({ name: 'movie', params: { meetId: meetId.value, movieId: nextMovieId } })
  }
}

onMounted(() => {
  meetId.value = Number(route.params.meetId)
  movieId.value = route.params.movieId
  getMovies()
})

watch(() => route.params.movieId, (newMovieId) => {
  movieId.value = newMovieId
  setCurrentMovie()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  font-family: 'Gowun Dodum', sans-serif;
  background-color: #FFF9DB;
  margin: 0;
  padding: 0;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 5px;
}

.navigation-buttons {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.btn {
  background-color: #fca234;
  color: #fff;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin: 0 10px;
  width: 200px;
}

.btn:hover {
  background-color: #ffe0a7;
}

.btn-nav {
  font-family: 'Gowun Dodum', sans-serif;
  font-size: 1rem;
}
</style>
