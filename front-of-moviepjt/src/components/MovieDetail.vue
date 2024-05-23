<template>
  <div class="main-container" v-if="movie">
    <div class="movie-info">
      <img :src="poster" alt="영화 포스터" class="poster">
      <h2> {{ movie.title }}</h2>
      <p class="ms-2">개봉일 : {{ movie.release_date }}</p>
      <p class="ms-2">평점: {{ movie.vote_average }}점</p>
      <p class="ms-2">
        <img 
          :src="isLiked ? fullheart : emptyheart" 
          alt="하트 아이콘" 
          class="heart-icon"
          @click="likeMovie"
        >
        {{ movie.like_users.length }}명이 좋아합니다.
      </p> 
      <p class="ms-2">
        키워드:
        <span v-for="(keyword, index) in limitedKeywords" :key="keyword">
          {{ keyword }}<span v-if="index < limitedKeywords.length - 1"> | </span>
        </span>
        <span v-if="remainingKeywordsCount > 0">
          외 {{ remainingKeywordsCount }}개
        </span>
      </p>
      <hr>
    </div>
    <div class="review-section">
      <MovieReviewCreate :movieId="movieId" @review-submitted="getReviews" />
      <hr>
      <div>
        <h2>리뷰 목록</h2>
        <div v-if="currentReviews.length">
          <MovieReview 
            v-for="review in currentReviews"
            :key="review.id"
            :reviewId="review.id"
            :movie="movie"
            :meetId="props.meetId"
            @reviewDeleted="getReviews"
          />
          <div class="pagination-buttons">
            <button class="btn btn-lightorange me-2" :disabled="currentPage === 1" @click="prevPage">이전</button>
            <button class="btn btn-lightorange" :disabled="currentPage === totalPages" @click="nextPage">다음</button>
          </div>
        </div>
        <div v-else>
          <p>리뷰가 없덕! 첫 리뷰어가 되어 볼꽉?</p>
        </div>
      </div>
    </div>
  </div>
  <div v-else>
    <p>로딩중이덕! 좀만 기다려 줄 수 있을꽉?</p>
  </div>
</template>

<script setup>
import MovieReview from './MovieReview.vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import { onMounted, ref, computed } from 'vue'
import emptyheart from '@/assets/emptyheart.png'
import fullheart from '@/assets/fullheart.png'
import MovieReviewCreate from './MovieReviewCreate.vue'

const route = useRoute()
const store = useMovieStore()
const movie = ref(null)
const movieId = ref(null)
const poster = ref('')

const props = defineProps({
  movie: {
    type: Object,
    required: true
  },
  meetId: Number
})

const currentPage = ref(1)
const reviewsPerPage = 3

const currentReviews = computed(() => {
  const start = (currentPage.value - 1) * reviewsPerPage
  const end = start + reviewsPerPage
  return movie.value.review_set.slice(start, end)
})

const totalPages = computed(() => {
  return Math.ceil(movie.value.review_set.length / reviewsPerPage)
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
  movie.value = props.movie 
  movieId.value = Number(route.params.movieId)
  getReviews()
})

const isLiked = computed(() => {
  return movie.value && movie.value.like_users.includes(store.user)
})

const likeMovie = function () {
  axios({
    method: 'post',
    url: `${store.API_URL}/duck9/movie/${movie.value.id}/like/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      const { isLikeMovie, like_count } = res.data
      if (isLikeMovie) {
        movie.value.like_users.push(store.user)
      } else {
        movie.value.like_users = movie.value.like_users.filter(user => user !== store.user)
      }
      movie.value.like_users.length = like_count
    })
    .catch((err) => {
      console.log(err)
    })
}

const getReviews = function () {
  axios({
    method: 'get',
    url: `${store.API_URL}/duck9/movie/${movieId.value}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      movie.value = res.data
      poster.value = `https://image.tmdb.org/t/p/original${res.data.poster_path}`
    })
    .catch((err) => {
      console.log(err)
    })
}

const limitedKeywords = computed(() => {
  return movie.value.keywords_list.slice(0, 3)
})

const remainingKeywordsCount = computed(() => {
  return movie.value.keywords_list.length - limitedKeywords.value.length
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

.main-container {
  display: flex;
  justify-content: center;
  gap: 30px;
  padding: 20px;
}

.movie-info, .review-section {
  font-family: 'Gowun Dodum', sans-serif;
  background: #FFF2B2;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  flex: 1;
  max-width: 700px;
}

.poster {
  width: 100%;
  height: auto;
  border-radius: 15px;
  margin-bottom: 20px;
}

h2 {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FF8C00;
  margin-bottom: 10px;
  margin-left: 3px;
}

hr {
  border: 1px solid #FF8C00;
}

button {
  padding: 10px;
  font-size: 16px;
  background-color: #FF8C00;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
  width: 100%;
}

button:hover {
  background-color: #FF7300;
}

.pagination-buttons {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.btn-lightorange {
  background-color: #ffcf94;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-lightorange:hover {
  background-color: #FF7300;
}

.me-2 {
  margin-right: 10px;
}

.heart-icon {
  cursor: pointer;
  margin-right: 5px;
  width: 20px; /* 하트 아이콘 크기 */
}
</style>
