<template>
  <main class="main-container">
    <div v-if="!loading" class="header-section">
      <h1 class="group-title">{{ store.groupDetail.name }}</h1>
      <div class="button-group">
        <button v-if="!isMember" @click="joinMeet(store.groupDetail.id)" class="btn btn-orange">둥지 들어가기</button>
        <button v-if="isMember && store.user.id !== store.groupDetail.admin" @click="leaveMeet(store.groupDetail.id)" class="btn btn-orange">둥지 나가기</button>
      </div>
      <div v-if="store.user.id === store.groupDetail.admin" class="admin-buttons">
        <button @click="goToUpdateMeet(store.groupDetail.id)" class="btn btn-orange">둥지 수정하기</button>
        <button @click="deleteMeet(store.groupDetail.id)" class="btn btn-orange">둥지 삭제하기</button>
      </div>
    </div>

    <div class="keywords">
      <span v-for="keyword in store.groupDetail.keywords_list" :key="keyword.pk" class="keyword">
        {{ keyword }}
      </span>
    </div>

    <div v-if="loading" class="loading-container">
      <p class="loading-text">아직 로딩중이덕</p>
    </div>

    <div v-if="isMember" class="movies-container">
      <div class="container">
        <div class="row">
          <div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 d-flex align-items-stretch" v-for="movie in paginatedMovies" :key="movie.id">
            <div class="card mb-4">
              <img :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" class="card-img-top" alt="#">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ movie.title }}</h5>
                <button @click="goToMovie(movie.id)" class="btn btn-orange mt-auto">영화 상세 페이지</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="movies-container">
      <div class="container">
        <div class="row">
          <div class="col-xl-2 col-lg-3 col-md-4 col-sm-6 d-flex align-items-stretch" v-for="movie in paginatedLimitedMovies" :key="movie.id">
            <div class="card mb-4">
              <img :src="`https://image.tmdb.org/t/p/original${movie.poster_path}`" class="card-img-top" alt="#">
              <div class="card-body d-flex flex-column">
                <h5 class="card-title">{{ movie.title }}</h5>
                <button class="btn btn-lightorange mt-auto">가입해줄 수 있덕?</button>
              </div>
            </div>
          </div>
          <div class="join-message-container">
            <h2 class="join-message">🐣가입하면 더 많은 영화 추천과 영화 정보를 확인할 수 있덕🐣</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="pagination-buttons">
      <button class="btn btn-lightorange me-2" :disabled="currentPage === 1" @click="prevPage">이전</button>
      <button class="btn btn-lightorange" :disabled="currentPage === totalPages" @click="nextPage">다음</button>
    </div>

  </main>
</template>

<script setup>
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref, watch, computed } from 'vue'
import { useRoute, useRouter, onBeforeRouteLeave } from 'vue-router'

const store = useMovieStore()
const route = useRoute()
const router = useRouter()

const movies = ref([])
const limitedMovies = ref([])
const loading = ref(true)
const meetId = ref(null) // meetId를 상태로 추가

const currentPage = ref(1)
const itemsPerPage = 6

const paginatedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return movies.value.slice(start, end)
})

const paginatedLimitedMovies = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return limitedMovies.value.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(movies.value.length / itemsPerPage)
})

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const isMember = computed(() => {
  return Array.isArray(store.groupDetail.users) && store.groupDetail.users.includes(store.user.id);
})


onMounted(async () => {
  meetId.value = route.params.id; // meetId를 상태에 저장
  console.log(route.params.id)
  await store.getGroupDetail(meetId.value);
  store.getMoviesByKeywords(store.groupDetail.keywords);
  movies.value = store.filteredMovies;
  limitedMovies.value = store.filteredMovies.slice(0, 6);
  loading.value = false;
});

watch(
  () => store.filteredMovies, 
  (newMovies) => {
    movies.value = newMovies.slice();
    limitedMovies.value = newMovies.slice(0, 6);
  },
  { deep: true }
)

onBeforeRouteLeave((to, from, next) => {
  store.filteredMovies = [];
  next();
})

const joinMeet = function(meet_id) {
  store.modifyMeet(meet_id, 'post')
}

const leaveMeet = function(meet_id) {
  store.modifyMeet(meet_id, 'delete')
}

const goToMovie = function(movieId) { // meetId를 상태에서 가져옴
  if (isMember.value) {
    console.log(`보냅니다 meetId ${meetId.value}, movieId ${movieId}`)
    router.push({ name: 'movie', params: { meetId: meetId.value, movieId: movieId } })
  }
}

const goToUpdateMeet = function(id) {
  router.push({ name: 'update_meet', params: { id: id } })
}

const deleteMeet = function(id) {
  store.meetUpdateAndDelete(id, {}, 'delete')
}
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

.main-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 추가: 공간을 균등하게 분배 */
  align-items: center;
  min-height: 100vh; /* 추가: 최소 높이를 100vh로 설정하여 화면 중앙에 배치 */
  padding-top: 20px; /* 추가: 상단 간격 */
  padding-bottom: 20px; /* 추가: 하단 간격 */
}

.header-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.group-title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2.5rem;
  font-weight: 700;
  color: #FF8C00;
  text-align: center;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
}

.admin-buttons {
  display: flex;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.keywords {
  font-family: 'Gowun Dodum', sans-serif;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 20px;
}

.keyword {
  background-color: #FFE4B5;
  border-radius: 15px;
  padding: 5px 10px;
  font-size: 1rem;
  color: #1b1b1b;
  margin: 0 5px;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.loading-text {
  text-align: center;
  font-size: 1.5rem;
  color: #FF8C00;
}

.movies-container {
  flex-grow: 1; /* 추가: 남은 공간을 채우도록 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container {
  max-width: 1200px;
  margin: auto;
}

.row {
  display: flex;
  flex-wrap: wrap;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 카드 안의 콘텐츠를 균등하게 분배 */
  margin-bottom: 20px; /* 카드 사이의 간격 추가 */
}

.card:hover {
  transform: scale(1.05);
}

.card-img-top {
  height: 300px; /* 포스터 이미지의 높이 고정 */
  object-fit: cover; /* 이미지가 카드 크기에 맞춰짐 */
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: 'Gowun Dodum', sans-serif;
  padding: 10px; /* 패딩 추가 */
}

.card-title {
  font-family: 'Gowun Dodum', sans-serif;
  font-size: 1.2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 10px; /* 제목과 버튼 사이의 간격 조정 */
}

.btn-orange {
  background-color: #fc9619;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 20px;
  transition: background-color 0.3s;
  width: 150px;
  margin-bottom: 10px; /* 버튼과 카드 바닥 사이의 간격 조정 */
  margin-top: auto; /* 버튼을 카드 하단에 고정 */
}

.btn-lightorange {
  background-color: #ffcf94;
  color: rgb(255, 255, 255);
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 20px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: auto;
  width: 160px;
}

.btn-orange:hover {
  background-color: #FF7300;
}

.btn-lightorange:hover {
  background-color: #FF7300;
}

.join-message-container {
  font-family: 'Nanum Gothic', sans-serif;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100px;
}

.join-message {
  text-align: center;
  font-size: 1.5rem;
  color: #FF8C00;
}

.pagination-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 추가: 작은 화면에서도 카드 간격을 유지하기 위한 미디어 쿼리 */
@media (max-width: 700px) {
  .col-sm-6 {
    margin-bottom: 20px; /* 작은 화면에서 카드 사이의 간격을 더 넓게 설정 */
  }
}
</style>
