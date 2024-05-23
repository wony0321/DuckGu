<template>
  <div class="container">
    <h1 class="title">리뷰 수정 페이지</h1>
    <div class="card">
      <form @submit.prevent="updateReview">
        <div class="form-group">
          <label for="rate">별점:</label>
          <MovieReviewStar v-model:rate="review.rate" :editable="true" />
        </div>
        <div class="form-group">
          <label for="content">리뷰 내용:</label>
          <textarea id="content" v-model="review.content" required></textarea>
        </div>
        <button type="submit" class="btn btn-orange">수정</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useMovieStore } from '@/stores/movie'
import MovieReviewStar from '@/components/MovieReviewStar.vue'

const router = useRouter()
const route = useRoute()
const store = useMovieStore()

const review = ref({
  rate: 0,
  content: ''
})

onMounted(() => {
  axios({
    method: 'get',
    url: `${store.API_URL}/duck9/movie/${route.params.movieId}/review/${route.params.reviewId}/`,
    headers: {
      Authorization: `Token ${store.token}`
    }
  })
    .then((res) => {
      review.value = res.data
    })
    .catch((err) => {
      console.log(err)
    })
})

function updateReview() {
  axios({
    method: 'put',
    url: `${store.API_URL}/duck9/movie/${route.params.movieId}/review/${route.params.reviewId}/`,
    headers: {
      Authorization: `Token ${store.token}`
    },
    data: {
      rate: review.value.rate,
      content: review.value.content
    }
  })
    .then((res) => {
      alert('리뷰가 수정되었습니덕! 🐣')
      router.push({ name: 'movie', params: { meetId: route.params.meetId, movieId: route.params.movieId } })
    })
    .catch((err) => {
      console.log(err)
      alert('리뷰 수정에 실패했습니다.')
    })
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

.container {
  max-width: 600px;
  margin: 20px auto;
  padding: 20px;
  background-color: #FFF2B2;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title {
  font-family: 'Nanum Gothic', sans-serif;
  font-size: 2rem;
  font-weight: 700;
  color: #FF8C00;
  text-align: center;
  margin-bottom: 20px;
}

.card {
  font-family: 'Gowun Dodum', sans-serif;
  background: white;
  padding: 20px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 15px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #FF8C00;
}

input, textarea {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #FF8C00;
}

textarea {
  resize: vertical;
  min-height: 100px;
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
</style>
