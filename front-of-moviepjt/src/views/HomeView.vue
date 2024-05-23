<template>
  <div class="container d-flex flex-column align-items-center min-vh-100 p-3" style="background-color: #FFF9DB;">
    <main class="w-100">
      <h2 class="text-center"> 🐣duck9 홈페이지에 방문하신걸 환영합니덕🐣</h2>
      <form v-if="store.isLogin && store.user" class="text-center mt-4">
        <p>
          <span class="fw-bold fs-4">{{ store.user.username }}</span> 님 반갑덕!
        </p>
        <button class="btn btn-orange" @click="createPage">그룹 만들기!</button>
      </form>
      <br>
      <MeetGroup />
    </main>
  </div>
</template>

<script setup>
import MeetGroup from '@/components/MeetGroup.vue'
import { useRouter } from 'vue-router'
import { useMovieStore } from '@/stores/movie'

const router = useRouter()
const store = useMovieStore()

const createPage = function() {
  router.push({ name: 'create'})
}

console.log(store.user)
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

h2, p, span, button {
  font-family: 'Gowun Dodum', sans-serif;
}

h2 {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #2c2c2c;
}

.btn-orange {
  background-color: #FF8C00;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 25px;
  transition: background-color 0.3s;
}

.btn-orange:hover {
  background-color: #FF7300;
}

.container {
  max-width: 1200px;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.card:hover {
  transform: scale(1.05);
}

@keyframes card-slide {
  0% {
    transform: translateX(-100%);
  }
  50% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(100%);
  }
}

.card-slider {
  display: flex;
  overflow: hidden;
  width: 100%;
  margin-top: 20px;
}

.card-slider .card {
  min-width: 300px;
  margin-right: 20px;
  animation: card-slide 5s infinite;
}
</style>
