<template>
  <form v-if="store.isLogin && store.user">
    <main class="container">
      <h3 class="section-title text-center">이런 둥지는 어떠십니꽉?</h3>
      <div class="card-slider-wrapper">
        <div class="card-slider">
          <div 
            class="card-container" 
            v-for="group in filteredGroups" 
            :key="group.id"
            >
            <div class="card h-100">
              <div class="card-body text-center">
                <h5 class="card-title"><strong>{{ group.name }}</strong></h5>
                <div class="card-text">
                <span class="keyword" v-for="(keyword, index) in group.keywords_list.slice(0, 3)" :key="index">
                  {{ keyword }}
                </span>
                <span v-if="group.keywords_list.length > 3" class="extra-keywords">
                  외 {{ group.keywords_list.length - 3 }}개
                </span>
                </div>
                <p>덕친 수: {{ group.users.length }}명</p>
                <button class="btn btn-orange" v-if="store.isLogin && store.user" @click="goToDetail(group.id)">둥지 살펴보기</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </form>
  <form v-else>
    <main class="container">
      <h3 class="section-title text-center">당신을 기다리고 있는 둥지들</h3>
      <div class="card-slider-wrapper">
        <div class="card-slider">
          <div
            class="card-container" 
            v-for="group in store.groups" 
            :key="group.id"
            >
            <div class="card h-100">
              <div class="card-body text-center">
                <h5 class="card-title">{{ group.name }}</h5>
                <div class="card-text">
                  <span class="keyword" v-for="(keyword, index) in group.keywords_list.slice(0, 3)" :key="index">
                    {{ keyword }}
                  </span>
                  <span v-if="group.keywords_list.length > 3" class="extra-keywords">
                    외 {{ group.keywords_list.length - 3 }}개
                  </span>
                </div>
                <p>덕친 수: {{ group.users.length }}명</p>
              </div>
              </div>
            </div>
          </div>
        </div>
    </main>
  </form>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useMovieStore } from '@/stores/movie'
import { useRouter } from 'vue-router'

const store = useMovieStore()
const router = useRouter()

onMounted(() => {
  store.getGroups()
  // store.getJoinedGroups()
})

const joinedGroupIds = computed(() => {
  return store.joinedGroups.map(group => group.id)
})

const filteredGroups = computed(() => {
  return store.groups.filter(group => !joinedGroupIds.value.includes(group.id))
})

const goToDetail = function(id) {
  router.push({ name: 'detail', params: { id: id } })
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

.section-title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #363636;
  margin-bottom: 20px;
}

.card {
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.card:hover {
  transform: scale(1.05);
}

.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  font-family: 'Gowun Dodum', sans-serif;
}

.card-title, .card-text, .p {
  font-family: 'Gowun Dodum', sans-serif;
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

.card-slider-wrapper {
  overflow: hidden;
  position: relative;
  width: 100%;
}

.card-slider {
  display: flex;
  flex-wrap: wrap;
  animation: card-slide 10s linear infinite;
}

.card-container {
  flex: 0 0 25%;
  box-sizing: border-box;
  padding: 10px;
}

@keyframes card-slide {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(-100%);
  }
}

.card-slider:hover {
  animation-play-state: paused;
}

.card-text {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 5px;
  margin-top: 10px;
}

.keyword {
  background-color: #FFE4B5;
  border-radius: 15px;
  padding: 5px 10px;
  font-size: 0.9rem;
  color: #1b1b1b;
  font-family: 'Gowun Dodum', sans-serif;
}

.extra-keywords {
  margin-left: 5px;
  font-size: 0.9rem;
  color: #0f0f0f;
  font-family: 'Gowun Dodum', sans-serif;
}
</style>
