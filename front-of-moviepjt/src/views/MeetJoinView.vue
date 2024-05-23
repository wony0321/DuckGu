<template>
  <main class="container">
    <span v-if="store.joinedGroups.length > 0">
      <h1 class="page-title">🧡참여 중인 둥지들입니덕🧡</h1>
    </span>
    <span v-else>
      <h1 class="page-title">아직 참여중인 둥지가 없습니다</h1>
    </span>
    <div class="row justify-content-center">
      <div class="col-lg-4 col-md-6 col-sm-12 mb-4" v-for="meet in paginatedGroups" :key="meet.name">
        <div class="card h-100 position-relative">
          <div class="card-body text-center">
            <h5 class="card-title">{{ meet.name }}</h5>
            <p class="card-text">
              <strong>덕친 수: {{ meet.users.length }}명</strong> 
            </p>
            <p class="card-text">
              <span v-for="(keyword, index) in meet.keywords_list.slice(0, 3)" :key="index" class="keyword">
                <strong>{{ keyword }}</strong>
              </span>
              <span v-if="meet.keywords_list.length > 3">
                <strong>외 {{ meet.keywords_list.length - 3 }}개</strong>
              </span>
            </p>
            <button class="btn btn-orange" @click="goToMeet(meet.id)">입장하기</button>
          </div>
        </div>
      </div>
    </div>
    <div class="d-flex justify-content-center m-4">
      <button class="btn btn-lightorange me-2" :disabled="currentPage === 1" @click="prevPage">이전</button>
      <button class="btn btn-lightorange" :disabled="currentPage === totalPages" @click="nextPage">다음</button>
    </div>
  </main>
  <br>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie';

const store = useMovieStore()
const router = useRouter()

const currentPage = ref(1)
const itemsPerPage = 6

const paginatedGroups = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return store.joinedGroups.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(store.joinedGroups.length / itemsPerPage)
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

onMounted(() => {
  store.getJoinedGroups()
  store.joinedGroups.reverse()
})

const goToMeet = function(id) {
  router.push({ name: 'detail', params: { id: id } })
}

console.log(store.joinedGroups)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Gowun+Dodum&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@700&display=swap');

body {
  background-color: #FFF9DB; /* 연한 노란색 배경 */
  font-family: 'Gowun Dodum', sans-serif; /* 귀여운 글꼴 */
  margin: 0;
  padding: 0;
}

.page-title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FF8C00;
  margin-bottom: 20px;
  text-align: center;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.card-title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: x-large;
}

.card:hover {
  transform: scale(1.05);
}

.card-body {
  font-family: 'Gowun Dodum', sans-serif;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.btn-orange {
  background-color: #FF8C00;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.btn-lightorange {
  background-color: #ffcf94;
  color: white;
  border: none;
  padding: 10px 20px;
  font-size: 1rem;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-top: 10px;
}

.btn-orange:hover {
  background-color: #FF7300;
}

.btn-lightorange:hover {
  background-color: #FF7300;
}

.card-text {
  margin: 10px 0;
}

.keyword {
  display: inline-block;
  background-color: #FFE4B5; /* 밝은 주황색 배경 */
  border-radius: 15px;
  padding: 5px 10px;
  margin: 2px;
  font-size: 0.9rem;
  color: #141414;
}

.btn-sm {
  padding: 5px 10px;
  font-size: 0.75rem;
  border-radius: 15px;
}

.position-absolute {
  position: absolute;
}

.top-0 {
  top: 0;
}

.end-0 {
  right: 0;
}

.m-2 {
  margin: 0.5rem;
}

.d-flex {
  display: flex;
}

.justify-content-center {
  justify-content: center;
}

.me-2 {
  margin-right: 0.5rem;
}

.mt-4 {
  margin-top: 1.5rem;
}
</style>
